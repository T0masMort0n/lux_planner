from __future__ import annotations

import sqlite3
from typing import Optional

from lux.data.models.tasks import (
    TaskDefinitionRow,
    TaskOccurrenceRow,
    TaskOccurrenceJoinedRow,
    bool_from_int,
    now_sqlite,
)


class TasksRepository:
    """
    Data-layer repository for task definitions and occurrences.

    Performance rules:
    - Queries must be bounded (date range + LIMIT).
    - Avoid N+1 by using JOIN for occurrence lists where we need task title.
    """

    def __init__(self, conn: sqlite3.Connection) -> None:
        self._conn = conn

    # -------------------------
    # Definitions
    # -------------------------
    def create_task(self, title: str, notes: str = "", parent_task_id: int | None = None) -> int:
        cur = self._conn.execute(
            """
            INSERT INTO task_definitions(title, notes, parent_task_id, archived)
            VALUES (?, ?, ?, 0)
            """,
            (title.strip(), notes or "", parent_task_id),
        )
        self._conn.commit()
        return int(cur.lastrowid)

    def get_task(self, task_id: int) -> Optional[TaskDefinitionRow]:
        row = self._conn.execute(
            "SELECT * FROM task_definitions WHERE id = ?",
            (int(task_id),),
        ).fetchone()
        if not row:
            return None

        parent_task_id: int | None
        try:
            v = row["parent_task_id"]
            parent_task_id = int(v) if v is not None else None
        except Exception:
            parent_task_id = None

        return TaskDefinitionRow(
            id=int(row["id"]),
            title=str(row["title"]),
            notes=str(row["notes"]),
            parent_task_id=parent_task_id,
            archived=bool_from_int(row["archived"]),
            created_at=str(row["created_at"]),
            updated_at=str(row["updated_at"]),
        )

    def list_tasks(self, include_archived: bool = False, limit: int = 200) -> list[TaskDefinitionRow]:
        limit = max(1, min(int(limit), 500))
        if include_archived:
            q = "SELECT * FROM task_definitions ORDER BY id DESC LIMIT ?"
            rows = self._conn.execute(q, (limit,)).fetchall()
        else:
            q = "SELECT * FROM task_definitions WHERE archived = 0 ORDER BY id DESC LIMIT ?"
            rows = self._conn.execute(q, (limit,)).fetchall()

        out: list[TaskDefinitionRow] = []
        for r in rows:
            try:
                v = r["parent_task_id"]
                parent_task_id = int(v) if v is not None else None
            except Exception:
                parent_task_id = None

            out.append(
                TaskDefinitionRow(
                    id=int(r["id"]),
                    title=str(r["title"]),
                    notes=str(r["notes"]),
                    parent_task_id=parent_task_id,
                    archived=bool_from_int(r["archived"]),
                    created_at=str(r["created_at"]),
                    updated_at=str(r["updated_at"]),
                )
            )
        return out

    def archive_task(self, task_id: int) -> None:
        self._conn.execute(
            """
            UPDATE task_definitions
            SET archived = 1, updated_at = ?
            WHERE id = ?
            """,
            (now_sqlite(), int(task_id)),
        )
        self._conn.commit()

    # -------------------------
    # Occurrences
    # -------------------------
    def next_sort_key_for_date(self, due_date: str) -> int:
        """
        Return a stable sort_key for a new occurrence on a given day.
        """
        row = self._conn.execute(
            """
            SELECT COALESCE(MAX(sort_key), 0) AS max_sk
            FROM task_occurrences
            WHERE due_date = ?
            """,
            (due_date,),
        ).fetchone()
        max_sk = int(row["max_sk"] or 0) if row else 0
        return max_sk + 1

    def create_occurrence(
        self,
        task_id: int,
        due_date: str,
        due_time: str | None = None,
        sort_key: int | None = None,
    ) -> int:
        if sort_key is None:
            sort_key = self.next_sort_key_for_date(due_date)

        cur = self._conn.execute(
            """
            INSERT INTO task_occurrences(task_id, due_date, due_time, sort_key, archived)
            VALUES (?, ?, ?, ?, 0)
            """,
            (int(task_id), due_date, due_time, int(sort_key)),
        )
        self._conn.commit()
        return int(cur.lastrowid)

    def update_occurrence_due_date(self, occurrence_id: int, target_date: str) -> None:
        """
        Reschedule an occurrence to a specific date (YYYY-MM-DD).
        We also re-assign sort_key to keep stable ordering within the target day.
        """
        new_sort = self.next_sort_key_for_date(target_date)
        self._conn.execute(
            """
            UPDATE task_occurrences
            SET due_date = ?, sort_key = ?, updated_at = ?
            WHERE id = ?
            """,
            (target_date, int(new_sort), now_sqlite(), int(occurrence_id)),
        )
        self._conn.commit()

    def list_occurrences_for_range(
        self,
        start_date: str,
        end_date: str,
        include_archived: bool = False,
        limit: int = 500,
    ) -> list[TaskOccurrenceRow]:
        """
        Bounded query: [start_date, end_date] inclusive, with hard LIMIT.
        Date format expected: YYYY-MM-DD
        """
        limit = max(1, min(int(limit), 2000))
        if include_archived:
            rows = self._conn.execute(
                """
                SELECT *
                FROM task_occurrences
                WHERE due_date >= ? AND due_date <= ?
                ORDER BY due_date ASC, sort_key ASC, id ASC
                LIMIT ?
                """,
                (start_date, end_date, limit),
            ).fetchall()
        else:
            rows = self._conn.execute(
                """
                SELECT *
                FROM task_occurrences
                WHERE archived = 0 AND due_date >= ? AND due_date <= ?
                ORDER BY due_date ASC, sort_key ASC, id ASC
                LIMIT ?
                """,
                (start_date, end_date, limit),
            ).fetchall()

        out: list[TaskOccurrenceRow] = []
        for r in rows:
            out.append(
                TaskOccurrenceRow(
                    id=int(r["id"]),
                    task_id=int(r["task_id"]),
                    due_date=str(r["due_date"]),
                    due_time=str(r["due_time"]) if r["due_time"] is not None else None,
                    sort_key=int(r["sort_key"]),
                    completed_at=str(r["completed_at"]) if r["completed_at"] is not None else None,
                    archived=bool_from_int(r["archived"]),
                    created_at=str(r["created_at"]),
                    updated_at=str(r["updated_at"]),
                )
            )
        return out

    def list_occurrences_joined_for_range(
        self,
        start_date: str,
        end_date: str,
        include_archived: bool = False,
        limit: int = 500,
    ) -> list[TaskOccurrenceJoinedRow]:
        """
        Same as list_occurrences_for_range, but JOINs definitions to avoid N+1 reads.
        """
        limit = max(1, min(int(limit), 2000))

        if include_archived:
            rows = self._conn.execute(
                """
                SELECT
                  o.id,
                  o.task_id,
                  d.title,
                  d.notes,
                  o.due_date,
                  o.due_time,
                  o.sort_key,
                  o.completed_at,
                  o.archived,
                  o.created_at,
                  o.updated_at
                FROM task_occurrences o
                JOIN task_definitions d ON d.id = o.task_id
                WHERE o.due_date >= ? AND o.due_date <= ?
                ORDER BY o.due_date ASC, o.sort_key ASC, o.id ASC
                LIMIT ?
                """,
                (start_date, end_date, limit),
            ).fetchall()
        else:
            rows = self._conn.execute(
                """
                SELECT
                  o.id,
                  o.task_id,
                  d.title,
                  d.notes,
                  o.due_date,
                  o.due_time,
                  o.sort_key,
                  o.completed_at,
                  o.archived,
                  o.created_at,
                  o.updated_at
                FROM task_occurrences o
                JOIN task_definitions d ON d.id = o.task_id
                WHERE o.archived = 0
                  AND d.archived = 0
                  AND o.due_date >= ? AND o.due_date <= ?
                ORDER BY o.due_date ASC, o.sort_key ASC, o.id ASC
                LIMIT ?
                """,
                (start_date, end_date, limit),
            ).fetchall()

        out: list[TaskOccurrenceJoinedRow] = []
        for r in rows:
            out.append(
                TaskOccurrenceJoinedRow(
                    id=int(r["id"]),
                    task_id=int(r["task_id"]),
                    title=str(r["title"]),
                    notes=str(r["notes"]),
                    due_date=str(r["due_date"]),
                    due_time=str(r["due_time"]) if r["due_time"] is not None else None,
                    sort_key=int(r["sort_key"]),
                    completed_at=str(r["completed_at"]) if r["completed_at"] is not None else None,
                    archived=bool_from_int(r["archived"]),
                    created_at=str(r["created_at"]),
                    updated_at=str(r["updated_at"]),
                )
            )
        return out

    def set_occurrence_completed(self, occurrence_id: int, completed: bool) -> None:
        if completed:
            self._conn.execute(
                """
                UPDATE task_occurrences
                SET completed_at = datetime('now'), updated_at = datetime('now')
                WHERE id = ?
                """,
                (int(occurrence_id),),
            )
        else:
            self._conn.execute(
                """
                UPDATE task_occurrences
                SET completed_at = NULL, updated_at = datetime('now')
                WHERE id = ?
                """,
                (int(occurrence_id),),
            )
        self._conn.commit()

    def archive_occurrence(self, occurrence_id: int) -> None:
        self._conn.execute(
            """
            UPDATE task_occurrences
            SET archived = 1, updated_at = datetime('now')
            WHERE id = ?
            """,
            (int(occurrence_id),),
        )
        self._conn.commit()

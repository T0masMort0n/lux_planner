from __future__ import annotations

import sqlite3
from typing import Any

from lux.data.models.schedule import ScheduledEntryRow, bool_from_int, now_sqlite


class ScheduledEntryRepo:
    """DB-only access for scheduled_entries (no business logic)."""

    def __init__(self, conn: sqlite3.Connection) -> None:
        self._conn = conn

    def create(self, entry_data: dict[str, Any]) -> int:
        created = now_sqlite()
        updated = created

        cur = self._conn.execute(
            """
            INSERT INTO scheduled_entries(
                item_kind,
                item_ref,
                start_dt,
                end_dt,
                title_cache,
                notes_cache,
                archived,
                created_at,
                updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, 0, ?, ?)
            """,
            (
                entry_data["item_kind"],
                entry_data["item_ref"],
                entry_data["start_dt"],
                entry_data["end_dt"],
                entry_data.get("title_cache"),
                entry_data.get("notes_cache"),
                created,
                updated,
            ),
        )
        self._conn.commit()
        return int(cur.lastrowid)

    def update_time(self, entry_id: int, new_start: str, new_end: str) -> None:
        self._conn.execute(
            """
            UPDATE scheduled_entries
               SET start_dt = ?,
                   end_dt = ?,
                   updated_at = ?
             WHERE id = ?
            """,
            (new_start, new_end, now_sqlite(), entry_id),
        )
        self._conn.commit()

    def archive(self, entry_id: int) -> None:
        self._conn.execute(
            """
            UPDATE scheduled_entries
               SET archived = 1,
                   updated_at = ?
             WHERE id = ?
            """,
            (now_sqlite(), entry_id),
        )
        self._conn.commit()

    def list_for_range(
        self,
        start_dt: str,
        end_dt: str,
        include_archived: bool = False,
        limit: int = 200,
    ) -> list[ScheduledEntryRow]:
        where_archived = "" if include_archived else "AND archived = 0"
        cur = self._conn.execute(
            f"""
            SELECT
                id,
                item_kind,
                item_ref,
                start_dt,
                end_dt,
                title_cache,
                notes_cache,
                archived,
                created_at,
                updated_at
              FROM scheduled_entries
             WHERE start_dt < ?
               AND end_dt > ?
               {where_archived}
             ORDER BY start_dt ASC
             LIMIT ?
            """,
            (end_dt, start_dt, limit),
        )
        rows = cur.fetchall()

        out: list[ScheduledEntryRow] = []
        for r in rows:
            out.append(
                ScheduledEntryRow(
                    id=int(r["id"]),
                    item_kind=str(r["item_kind"]),
                    item_ref=str(r["item_ref"]),
                    start_dt=str(r["start_dt"]),
                    end_dt=str(r["end_dt"]),
                    title_cache=r["title_cache"],
                    notes_cache=r["notes_cache"],
                    archived=bool_from_int(r["archived"]),
                    created_at=str(r["created_at"]),
                    updated_at=str(r["updated_at"]),
                )
            )
        return out

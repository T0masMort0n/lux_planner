from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta

from lux.data.db import ensure_db_ready
from lux.data.repositories.tasks_repo import TasksRepository
from lux.features.todo.domain import TaskOccurrence
from lux.features.todo.repo import TodoRepo


@dataclass(frozen=True)
class DateRange:
    start: str  # YYYY-MM-DD
    end: str    # YYYY-MM-DD


def _today_str() -> str:
    return date.today().isoformat()


def _range_for_days(days: int) -> DateRange:
    days = max(1, min(int(days), 31))
    start = date.today()
    end = start + timedelta(days=days - 1)
    return DateRange(start=start.isoformat(), end=end.isoformat())


class TodoService:
    """
    Feature service. UI calls here; DB stays behind repos.
    """

    def __init__(self) -> None:
        # Local, feature-owned access to the shared system DB.
        # (Still a single DB file; we just open a connection here.)
        conn = ensure_db_ready()
        self._repo = TodoRepo(TasksRepository(conn))

    # -----------------------
    # Primary: Today
    # -----------------------
    def list_today(self, limit: int = 200) -> list[TaskOccurrence]:
        t = _today_str()
        rows = self._repo.list_occurrences_for_range(t, t, limit=limit)

        # Join title via per-task lookup (still bounded by day's rows).
        # If needed later, we can optimize with a SQL join.
        out: list[TaskOccurrence] = []
        for r in rows:
            task = self._repo.get_task(r.task_id)
            title = task.title if task else f"Task #{r.task_id}"
            out.append(
                TaskOccurrence(
                    id=r.id,
                    task_id=r.task_id,
                    title=title,
                    due_date=r.due_date,
                    due_time=r.due_time,
                    completed=(r.completed_at is not None),
                    archived=r.archived,
                )
            )
        return out

    def add_task_for_today(self, title: str) -> int:
        clean = (title or "").strip()
        if not clean:
            return 0

        task_id = self._repo.create_task(title=clean, notes="")
        occ_id = self._repo.create_occurrence(task_id=task_id, due_date=_today_str(), due_time=None, sort_key=0)
        return occ_id

    def set_completed(self, occurrence_id: int, completed: bool) -> None:
        if occurrence_id <= 0:
            return
        self._repo.set_occurrence_completed(occurrence_id=occurrence_id, completed=completed)

    def archive_occurrence(self, occurrence_id: int) -> None:
        if occurrence_id <= 0:
            return
        self._repo.archive_occurrence(occurrence_id=occurrence_id)

    # -----------------------
    # Upcoming (small window)
    # -----------------------
    def list_upcoming(self, days: int = 7, limit: int = 400) -> list[TaskOccurrence]:
        dr = _range_for_days(days)
        rows = self._repo.list_occurrences_for_range(dr.start, dr.end, limit=limit)

        out: list[TaskOccurrence] = []
        for r in rows:
            task = self._repo.get_task(r.task_id)
            title = task.title if task else f"Task #{r.task_id}"
            out.append(
                TaskOccurrence(
                    id=r.id,
                    task_id=r.task_id,
                    title=title,
                    due_date=r.due_date,
                    due_time=r.due_time,
                    completed=(r.completed_at is not None),
                    archived=r.archived,
                )
            )
        return out

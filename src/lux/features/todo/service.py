from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta

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

    IMPORTANT:
    - DB lifecycle is system-owned. This service must be constructed via bootstrap injection.
    """

    def __init__(self, repo: TodoRepo) -> None:
        self._repo = repo

    # -----------------------
    # Primary: Today
    # -----------------------
    def list_today(self, limit: int = 200) -> list[TaskOccurrence]:
        t = _today_str()
        rows = self._repo.list_occurrences_for_range_joined(t, t, limit=limit)

        out: list[TaskOccurrence] = []
        for r in rows:
            out.append(
                TaskOccurrence(
                    id=r.id,
                    task_id=r.task_id,
                    title=r.title,
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
        occ_id = self._repo.create_occurrence(task_id=task_id, due_date=_today_str(), due_time=None, sort_key=None)
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
        rows = self._repo.list_occurrences_for_range_joined(dr.start, dr.end, limit=limit)

        out: list[TaskOccurrence] = []
        for r in rows:
            out.append(
                TaskOccurrence(
                    id=r.id,
                    task_id=r.task_id,
                    title=r.title,
                    due_date=r.due_date,
                    due_time=r.due_time,
                    completed=(r.completed_at is not None),
                    archived=r.archived,
                )
            )
        return out

    # -----------------------
    # Drag & Drop semantics
    # -----------------------
    def reschedule_occurrence(self, occurrence_id: int, target_date: str) -> None:
        if occurrence_id <= 0:
            return
        self._repo.reschedule_occurrence(occurrence_id=occurrence_id, target_date=target_date)

    def create_occurrence_for_date(self, task_definition_id: int, target_date: str) -> int:
        if task_definition_id <= 0:
            return 0
        return self._repo.create_occurrence(task_id=task_definition_id, due_date=target_date, due_time=None, sort_key=None)

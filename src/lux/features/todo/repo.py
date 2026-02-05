from __future__ import annotations

from typing import Optional

from lux.data.models.tasks import TaskDefinitionRow, TaskOccurrenceJoinedRow, TaskOccurrenceRow
from lux.data.repositories.tasks_repo import TasksRepository


class TodoRepo:
    """
    Feature-level repo adapter.
    """

    def __init__(self, tasks_repo: TasksRepository) -> None:
        self._tasks = tasks_repo

    # ---- Definitions ----
    def create_task(self, title: str, notes: str = "") -> int:
        return self._tasks.create_task(title=title, notes=notes)

    def get_task(self, task_id: int) -> Optional[TaskDefinitionRow]:
        return self._tasks.get_task(task_id)

    # ---- Occurrences ----
    def create_occurrence(
        self,
        task_id: int,
        due_date: str,
        due_time: str | None = None,
        sort_key: int | None = None,
    ) -> int:
        # sort_key=None -> repo auto-assign next stable sort_key for that day
        return self._tasks.create_occurrence(
            task_id=task_id,
            due_date=due_date,
            due_time=due_time,
            sort_key=sort_key,
        )

    def list_occurrences_for_range_joined(self, start_date: str, end_date: str, limit: int = 500) -> list[TaskOccurrenceJoinedRow]:
        return self._tasks.list_occurrences_joined_for_range(start_date=start_date, end_date=end_date, limit=limit)

    # (kept for completeness / future use)
    def list_occurrences_for_range(self, start_date: str, end_date: str, limit: int = 500) -> list[TaskOccurrenceRow]:
        return self._tasks.list_occurrences_for_range(start_date=start_date, end_date=end_date, limit=limit)

    def set_occurrence_completed(self, occurrence_id: int, completed: bool) -> None:
        self._tasks.set_occurrence_completed(occurrence_id=occurrence_id, completed=completed)

    def archive_occurrence(self, occurrence_id: int) -> None:
        self._tasks.archive_occurrence(occurrence_id=occurrence_id)

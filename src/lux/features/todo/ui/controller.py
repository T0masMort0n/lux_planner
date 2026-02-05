from __future__ import annotations

from PySide6.QtCore import QObject, Signal

from lux.features.todo.domain import TaskOccurrence
from lux.features.todo.service import TodoService


class TodoController(QObject):
    changed = Signal()  # simple "refresh" signal

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._svc = TodoService()

    # Queries
    def today(self) -> list[TaskOccurrence]:
        return self._svc.list_today()

    def upcoming(self, days: int = 7) -> list[TaskOccurrence]:
        return self._svc.list_upcoming(days=days)

    # Commands
    def add_today(self, title: str) -> None:
        occ_id = self._svc.add_task_for_today(title)
        if occ_id:
            self.changed.emit()

    def set_completed(self, occurrence_id: int, completed: bool) -> None:
        self._svc.set_completed(occurrence_id, completed)
        self.changed.emit()

    def archive(self, occurrence_id: int) -> None:
        self._svc.archive_occurrence(occurrence_id)
        self.changed.emit()

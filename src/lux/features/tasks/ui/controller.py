from __future__ import annotations

from PySide6.QtCore import QObject, Signal

from lux.app.services import SystemServices
from lux.features.tasks.domain import TaskOccurrence
from lux.ui.qt.dragdrop import LuxDragPayload


class TasksController(QObject):
    changed = Signal()  # simple "refresh" signal

    def __init__(self, services: SystemServices, parent=None) -> None:
        super().__init__(parent)
        self._svc = services.tasks_service

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

    # DnD: date-resolving drop only (targets provide a concrete YYYY-MM-DD)
    def handle_drop(self, payload: LuxDragPayload, target_date: str) -> None:
        if payload.kind == "task_occurrence":
            occ_id = int(payload.data.get("occurrence_id", 0) or 0)
            if occ_id > 0:
                self._svc.reschedule_occurrence(occ_id, target_date)
                self.changed.emit()
        elif payload.kind == "task_definition":
            task_id = int(payload.data.get("task_id", 0) or 0)
            if task_id > 0:
                self._svc.create_occurrence_for_date(task_id, target_date)
                self.changed.emit()

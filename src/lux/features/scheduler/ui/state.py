from __future__ import annotations

from PySide6.QtCore import QObject, QDate, Signal


class SchedulerState(QObject):
    """Feature-owned Scheduler UI state.

    Created inside the scheduler feature factory, not held by system navigation.
    """

    date_changed = Signal(QDate)
    data_changed = Signal()

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._selected_date = QDate.currentDate()

    def selected_date(self) -> QDate:
        return self._selected_date

    def set_selected_date(self, qd: QDate) -> None:
        if not isinstance(qd, QDate):
            return
        if qd == self._selected_date:
            return
        self._selected_date = qd
        self.date_changed.emit(qd)

    def notify_data_changed(self) -> None:
        self.data_changed.emit()

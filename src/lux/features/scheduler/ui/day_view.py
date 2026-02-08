from __future__ import annotations

from PySide6.QtCore import Qt, QDate, QTime
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QFrame,
    QDateEdit,
    QScrollArea,
    QDialog,
    QDialogButtonBox,
    QTimeEdit,
    QMessageBox,
)

from lux.core.scheduler.service import SchedulerService
from lux.features.scheduler.ui.controller import SchedulerController, SchedulerEntryVM
from lux.features.scheduler.ui.state import SchedulerState
from lux.ui.qt.widgets.cards import Card
from lux.ui.qt.widgets.buttons import LuxButton


class SchedulerDayView(QWidget):
    """Scheduler Day View (feature-provided).

    Contract:
    - Bounded list for selected date.
    - Reschedule edits start/end times only (same-day only).
    - Archive hides from default list.
    """

    def __init__(self, scheduler_service: SchedulerService, state: SchedulerState, parent=None) -> None:
        super().__init__(parent)

        self._state = state
        self._ctl = SchedulerController(scheduler_service)

        self._state.date_changed.connect(self._on_state_date_changed)  # type: ignore[arg-type]
        self._state.data_changed.connect(self._refresh)  # type: ignore[arg-type]

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(12)

        header = QWidget()
        h = QHBoxLayout(header)
        h.setContentsMargins(0, 0, 0, 0)
        h.setSpacing(10)

        title = QLabel("Schedule")
        title.setObjectName("TitleUnified")
        h.addWidget(title, 0, Qt.AlignVCenter)

        h.addStretch(1)

        self._date = QDateEdit()
        self._date.setCalendarPopup(True)
        self._date.setDate(self._state.selected_date())
        self._date.dateChanged.connect(self._on_date_changed)  # type: ignore[arg-type]
        h.addWidget(self._date, 0)

        root.addWidget(header, 0)

        card = Card()
        c = QVBoxLayout(card)
        c.setContentsMargins(12, 12, 12, 12)
        c.setSpacing(10)

        caption = QLabel("Entries")
        caption.setObjectName("MetaCaption")
        c.addWidget(caption)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)

        self._list_host = QWidget()
        self._list_lay = QVBoxLayout(self._list_host)
        self._list_lay.setContentsMargins(0, 0, 0, 0)
        self._list_lay.setSpacing(8)

        scroll.setWidget(self._list_host)
        c.addWidget(scroll, 1)

        root.addWidget(card, 1)

        self._refresh()

    def _on_date_changed(self, qd: QDate) -> None:
        self._state.set_selected_date(qd)
        self._refresh()

    def _on_state_date_changed(self, qd: QDate) -> None:
        if qd != self._date.date():
            self._date.blockSignals(True)
            try:
                self._date.setDate(qd)
            finally:
                self._date.blockSignals(False)
        self._refresh()

    def _clear_list(self) -> None:
        while self._list_lay.count():
            item = self._list_lay.takeAt(0)
            w = item.widget()
            if w is not None:
                w.deleteLater()

    def _refresh(self) -> None:
        self._clear_list()

        qd = self._state.selected_date()

        try:
            rows = self._ctl.list_entries_for_date(qd)
        except Exception as e:
            err = QLabel(
                "Scheduler failed to load entries.\n\n"
                f"{type(e).__name__}: {e}"
            )
            err.setObjectName("MetaCaption")
            err.setWordWrap(True)
            self._list_lay.addWidget(err)
            self._list_lay.addStretch(1)
            return

        if not rows:
            empty = QLabel("No scheduled entries for this day.")
            empty.setObjectName("MetaCaption")
            empty.setWordWrap(True)
            self._list_lay.addWidget(empty)
            self._list_lay.addStretch(1)
            return

        for vm in rows:
            self._list_lay.addWidget(self._make_row(vm, qd))

        self._list_lay.addStretch(1)

    def _make_row(self, vm: SchedulerEntryVM, qd: QDate) -> QWidget:
        row = QWidget()
        r = QHBoxLayout(row)
        r.setContentsMargins(0, 0, 0, 0)
        r.setSpacing(10)

        time_lbl = QLabel(self._ctl.format_time_range(vm.start_dt, vm.end_dt))
        time_lbl.setObjectName("MetaCaption")
        time_lbl.setMinimumWidth(72)
        r.addWidget(time_lbl, 0)

        title_lbl = QLabel(vm.title)
        title_lbl.setWordWrap(True)
        r.addWidget(title_lbl, 1)

        edit_btn = LuxButton("Edit")
        edit_btn.setMinimumHeight(32)
        edit_btn.clicked.connect(lambda _=False, v=vm: self._edit_time(v, qd))  # type: ignore[arg-type]
        r.addWidget(edit_btn, 0)

        arch_btn = LuxButton("Archive")
        arch_btn.setMinimumHeight(32)
        arch_btn.clicked.connect(lambda _=False, eid=vm.id: self._archive(eid))  # type: ignore[arg-type]
        r.addWidget(arch_btn, 0)

        return row

    def _archive(self, entry_id: int) -> None:
        try:
            self._ctl.archive_entry(entry_id)
            self._state.notify_data_changed()
        except Exception as e:
            QMessageBox.warning(self, "Archive failed", f"{type(e).__name__}: {e}")

    def _edit_time(self, vm: SchedulerEntryVM, qd: QDate) -> None:
        def _parse_time(dt_str: str) -> QTime:
            try:
                t = str(dt_str).replace("T", " ").split(" ")[1][:5]
                hh, mm = t.split(":")
                return QTime(int(hh), int(mm))
            except Exception:
                return QTime(9, 0)

        start_time = _parse_time(vm.start_dt)
        end_time = _parse_time(vm.end_dt)

        dlg = QDialog(self)
        dlg.setWindowTitle("Reschedule")

        lay = QVBoxLayout(dlg)
        lay.setContentsMargins(12, 12, 12, 12)
        lay.setSpacing(10)

        row = QWidget()
        rl = QHBoxLayout(row)
        rl.setContentsMargins(0, 0, 0, 0)
        rl.setSpacing(10)

        rl.addWidget(QLabel("Start"), 0)
        start = QTimeEdit()
        start.setDisplayFormat("HH:mm")
        start.setTime(start_time)
        rl.addWidget(start, 0)

        rl.addWidget(QLabel("End"), 0)
        end = QTimeEdit()
        end.setDisplayFormat("HH:mm")
        end.setTime(end_time)
        rl.addWidget(end, 0)

        rl.addStretch(1)
        lay.addWidget(row)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        lay.addWidget(buttons)

        buttons.accepted.connect(dlg.accept)  # type: ignore[arg-type]
        buttons.rejected.connect(dlg.reject)  # type: ignore[arg-type]

        if dlg.exec() != QDialog.Accepted:
            return

        # Same-day only: edit times only, current date remains.
        if start.time() >= end.time():
            QMessageBox.warning(self, "Invalid time range", "End time must be after start time.")
            return

        try:
            self._ctl.reschedule_entry(vm.id, qd, start.time(), end.time())
            self._state.notify_data_changed()
        except Exception as e:
            QMessageBox.warning(self, "Reschedule failed", f"{type(e).__name__}: {e}")

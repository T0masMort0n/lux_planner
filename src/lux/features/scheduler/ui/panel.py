from __future__ import annotations

from PySide6.QtCore import QDate, QTime
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QCalendarWidget,
    QScrollArea,
    QFrame,
    QLineEdit,
    QTimeEdit,
    QMessageBox,
)

from lux.core.scheduler.service import SchedulerService
from lux.features.scheduler.ui.controller import SchedulerController
from lux.features.scheduler.ui.state import SchedulerState
from lux.ui.qt.widgets.buttons import LuxButton
from lux.ui.qt.widgets.cards import Card


class SchedulerLeftPanel(QWidget):
    """Scheduler Left Content Surface (feature-provided).

    Contract:
    - Date selection updates Day View (via feature-owned SchedulerState).
    - Quick Add writes via SchedulerService only (through controller adapter).
    - No DB operations/imports from UI.
    """

    def __init__(self, scheduler_service: SchedulerService, state: SchedulerState, parent=None) -> None:
        super().__init__(parent)

        self._state = state
        self._ctl = SchedulerController(scheduler_service)

        self._state.date_changed.connect(self._on_state_date_changed)  # type: ignore[arg-type]
        self._state.data_changed.connect(self._refresh_agenda)  # type: ignore[arg-type]

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(12)

        hdr = QLabel("Scheduler")
        hdr.setObjectName("MetaCaption")
        root.addWidget(hdr)

        # Date selector card
        cal_card = Card()
        cal_lay = QVBoxLayout(cal_card)
        cal_lay.setContentsMargins(10, 10, 10, 10)
        cal_lay.setSpacing(10)

        cal_title = QLabel("Jump to date")
        cal_title.setObjectName("MetaCaption")
        cal_lay.addWidget(cal_title)

        self._cal = QCalendarWidget()
        self._cal.setSelectedDate(self._state.selected_date())
        self._cal.selectionChanged.connect(self._on_calendar_changed)  # type: ignore[arg-type]
        cal_lay.addWidget(self._cal)

        root.addWidget(cal_card, 0)

        # Quick Add card
        quick = Card()
        q = QVBoxLayout(quick)
        q.setContentsMargins(10, 10, 10, 10)
        q.setSpacing(10)

        q_title = QLabel("Quick Add")
        q_title.setObjectName("MetaCaption")
        q.addWidget(q_title)

        self._title = QLineEdit()
        self._title.setPlaceholderText("Title…")
        q.addWidget(self._title)

        time_row = QWidget()
        tr = QHBoxLayout(time_row)
        tr.setContentsMargins(0, 0, 0, 0)
        tr.setSpacing(10)

        self._start = QTimeEdit()
        self._start.setDisplayFormat("HH:mm")
        self._start.setTime(QTime.currentTime())
        tr.addWidget(QLabel("Start"), 0)
        tr.addWidget(self._start, 0)

        self._end = QTimeEdit()
        self._end.setDisplayFormat("HH:mm")
        self._end.setTime(QTime.currentTime().addSecs(30 * 60))
        tr.addWidget(QLabel("End"), 0)
        tr.addWidget(self._end, 0)

        tr.addStretch(1)
        q.addWidget(time_row)

        btn_row = QHBoxLayout()
        btn_row.setContentsMargins(0, 0, 0, 0)
        btn_row.setSpacing(10)

        today_btn = LuxButton("Today")
        today_btn.setMinimumHeight(38)
        today_btn.clicked.connect(lambda: self._cal.setSelectedDate(QDate.currentDate()))  # type: ignore[arg-type]
        btn_row.addWidget(today_btn, 1)

        add_btn = LuxButton("Add")
        add_btn.setMinimumHeight(38)
        add_btn.clicked.connect(self._on_add)  # type: ignore[arg-type]
        btn_row.addWidget(add_btn, 1)

        q.addLayout(btn_row)
        root.addWidget(quick, 0)

        # Agenda preview card
        agenda = Card()
        ag = QVBoxLayout(agenda)
        ag.setContentsMargins(10, 10, 10, 10)
        ag.setSpacing(10)

        ag_title = QLabel("Up next")
        ag_title.setObjectName("MetaCaption")
        ag.addWidget(ag_title)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)

        self._agenda_host = QWidget()
        self._agenda_lay = QVBoxLayout(self._agenda_host)
        self._agenda_lay.setContentsMargins(0, 0, 0, 0)
        self._agenda_lay.setSpacing(10)

        scroll.setWidget(self._agenda_host)
        ag.addWidget(scroll, 1)

        root.addWidget(agenda, 1)

        self._refresh_agenda()

    def _on_calendar_changed(self) -> None:
        self._state.set_selected_date(self._cal.selectedDate())
        self._refresh_agenda()

    def _on_state_date_changed(self, qd: QDate) -> None:
        if qd != self._cal.selectedDate():
            self._cal.blockSignals(True)
            try:
                self._cal.setSelectedDate(qd)
            finally:
                self._cal.blockSignals(False)
        self._refresh_agenda()

    def _on_add(self) -> None:
        qd = self._state.selected_date()
        title = (self._title.text() or "").strip()
        if not title:
            QMessageBox.information(self, "Missing title", "Please enter a title.")
            return

        if self._start.time() >= self._end.time():
            QMessageBox.information(self, "Invalid time range", "End time must be after start time.")
            return

        try:
            self._ctl.create_adhoc(qd, title, self._start.time(), self._end.time())
            self._title.setText("")
            self._state.notify_data_changed()
        except Exception as e:
            QMessageBox.warning(self, "Create failed", f"{type(e).__name__}: {e}")

    def _refresh_agenda(self) -> None:
        while self._agenda_lay.count():
            item = self._agenda_lay.takeAt(0)
            w = item.widget()
            if w is not None:
                w.deleteLater()

        try:
            vms = self._ctl.list_entries_for_date(self._state.selected_date())
        except Exception as e:
            err = QLabel(
                "Scheduler failed to load agenda.\n\n"
                f"{type(e).__name__}: {e}"
            )
            err.setObjectName("MetaCaption")
            err.setWordWrap(True)
            self._agenda_lay.addWidget(err)
            self._agenda_lay.addStretch(1)
            return

        if not vms:
            lbl = QLabel("Nothing scheduled for this day.")
            lbl.setObjectName("MetaCaption")
            lbl.setWordWrap(True)
            self._agenda_lay.addWidget(lbl)
            self._agenda_lay.addStretch(1)
            return

        for vm in vms[:12]:
            t = self._ctl.format_time_range(vm.start_dt, vm.end_dt)
            txt = f"{t} · {vm.title}" if t else vm.title
            lbl = QLabel(txt)
            lbl.setWordWrap(True)
            self._agenda_lay.addWidget(lbl)

        self._agenda_lay.addStretch(1)

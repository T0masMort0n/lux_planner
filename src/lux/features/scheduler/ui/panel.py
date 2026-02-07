from __future__ import annotations

from PySide6.QtCore import QDate
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QCalendarWidget,
    QScrollArea,
    QFrame,
)

from lux.core.scheduler.service import SchedulerService
from lux.features.scheduler.ui.controller import SchedulerController
from lux.ui.qt.widgets.buttons import LuxButton
from lux.ui.qt.widgets.cards import Card


class SchedulerLeftPanel(QWidget):
    """
    Left panel is intentionally “supporting UI” only.
    It does NOT control right-side switching (AppModuleSpec creates them separately).
    """

    def __init__(self, scheduler_service, parent=None) -> None:
        super().__init__(parent)

        # Injected system service; UI never creates DB-backed services.
        self._ctl = SchedulerController(scheduler_service)

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(12)

        hdr = QLabel("Scheduler")
        hdr.setObjectName("MetaCaption")
        root.addWidget(hdr)

        # Mini calendar card
        cal_card = Card()
        cal_lay = QVBoxLayout(cal_card)
        cal_lay.setContentsMargins(10, 10, 10, 10)
        cal_lay.setSpacing(10)

        cal_title = QLabel("Jump to date")
        cal_title.setObjectName("MetaCaption")
        cal_lay.addWidget(cal_title)

        self._cal = QCalendarWidget()
        self._cal.setSelectedDate(QDate.currentDate())
        self._cal.selectionChanged.connect(self._refresh_agenda)  # type: ignore[arg-type]
        cal_lay.addWidget(self._cal)

        root.addWidget(cal_card, 0)

        # Quick actions (placeholders only in Phase 0)
        actions = Card()
        a = QVBoxLayout(actions)
        a.setContentsMargins(10, 10, 10, 10)
        a.setSpacing(10)

        row = QHBoxLayout()
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(10)

        today_btn = LuxButton("Today")
        today_btn.setMinimumHeight(38)
        today_btn.clicked.connect(lambda: self._cal.setSelectedDate(QDate.currentDate()))  # type: ignore[arg-type]
        row.addWidget(today_btn, 1)

        new_btn = LuxButton("New Event")
        new_btn.setMinimumHeight(38)
        new_btn.setEnabled(False)  # Phase 0: no create UI
        row.addWidget(new_btn, 1)

        a.addLayout(row)

        for name in ["Day", "Week", "Month", "Task Assignment"]:
            b = LuxButton(name)
            b.setMinimumHeight(38)
            b.setEnabled(False)
            a.addWidget(b)

        root.addWidget(actions, 0)

        # Agenda preview (reads from SchedulerService via controller)
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

    def _refresh_agenda(self) -> None:
        while self._agenda_lay.count():
            item = self._agenda_lay.takeAt(0)
            w = item.widget()
            if w is not None:
                w.deleteLater()

        try:
            rows = self._ctl.list_entries_for_date(self._cal.selectedDate())
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

        if not rows:
            lbl = QLabel("Nothing scheduled for this day.")
            lbl.setObjectName("MetaCaption")
            lbl.setWordWrap(True)
            self._agenda_lay.addWidget(lbl)
            self._agenda_lay.addStretch(1)
            return

        for txt in rows[:12]:
            lbl = QLabel(txt)
            lbl.setWordWrap(True)
            self._agenda_lay.addWidget(lbl)

        self._agenda_lay.addStretch(1)
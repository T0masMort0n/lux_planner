from __future__ import annotations

from PySide6.QtCore import Qt, QDate
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QDateEdit, QScrollArea

from lux.core.scheduler.service import SchedulerService
from lux.features.scheduler.ui.controller import SchedulerController
from lux.ui.qt.widgets.cards import Card
from lux.ui.qt.widgets.buttons import LuxButton


class SchedulerDayView(QWidget):
    """
    Minimal, system-compliant Scheduler surface (Phase 0):
    - UI reads scheduled entries via SchedulerController (service -> repo -> DB).
    - No DB imports in UI.
    - No scheduling logic in UI (creation/reschedule handled by service layer only).
    """

    def __init__(self, scheduler_service, parent=None) -> None:
        super().__init__(parent)

        # Injected system service; UI never creates DB-backed services.
        self._ctl = SchedulerController(scheduler_service)

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(12)

        # Header
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
        self._date.setDate(QDate.currentDate())
        self._date.dateChanged.connect(self._refresh)  # type: ignore[arg-type]
        h.addWidget(self._date, 0)

        # Placeholder controls (no view switching logic in Phase 0)
        for txt in ["Day", "Week", "Month"]:
            b = LuxButton(txt)
            b.setMinimumHeight(36)
            b.setEnabled(False)
            h.addWidget(b, 0)

        root.addWidget(header, 0)

        # Entries list
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

    def _refresh(self) -> None:
        # Clear existing rows
        while self._list_lay.count():
            item = self._list_lay.takeAt(0)
            w = item.widget()
            if w is not None:
                w.deleteLater()

        qd = self._date.date()

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

        for line in rows:
            lbl = QLabel(line)
            lbl.setWordWrap(True)
            self._list_lay.addWidget(lbl)

        self._list_lay.addStretch(1)

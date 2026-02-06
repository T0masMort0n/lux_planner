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

from lux.ui.qt.widgets.buttons import LuxButton
from lux.ui.qt.widgets.cards import Card


class SchedulerLeftPanel(QWidget):
    """
    Left panel is intentionally “supporting UI” only.
    It does NOT control right-side switching (AppModuleSpec creates them separately).
    """

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

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

        cal = QCalendarWidget()
        cal.setSelectedDate(QDate.currentDate())
        cal_lay.addWidget(cal)

        root.addWidget(cal_card, 0)

        # Quick actions
        actions = Card()
        a = QVBoxLayout(actions)
        a.setContentsMargins(10, 10, 10, 10)
        a.setSpacing(10)

        row = QHBoxLayout()
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(10)

        today_btn = LuxButton("Today")
        today_btn.setMinimumHeight(38)
        row.addWidget(today_btn, 1)

        new_btn = LuxButton("New Event")
        new_btn.setMinimumHeight(38)
        row.addWidget(new_btn, 1)

        a.addLayout(row)

        for name in ["Day", "Week", "Month", "Task Assignment"]:
            b = LuxButton(name)
            b.setMinimumHeight(38)
            a.addWidget(b)

        root.addWidget(actions, 0)

        # Agenda preview (placeholder list)
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

        host = QWidget()
        hl = QVBoxLayout(host)
        hl.setContentsMargins(0, 0, 0, 0)
        hl.setSpacing(10)

        for txt in ["Standup · 10:00 AM", "Lunch · 1:00 PM", "Project Block · 3:00 PM"]:
            lbl = QLabel(txt)
            lbl.setWordWrap(True)
            hl.addWidget(lbl)

        hl.addStretch(1)

        scroll.setWidget(host)
        ag.addWidget(scroll, 1)

        root.addWidget(agenda, 1)

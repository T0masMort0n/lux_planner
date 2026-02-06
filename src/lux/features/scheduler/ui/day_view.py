from __future__ import annotations

from dataclasses import dataclass

from PySide6.QtCore import Qt, QDate
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QScrollArea,
    QFrame,
    QToolButton,
    QDateEdit,
    QSizePolicy,
)

from lux.ui.qt.widgets.cards import Card
from lux.ui.qt.widgets.buttons import LuxButton


@dataclass(frozen=True)
class _SampleEvent:
    start_hour: int
    title: str
    meta: str


class _TimeRow(QWidget):
    """
    One hour row: left time label + right lane container.
    We keep visuals minimal; QSS/theme handles global look.
    """

    def __init__(self, hour_24: int, parent=None) -> None:
        super().__init__(parent)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setMinimumHeight(64)

        root = QHBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(12)

        self.time_lbl = QLabel(self._fmt_hour(hour_24))
        self.time_lbl.setObjectName("MetaCaption")
        self.time_lbl.setAlignment(Qt.AlignRight | Qt.AlignTop)
        self.time_lbl.setFixedWidth(70)
        root.addWidget(self.time_lbl, 0)

        self.lane = QWidget()
        lane_lay = QVBoxLayout(self.lane)
        lane_lay.setContentsMargins(0, 0, 0, 0)
        lane_lay.setSpacing(8)

        # Subtle separator (no custom colors)
        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setFrameShadow(QFrame.Sunken)

        lane_lay.addStretch(1)
        lane_lay.addWidget(sep, 0)

        root.addWidget(self.lane, 1)

    @staticmethod
    def _fmt_hour(hour_24: int) -> str:
        if hour_24 == 0:
            return "12 AM"
        if hour_24 < 12:
            return f"{hour_24} AM"
        if hour_24 == 12:
            return "12 PM"
        return f"{hour_24 - 12} PM"


class _DayGrid(QWidget):
    """
    Scrollable day grid from START_HOUR..END_HOUR.
    Events are simple Card blocks placed inside their start-hour row.
    """

    START_HOUR = 4
    END_HOUR = 18  # inclusive label, last visible hour line at 6 PM

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self._rows: dict[int, _TimeRow] = {}

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(10)

        # Build rows
        for h in range(self.START_HOUR, self.END_HOUR + 1):
            row = _TimeRow(h)
            self._rows[h] = row
            root.addWidget(row)

        root.addStretch(1)

        self._seed_sample_events()

    def _seed_sample_events(self) -> None:
        # Non-functional sample data to make the layout feel “real”
        sample = [
            _SampleEvent(8, "Deep Work", "Focus · 90m"),
            _SampleEvent(10, "Standup", "Team · 15m"),
            _SampleEvent(13, "Lunch", "Personal · 45m"),
            _SampleEvent(15, "Project Block", "Scheduler wiring later"),
        ]
        for ev in sample:
            self._add_event_card(ev)

    def _add_event_card(self, ev: _SampleEvent) -> None:
        row = self._rows.get(ev.start_hour)
        if row is None:
            return

        card = Card()
        lay = QVBoxLayout(card)
        lay.setContentsMargins(12, 10, 12, 10)
        lay.setSpacing(4)

        title = QLabel(ev.title)
        title.setObjectName("TitleUnified")
        lay.addWidget(title)

        meta = QLabel(ev.meta)
        meta.setObjectName("MetaCaption")
        meta.setWordWrap(True)
        lay.addWidget(meta)

        # Place near top of the hour lane (above the separator)
        lane_lay: QVBoxLayout = row.lane.layout()  # type: ignore[assignment]
        lane_lay.insertWidget(0, card)


class SchedulerDayView(QWidget):
    """
    Day view UI only:
    - top header with date + view buttons (non-functional placeholders)
    - scrollable day grid
    """

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

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
        h.addWidget(self._date, 0)

        # Lightweight controls (kept local to this view; no cross-feature nav)
        for txt in ["Day", "Week", "Month"]:
            b = LuxButton(txt)
            b.setMinimumHeight(36)
            h.addWidget(b, 0)

        new_btn = QToolButton()
        new_btn.setAutoRaise(True)
        new_btn.setCursor(Qt.PointingHandCursor)
        new_btn.setText("＋ New")
        h.addWidget(new_btn, 0)

        root.addWidget(header, 0)

        # Grid container card
        grid_card = Card()
        grid_lay = QVBoxLayout(grid_card)
        grid_lay.setContentsMargins(12, 12, 12, 12)
        grid_lay.setSpacing(10)

        caption = QLabel("Today")
        caption.setObjectName("MetaCaption")
        grid_lay.addWidget(caption)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)

        grid = _DayGrid()
        scroll.setWidget(grid)

        grid_lay.addWidget(scroll, 1)

        root.addWidget(grid_card, 1)

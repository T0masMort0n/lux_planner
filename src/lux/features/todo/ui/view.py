from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QHBoxLayout,
    QCheckBox,
    QFrame,
    QScrollArea,
)

from lux.ui.qt.widgets.buttons import LuxButton
from lux.ui.qt.widgets.cards import Card
from lux.features.todo.ui.controller import TodoController


class TodoRightView(QWidget):
    """
    Dashboard-style To Do view.
    Uses TodoController for data (today + upcoming) but keeps everything else as placeholders.
    """

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self._ctl = TodoController(self)
        self._ctl.changed.connect(self._refresh)

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(12)

        header_row = QHBoxLayout()
        header_row.setContentsMargins(0, 0, 0, 0)
        header_row.setSpacing(10)

        title = QLabel("To Do")
        title.setObjectName("TitleUnified")
        title.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        header_row.addWidget(title, 1)

        new_btn = LuxButton("New task")
        new_btn.setMinimumHeight(40)
        header_row.addWidget(new_btn, 0)

        focus_btn = LuxButton("Focus mode")
        focus_btn.setMinimumHeight(40)
        header_row.addWidget(focus_btn, 0)

        root.addLayout(header_row)

        self._scroll = QScrollArea()
        self._scroll.setWidgetResizable(True)
        self._scroll.setFrameShape(QFrame.NoFrame)

        self._host = QWidget()
        self._lay = QVBoxLayout(self._host)
        self._lay.setContentsMargins(0, 0, 0, 0)
        self._lay.setSpacing(12)

        self._scroll.setWidget(self._host)
        root.addWidget(self._scroll, 1)

        self._refresh()

    def _refresh(self) -> None:
        while self._lay.count():
            item = self._lay.takeAt(0)
            w = item.widget()
            if w is not None:
                w.setParent(None)
                w.deleteLater()

        # Today card
        today_card = Card()
        t_lay = QVBoxLayout(today_card)
        t_lay.setContentsMargins(14, 14, 14, 14)
        t_lay.setSpacing(10)

        today_lbl = QLabel("Today")
        today_lbl.setObjectName("MetaCaption")
        t_lay.addWidget(today_lbl)

        today = self._ctl.today()
        if not today:
            e = QLabel("Nothing scheduled for today.")
            e.setObjectName("MetaCaption")
            t_lay.addWidget(e)
        else:
            for occ in today:
                row = QWidget()
                r = QHBoxLayout(row)
                r.setContentsMargins(0, 0, 0, 0)
                r.setSpacing(10)

                chk = QCheckBox()
                chk.setChecked(occ.completed)
                chk.stateChanged.connect(
                    lambda state, oid=occ.id: self._ctl.set_completed(oid, state == Qt.Checked)
                )
                r.addWidget(chk, 0, Qt.AlignTop)

                lbl = QLabel(occ.title)
                lbl.setWordWrap(True)
                r.addWidget(lbl, 1)

                t_lay.addWidget(row)

        self._lay.addWidget(today_card)

        # Upcoming card
        up_card = Card()
        u_lay = QVBoxLayout(up_card)
        u_lay.setContentsMargins(14, 14, 14, 14)
        u_lay.setSpacing(10)

        upcoming_lbl = QLabel("Upcoming (7 days)")
        upcoming_lbl.setObjectName("MetaCaption")
        u_lay.addWidget(upcoming_lbl)

        upcoming = self._ctl.upcoming(7)
        if not upcoming:
            e2 = QLabel("No upcoming tasks.")
            e2.setObjectName("MetaCaption")
            u_lay.addWidget(e2)
        else:
            for occ in upcoming:
                lbl = QLabel(f"{occ.due_date} — {occ.title}")
                lbl.setWordWrap(True)
                u_lay.addWidget(lbl)

        actions = QHBoxLayout()
        actions.setContentsMargins(0, 0, 0, 0)
        actions.setSpacing(10)
        actions.addStretch(1)

        sched = LuxButton("Open scheduler")
        sched.setMinimumHeight(38)
        actions.addWidget(sched)

        review = LuxButton("Weekly review")
        review.setMinimumHeight(38)
        actions.addWidget(review)

        u_lay.addLayout(actions)
        self._lay.addWidget(up_card)

        # Placeholder: details panel hint
        hint_card = Card()
        h_lay = QVBoxLayout(hint_card)
        h_lay.setContentsMargins(14, 14, 14, 14)
        h_lay.setSpacing(6)

        h_title = QLabel("Details (placeholder)")
        h_title.setObjectName("MetaCaption")
        h_lay.addWidget(h_title)

        hint = QLabel("Later: selecting a task will show notes, subtasks, and history here.")
        hint.setWordWrap(True)
        hint.setObjectName("MetaCaption")
        h_lay.addWidget(hint)

        self._lay.addWidget(hint_card)

        self._lay.addStretch(1)

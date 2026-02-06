from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QHBoxLayout,
    QComboBox,
    QScrollArea,
    QFrame,
    QGridLayout,
    QProgressBar,
    QLineEdit,
)

from lux.ui.qt.widgets.buttons import LuxButton
from lux.ui.qt.widgets.cards import Card


class GoalsRightView(QWidget):
    """
    Sample Goals UI:
    - active goals list with progress
    - milestones + daily check-in placeholders
    - all wiring deferred (non-functional widgets are OK here)
    """

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(12)

        header_row = QHBoxLayout()
        header_row.setContentsMargins(0, 0, 0, 0)
        header_row.setSpacing(10)

        title = QLabel("Goals")
        title.setObjectName("TitleUnified")
        title.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        header_row.addWidget(title, 1)

        scope = QComboBox()
        scope.addItems(["All", "Personal", "Work", "Health"])
        header_row.addWidget(scope, 0)

        new_btn = LuxButton("New goal")
        new_btn.setMinimumHeight(40)
        header_row.addWidget(new_btn, 0)

        root.addLayout(header_row)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)

        host = QWidget()
        lay = QVBoxLayout(host)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(12)

        # Card: Active goals
        active = Card()
        a_lay = QVBoxLayout(active)
        a_lay.setContentsMargins(14, 14, 14, 14)
        a_lay.setSpacing(12)

        a_title = QLabel("Active Goals")
        a_title.setObjectName("MetaCaption")
        a_lay.addWidget(a_title)

        for name, pct, note in [
            ("Run 10 km without stopping", 35, "Next: easy 20 min run"),
            ("Read 24 books this year", 50, "Currently: 12/24"),
            ("Lift 3x / week", 60, "Streak: 2 weeks"),
        ]:
            row = QWidget()
            r = QVBoxLayout(row)
            r.setContentsMargins(0, 0, 0, 0)
            r.setSpacing(6)

            top = QHBoxLayout()
            top.setContentsMargins(0, 0, 0, 0)
            top.setSpacing(10)

            lbl = QLabel(name)
            lbl.setWordWrap(True)
            top.addWidget(lbl, 1)

            edit = LuxButton("Edit")
            edit.setMinimumHeight(34)
            top.addWidget(edit, 0)

            r.addLayout(top)

            pb = QProgressBar()
            pb.setRange(0, 100)
            pb.setValue(int(pct))
            pb.setTextVisible(True)
            pb.setFormat("%p%")
            r.addWidget(pb)

            meta = QLabel(note)
            meta.setObjectName("MetaCaption")
            meta.setWordWrap(True)
            r.addWidget(meta)

            a_lay.addWidget(row)

        lay.addWidget(active)

        # Card: Milestones (placeholder)
        miles = Card()
        m_lay = QVBoxLayout(miles)
        m_lay.setContentsMargins(14, 14, 14, 14)
        m_lay.setSpacing(10)

        m_title = QLabel("Milestones (placeholder)")
        m_title.setObjectName("MetaCaption")
        m_lay.addWidget(m_title)

        grid = QGridLayout()
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setHorizontalSpacing(14)
        grid.setVerticalSpacing(8)

        data = [
            ("This week", "2 / 5"),
            ("This month", "7 / 12"),
            ("This quarter", "—"),
        ]
        for r, (k, v) in enumerate(data):
            k_lbl = QLabel(k)
            k_lbl.setObjectName("MetaCaption")
            v_lbl = QLabel(v)
            grid.addWidget(k_lbl, r, 0)
            grid.addWidget(v_lbl, r, 1)

        m_lay.addLayout(grid)

        row2 = QHBoxLayout()
        row2.setContentsMargins(0, 0, 0, 0)
        row2.setSpacing(10)
        row2.addStretch(1)

        add_m = LuxButton("Add milestone")
        add_m.setMinimumHeight(38)
        row2.addWidget(add_m)

        m_lay.addLayout(row2)
        lay.addWidget(miles)

        # Card: Daily check-in
        check = Card()
        c_lay = QVBoxLayout(check)
        c_lay.setContentsMargins(14, 14, 14, 14)
        c_lay.setSpacing(10)

        c_title = QLabel("Daily Check-in")
        c_title.setObjectName("MetaCaption")
        c_lay.addWidget(c_title)

        prompt = QLabel("What is the one thing you'll do today that moves the needle?")
        prompt.setWordWrap(True)
        prompt.setObjectName("MetaCaption")
        c_lay.addWidget(prompt)

        self._checkin = QLineEdit()
        self._checkin.setPlaceholderText("Type your commit…")
        c_lay.addWidget(self._checkin)

        btn_row = QHBoxLayout()
        btn_row.setContentsMargins(0, 0, 0, 0)
        btn_row.setSpacing(10)
        btn_row.addStretch(1)

        save = LuxButton("Save")
        save.setMinimumHeight(38)
        btn_row.addWidget(save)

        c_lay.addLayout(btn_row)
        lay.addWidget(check)

        lay.addStretch(1)
        scroll.setWidget(host)
        root.addWidget(scroll, 1)

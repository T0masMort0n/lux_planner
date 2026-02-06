from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QHBoxLayout,
    QComboBox,
    QLineEdit,
    QGridLayout,
    QProgressBar,
    QScrollArea,
    QFrame,
)

from lux.ui.qt.widgets.buttons import LuxButton
from lux.ui.qt.widgets.cards import Card


class ExerciseRightView(QWidget):
    """
    Sample Exercise UI:
    - calm, dark, system-themed by QSS
    - feature provides content only (no navigation/motion systems)
    - buttons are placeholders for later wiring by services/controllers
    """

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(12)

        # Header
        header_row = QHBoxLayout()
        header_row.setContentsMargins(0, 0, 0, 0)
        header_row.setSpacing(10)

        title = QLabel("Exercise")
        title.setObjectName("TitleUnified")
        title.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        header_row.addWidget(title, 1)

        self._date = QComboBox()
        self._date.addItems(["Today", "Yesterday", "This week"])
        header_row.addWidget(self._date, 0)

        start_btn = LuxButton("Start workout")
        start_btn.setMinimumHeight(40)
        header_row.addWidget(start_btn, 0)

        root.addLayout(header_row)

        # Scrollable content
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)

        host = QWidget()
        lay = QVBoxLayout(host)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(12)

        # Card: Today's plan
        plan = Card()
        plan_lay = QVBoxLayout(plan)
        plan_lay.setContentsMargins(14, 14, 14, 14)
        plan_lay.setSpacing(10)

        plan_title = QLabel("Today's Plan")
        plan_title.setObjectName("MetaCaption")
        plan_lay.addWidget(plan_title)

        for line in [
            "Warmup — 5–10 min (walk, row, bike)",
            "Main — Upper A (Bench / Row / OHP)",
            "Accessory — Arms + Core",
        ]:
            lbl = QLabel("• " + line)
            lbl.setWordWrap(True)
            plan_lay.addWidget(lbl)

        plan_actions = QHBoxLayout()
        plan_actions.setContentsMargins(0, 0, 0, 0)
        plan_actions.setSpacing(10)
        plan_actions.addStretch(1)

        edit_btn = LuxButton("Edit plan")
        edit_btn.setMinimumHeight(38)
        plan_actions.addWidget(edit_btn)

        template_btn = LuxButton("Save as template")
        template_btn.setMinimumHeight(38)
        plan_actions.addWidget(template_btn)

        plan_lay.addLayout(plan_actions)
        lay.addWidget(plan)

        # Card: Quick log
        ql = Card()
        ql_lay = QVBoxLayout(ql)
        ql_lay.setContentsMargins(14, 14, 14, 14)
        ql_lay.setSpacing(10)

        ql_title = QLabel("Quick Log")
        ql_title.setObjectName("MetaCaption")
        ql_lay.addWidget(ql_title)

        hint = QLabel('Log a set in one line: "Bench 135 x 8" or "Run 2.1 mi".')
        hint.setWordWrap(True)
        hint.setObjectName("MetaCaption")
        ql_lay.addWidget(hint)

        log_row = QHBoxLayout()
        log_row.setContentsMargins(0, 0, 0, 0)
        log_row.setSpacing(10)

        self._log = QLineEdit()
        self._log.setPlaceholderText("Type here…")
        log_row.addWidget(self._log, 1)

        add_btn = LuxButton("Add")
        add_btn.setMinimumHeight(38)
        log_row.addWidget(add_btn, 0)

        ql_lay.addLayout(log_row)
        lay.addWidget(ql)

        # Card: Metrics (placeholder)
        metrics = Card()
        m_lay = QVBoxLayout(metrics)
        m_lay.setContentsMargins(14, 14, 14, 14)
        m_lay.setSpacing(10)

        m_title = QLabel("Metrics (placeholder)")
        m_title.setObjectName("MetaCaption")
        m_lay.addWidget(m_title)

        grid = QGridLayout()
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setHorizontalSpacing(14)
        grid.setVerticalSpacing(10)

        pairs = [
            ("Training streak", "3 days"),
            ("Last workout", "Upper A"),
            ("Sleep", "—"),
            ("Calories", "—"),
        ]
        for r, (k, v) in enumerate(pairs):
            k_lbl = QLabel(k)
            k_lbl.setObjectName("MetaCaption")
            v_lbl = QLabel(v)
            grid.addWidget(k_lbl, r, 0)
            grid.addWidget(v_lbl, r, 1)

        m_lay.addLayout(grid)

        pb = QProgressBar()
        pb.setRange(0, 100)
        pb.setValue(42)
        pb.setTextVisible(True)
        pb.setFormat("Weekly progress — %p%")
        m_lay.addWidget(pb)

        lay.addWidget(metrics)

        lay.addStretch(1)
        scroll.setWidget(host)
        root.addWidget(scroll, 1)

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QLineEdit

from lux.ui.qt.widgets.buttons import LuxButton
from lux.ui.qt.widgets.cards import Card


class ExerciseLeftPanel(QWidget):
    """
    Feature left panel content only.
    No navigation, no animations, no cross-feature imports.
    """

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(12)

        header_row = QHBoxLayout()
        header_row.setContentsMargins(0, 0, 0, 0)
        header_row.setSpacing(10)

        header = QLabel("Exercise")
        header.setObjectName("MetaCaption")
        header_row.addWidget(header, 1, Qt.AlignVCenter)

        quick = LuxButton("Quick log")
        quick.setMinimumHeight(36)
        header_row.addWidget(quick, 0)

        root.addLayout(header_row)

        # Quick search / filter (non-functional placeholder)
        self._search = QLineEdit()
        self._search.setPlaceholderText("Search workouts, movements, templates…")
        root.addWidget(self._search)

        # Sections
        nav_card = Card()
        nav_lay = QVBoxLayout(nav_card)
        nav_lay.setContentsMargins(12, 12, 12, 12)
        nav_lay.setSpacing(8)

        for label in ["Today", "Plan", "Programs", "History"]:
            b = LuxButton(label)
            b.setMinimumHeight(42)
            nav_lay.addWidget(b)

        root.addWidget(nav_card)

        # Small “suggestion” area (non-functional)
        tip_card = Card()
        tip_lay = QVBoxLayout(tip_card)
        tip_lay.setContentsMargins(12, 12, 12, 12)
        tip_lay.setSpacing(6)

        tip_title = QLabel("Suggestion")
        tip_title.setObjectName("MetaCaption")
        tip_lay.addWidget(tip_title)

        tip = QLabel("Keep it simple: pick a template, hit start, log sets as you go.")
        tip.setWordWrap(True)
        tip.setObjectName("MetaCaption")
        tip_lay.addWidget(tip)

        root.addWidget(tip_card)
        root.addStretch(1)

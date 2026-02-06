from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QLineEdit

from lux.ui.qt.widgets.buttons import LuxButton
from lux.ui.qt.widgets.cards import Card


class GoalsLeftPanel(QWidget):
    """
    Feature left panel content only.
    No navigation logic or cross-feature dependencies.
    """

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(12)

        header_row = QHBoxLayout()
        header_row.setContentsMargins(0, 0, 0, 0)
        header_row.setSpacing(10)

        header = QLabel("Goals")
        header.setObjectName("MetaCaption")
        header_row.addWidget(header, 1, Qt.AlignVCenter)

        new_btn = LuxButton("New goal")
        new_btn.setMinimumHeight(36)
        header_row.addWidget(new_btn, 0)

        root.addLayout(header_row)

        self._search = QLineEdit()
        self._search.setPlaceholderText("Search goals, milestones, habits…")
        root.addWidget(self._search)

        nav_card = Card()
        nav_lay = QVBoxLayout(nav_card)
        nav_lay.setContentsMargins(12, 12, 12, 12)
        nav_lay.setSpacing(8)

        for label in ["Overview", "Goals", "Milestones", "Habits", "Archives"]:
            b = LuxButton(label)
            b.setMinimumHeight(42)
            nav_lay.addWidget(b)

        root.addWidget(nav_card)

        focus_card = Card()
        focus_lay = QVBoxLayout(focus_card)
        focus_lay.setContentsMargins(12, 12, 12, 12)
        focus_lay.setSpacing(6)

        focus_title = QLabel("Focus")
        focus_title.setObjectName("MetaCaption")
        focus_lay.addWidget(focus_title)

        focus = QLabel("Pick 1–3 active goals. Everything else is supporting cast.")
        focus.setWordWrap(True)
        focus.setObjectName("MetaCaption")
        focus_lay.addWidget(focus)

        root.addWidget(focus_card)
        root.addStretch(1)

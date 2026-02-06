from __future__ import annotations

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
)

from lux.ui.qt.widgets.buttons import LuxButton
from lux.ui.qt.widgets.cards import Card


class MealsLeftPanel(QWidget):
    """
    Left rail for Meals: mode buttons + quick recipe search + pinned recipes list (UI only).
    """

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(12)

        hdr = QLabel("Meals")
        hdr.setObjectName("MetaCaption")
        root.addWidget(hdr)

        modes = Card()
        m = QVBoxLayout(modes)
        m.setContentsMargins(10, 10, 10, 10)
        m.setSpacing(10)

        for name in ["Meal Plan", "Recipes", "Shopping List"]:
            b = LuxButton(name)
            b.setMinimumHeight(40)
            m.addWidget(b)

        root.addWidget(modes, 0)

        self._search = QLineEdit()
        self._search.setPlaceholderText("Search recipes…")
        root.addWidget(self._search, 0)

        pinned = Card()
        p = QVBoxLayout(pinned)
        p.setContentsMargins(10, 10, 10, 10)
        p.setSpacing(10)

        cap = QLabel("Pinned")
        cap.setObjectName("MetaCaption")
        p.addWidget(cap)

        self._list = QListWidget()
        self._list.setUniformItemSizes(True)

        for name in ["Chicken Bowl", "Overnight Oats", "Taco Night", "Salmon + Rice"]:
            self._list.addItem(QListWidgetItem(name))

        p.addWidget(self._list, 1)

        btn_row = QHBoxLayout()
        btn_row.setContentsMargins(0, 0, 0, 0)
        btn_row.setSpacing(10)

        new_recipe = LuxButton("New Recipe")
        new_recipe.setMinimumHeight(38)
        btn_row.addWidget(new_recipe, 1)

        import_btn = LuxButton("Import")
        import_btn.setMinimumHeight(38)
        btn_row.addWidget(import_btn, 1)

        p.addLayout(btn_row)

        root.addWidget(pinned, 1)

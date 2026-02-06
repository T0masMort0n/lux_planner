from __future__ import annotations

from PySide6.QtCore import Qt, QDate
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QLineEdit,
    QGridLayout,
    QScrollArea,
    QFrame,
    QSplitter,
    QToolButton,
    QDateEdit,
)

from lux.ui.qt.widgets.cards import Card
from lux.ui.qt.widgets.buttons import LuxButton


class _MealDayCard(Card):
    def __init__(self, day_name: str, date_str: str, parent=None) -> None:
        super().__init__(parent)

        lay = QVBoxLayout(self)
        lay.setContentsMargins(12, 12, 12, 12)
        lay.setSpacing(8)

        top = QHBoxLayout()
        top.setContentsMargins(0, 0, 0, 0)
        top.setSpacing(10)

        title = QLabel(day_name)
        title.setObjectName("TitleUnified")
        top.addWidget(title, 0)

        top.addStretch(1)

        meta = QLabel(date_str)
        meta.setObjectName("MetaCaption")
        top.addWidget(meta, 0)

        lay.addLayout(top)

        for slot in ["Breakfast", "Lunch", "Dinner"]:
            row = QHBoxLayout()
            row.setContentsMargins(0, 0, 0, 0)
            row.setSpacing(10)

            lbl = QLabel(f"{slot}")
            lbl.setObjectName("MetaCaption")
            row.addWidget(lbl, 0)

            add = QToolButton()
            add.setAutoRaise(True)
            add.setCursor(Qt.PointingHandCursor)
            add.setText("＋")
            row.addStretch(1)
            row.addWidget(add, 0)

            lay.addLayout(row)

            item = QLabel("—")
            item.setWordWrap(True)
            lay.addWidget(item)

        lay.addStretch(1)


class MealsRightView(QWidget):
    """
    Meals UI sample:
    - Left sub-pane: recipe library (within feature)
    - Right: weekly plan grid + shopping preview
    No real data wiring yet.
    """

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(12)

        header = QWidget()
        h = QHBoxLayout(header)
        h.setContentsMargins(0, 0, 0, 0)
        h.setSpacing(10)

        title = QLabel("Meal Plan")
        title.setObjectName("TitleUnified")
        h.addWidget(title, 0)

        h.addStretch(1)

        week_lbl = QLabel("Week of")
        week_lbl.setObjectName("MetaCaption")
        h.addWidget(week_lbl, 0)

        week = QDateEdit()
        week.setCalendarPopup(True)
        week.setDate(QDate.currentDate())
        h.addWidget(week, 0)

        gen = LuxButton("Generate")
        gen.setMinimumHeight(36)
        h.addWidget(gen, 0)

        root.addWidget(header, 0)

        splitter = QSplitter(Qt.Horizontal)
        splitter.setChildrenCollapsible(False)

        # Recipe library
        lib = Card()
        ll = QVBoxLayout(lib)
        ll.setContentsMargins(12, 12, 12, 12)
        ll.setSpacing(10)

        lib_title = QLabel("Recipes")
        lib_title.setObjectName("TitleUnified")
        ll.addWidget(lib_title)

        search = QLineEdit()
        search.setPlaceholderText("Find a recipe…")
        ll.addWidget(search)

        chips = QHBoxLayout()
        chips.setContentsMargins(0, 0, 0, 0)
        chips.setSpacing(10)

        for c in ["Quick", "High Protein", "Comfort", "Vegetarian"]:
            b = LuxButton(c)
            b.setMinimumHeight(34)
            chips.addWidget(b, 0)

        chips.addStretch(1)
        ll.addLayout(chips)

        lst = QListWidget()
        for name in [
            "Chicken Bowl",
            "Overnight Oats",
            "Taco Night",
            "Salmon + Rice",
            "Stir Fry",
            "Greek Yogurt Parfait",
        ]:
            lst.addItem(QListWidgetItem(name))
        ll.addWidget(lst, 1)

        add_row = QHBoxLayout()
        add_row.setContentsMargins(0, 0, 0, 0)
        add_row.setSpacing(10)

        new_btn = LuxButton("New Recipe")
        new_btn.setMinimumHeight(38)
        add_row.addWidget(new_btn, 1)

        pin_btn = LuxButton("Pin")
        pin_btn.setMinimumHeight(38)
        add_row.addWidget(pin_btn, 1)

        ll.addLayout(add_row)

        splitter.addWidget(lib)

        # Planner + shopping preview
        right = QWidget()
        rl = QVBoxLayout(right)
        rl.setContentsMargins(0, 0, 0, 0)
        rl.setSpacing(12)

        plan_card = Card()
        pl = QVBoxLayout(plan_card)
        pl.setContentsMargins(12, 12, 12, 12)
        pl.setSpacing(10)

        cap = QLabel("Week")
        cap.setObjectName("MetaCaption")
        pl.addWidget(cap)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)

        host = QWidget()
        grid = QGridLayout(host)
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setSpacing(12)

        days = [("Mon", "—"), ("Tue", "—"), ("Wed", "—"), ("Thu", "—"), ("Fri", "—"), ("Sat", "—"), ("Sun", "—")]
        for i, (d, ds) in enumerate(days):
            grid.addWidget(_MealDayCard(d, ds), 0, i)

        grid.setColumnStretch(0, 1)
        scroll.setWidget(host)

        pl.addWidget(scroll, 1)

        # cross-feature “future hooks” (non-functional)
        hooks = QHBoxLayout()
        hooks.setContentsMargins(0, 0, 0, 0)
        hooks.setSpacing(10)

        hooks.addStretch(1)
        hooks.addWidget(LuxButton("Send to Scheduler"), 0)
        hooks.addWidget(LuxButton("Open Grocery Run"), 0)

        pl.addLayout(hooks)

        rl.addWidget(plan_card, 1)

        shop = Card()
        sl = QVBoxLayout(shop)
        sl.setContentsMargins(12, 12, 12, 12)
        sl.setSpacing(10)

        st = QLabel("Shopping Preview")
        st.setObjectName("TitleUnified")
        sl.addWidget(st)

        for item in ["• Chicken breast", "• Rice", "• Greek yogurt", "• Greens", "• Tortillas"]:
            sl.addWidget(QLabel(item))

        sl.addStretch(1)

        rl.addWidget(shop, 0)

        splitter.addWidget(right)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 3)

        root.addWidget(splitter, 1)

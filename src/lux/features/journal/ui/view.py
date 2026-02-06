from __future__ import annotations

from PySide6.QtCore import Qt, QDate
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QTextEdit,
    QComboBox,
    QSpinBox,
    QToolButton,
    QDateEdit,
    QCheckBox,
    QSplitter,
)

from lux.ui.qt.widgets.cards import Card
from lux.ui.qt.widgets.buttons import LuxButton


class JournalRightView(QWidget):
    """
    UI-only “classic Lux Journal” layout:
    - Header: Date + Title
    - Formatting bar (non-functional)
    - Main editor
    - Bottom: Daily Habits + Photos panels
    """

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(12)

        # Top editor card
        editor_card = Card()
        e = QVBoxLayout(editor_card)
        e.setContentsMargins(14, 14, 14, 14)
        e.setSpacing(10)

        title = QLabel("Journal Entry")
        title.setObjectName("TitleUnified")
        e.addWidget(title)

        # Date + title row
        row = QWidget()
        r = QHBoxLayout(row)
        r.setContentsMargins(0, 0, 0, 0)
        r.setSpacing(10)

        date_lbl = QLabel("Date")
        date_lbl.setObjectName("MetaCaption")
        r.addWidget(date_lbl, 0)

        self._date = QDateEdit()
        self._date.setCalendarPopup(True)
        self._date.setDate(QDate.currentDate())
        r.addWidget(self._date, 0)

        r.addSpacing(10)

        title_lbl = QLabel("Title")
        title_lbl.setObjectName("MetaCaption")
        r.addWidget(title_lbl, 0)

        self._title = QLineEdit()
        self._title.setPlaceholderText("Entry title…")
        r.addWidget(self._title, 1)

        e.addWidget(row)

        # Format bar (UI-only)
        bar = QWidget()
        b = QHBoxLayout(bar)
        b.setContentsMargins(0, 0, 0, 0)
        b.setSpacing(8)

        fmt_lbl = QLabel("Format")
        fmt_lbl.setObjectName("MetaCaption")
        b.addWidget(fmt_lbl, 0)

        font_combo = QComboBox()
        font_combo.addItems(["Inter", "Segoe UI", "System"])
        b.addWidget(font_combo, 0)

        size = QSpinBox()
        size.setRange(8, 72)
        size.setValue(15)
        b.addWidget(size, 0)

        def _tool(text: str) -> QToolButton:
            t = QToolButton()
            t.setAutoRaise(True)
            t.setCursor(Qt.PointingHandCursor)
            t.setText(text)
            return t

        for t in ["B", "I", "U", "S", "x²", "x₂", "Color"]:
            b.addWidget(_tool(t), 0)

        b.addStretch(1)
        e.addWidget(bar)

        # Editor
        self._edit = QTextEdit()
        self._edit.setPlaceholderText("Write your entry…")
        self._edit.setAcceptRichText(True)
        e.addWidget(self._edit, 1)

        root.addWidget(editor_card, 1)

        # Bottom row: Habits + Photos
        splitter = QSplitter(Qt.Horizontal)
        splitter.setChildrenCollapsible(False)

        # Habits card
        habits = Card()
        hl = QVBoxLayout(habits)
        hl.setContentsMargins(12, 12, 12, 12)
        hl.setSpacing(10)

        h_top = QHBoxLayout()
        h_top.setContentsMargins(0, 0, 0, 0)

        h_title = QLabel("Daily Habits")
        h_title.setObjectName("TitleUnified")
        h_top.addWidget(h_title, 0)

        h_top.addStretch(1)

        menu_btn = _tool("⋯")
        h_top.addWidget(menu_btn, 0)

        hl.addLayout(h_top)

        add_row = QHBoxLayout()
        add_row.setContentsMargins(0, 0, 0, 0)
        add_row.setSpacing(10)

        habit_in = QLineEdit()
        habit_in.setPlaceholderText("Add your habits here…")
        add_row.addWidget(habit_in, 1)

        add_btn = LuxButton("Add")
        add_btn.setMinimumHeight(36)
        add_row.addWidget(add_btn, 0)

        hl.addLayout(add_row)

        # Sample checklist
        for txt in ["You can change them", "Save them as a template", "Drink water or something idk lol"]:
            chk = QCheckBox(txt)
            hl.addWidget(chk)

        hl.addStretch(1)

        # Photos card
        photos = Card()
        pl = QVBoxLayout(photos)
        pl.setContentsMargins(12, 12, 12, 12)
        pl.setSpacing(10)

        p_top = QHBoxLayout()
        p_top.setContentsMargins(0, 0, 0, 0)

        p_title = QLabel("Photos")
        p_title.setObjectName("TitleUnified")
        p_top.addWidget(p_title, 0)

        p_top.addStretch(1)

        trash = _tool("🗑")
        plus = _tool("＋")
        p_top.addWidget(trash, 0)
        p_top.addWidget(plus, 0)

        pl.addLayout(p_top)

        # Preview area (placeholder)
        preview = Card()
        pv = QVBoxLayout(preview)
        pv.setContentsMargins(10, 10, 10, 10)
        pv.setSpacing(10)

        ph = QLabel("Drop photos here (wiring later)")
        ph.setObjectName("MetaCaption")
        ph.setAlignment(Qt.AlignCenter)
        pv.addStretch(1)
        pv.addWidget(ph, 0)
        pv.addStretch(1)

        pl.addWidget(preview, 1)

        nav = QHBoxLayout()
        nav.setContentsMargins(0, 0, 0, 0)
        nav.setSpacing(10)

        left = _tool("‹")
        right = _tool("›")
        count = QLabel("1")
        count.setObjectName("MetaCaption")
        count.setAlignment(Qt.AlignCenter)

        nav.addWidget(left, 0)
        nav.addStretch(1)
        nav.addWidget(count, 0)
        nav.addStretch(1)
        nav.addWidget(right, 0)

        pl.addLayout(nav)

        splitter.addWidget(habits)
        splitter.addWidget(photos)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 1)

        root.addWidget(splitter, 0)

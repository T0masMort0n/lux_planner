from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QAbstractItemView,
)

from lux.ui.qt.widgets.buttons import LuxButton
from lux.ui.qt.widgets.cards import Card


class JournalLeftPanel(QWidget):
    """
    Journal navigation/entry list panel (UI only).
    Matches the spirit of the old Lux Journal left rail: New/Save/Load + search + entries list.
    """

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(12)

        header = QLabel("Lux Journal")
        header.setObjectName("MetaCaption")
        root.addWidget(header)

        # Actions
        actions = Card()
        a = QHBoxLayout(actions)
        a.setContentsMargins(10, 10, 10, 10)
        a.setSpacing(10)

        for txt in ["New", "Save", "Load"]:
            b = LuxButton(txt)
            b.setMinimumHeight(38)
            a.addWidget(b, 1)

        root.addWidget(actions, 0)

        # Search
        self._search = QLineEdit()
        self._search.setPlaceholderText("Search entries…")
        root.addWidget(self._search, 0)

        # Entries list
        list_card = Card()
        lc = QVBoxLayout(list_card)
        lc.setContentsMargins(10, 10, 10, 10)
        lc.setSpacing(10)

        cap = QLabel("Entries")
        cap.setObjectName("MetaCaption")
        lc.addWidget(cap)

        self._list = QListWidget()
        self._list.setUniformItemSizes(True)
        self._list.setSelectionMode(QAbstractItemView.SingleSelection)


        # Seed sample entries (non-functional)
        samples = [
            ("2026/Feb/01", "Welcome! (Load This Entry!)"),
            ("2026/Jan/31", "Late night brain dump"),
            ("2026/Jan/30", "Project notes"),
        ]
        for d, t in samples:
            item = QListWidgetItem(f"{d}\n{t}")
            self._list.addItem(item)

        self._list.setCurrentRow(0)

        lc.addWidget(self._list, 1)

        hint = QLabel("Tip: wiring search/filter happens later in Journal service/repo.")
        hint.setObjectName("MetaCaption")
        hint.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        lc.addWidget(hint, 0)

        root.addWidget(list_card, 1)

        # Footer action
        del_btn = LuxButton("Delete Entry")
        del_btn.setMinimumHeight(44)
        root.addWidget(del_btn, 0)

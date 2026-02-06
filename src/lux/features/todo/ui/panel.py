from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QHBoxLayout,
    QLineEdit,
    QScrollArea,
    QFrame,
    QCheckBox,
    QToolButton,
)

from lux.ui.qt.widgets.buttons import LuxButton
from lux.ui.qt.widgets.cards import Card
from lux.features.todo.ui.controller import TodoController


class _OccRow(QWidget):
    def __init__(
        self,
        occ_id: int,
        title: str,
        completed: bool,
        on_toggle,
        on_archive,
        parent=None,
    ) -> None:
        super().__init__(parent)
        self._occ_id = occ_id
        self._on_toggle = on_toggle
        self._on_archive = on_archive

        lay = QHBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(10)

        chk = QCheckBox()
        chk.setChecked(completed)
        chk.stateChanged.connect(self._handle_check)
        lay.addWidget(chk, 0, Qt.AlignTop)

        lbl = QLabel(title)
        lbl.setWordWrap(True)
        lay.addWidget(lbl, 1)

        archive_btn = QToolButton()
        archive_btn.setAutoRaise(True)
        archive_btn.setCursor(Qt.PointingHandCursor)
        archive_btn.setText("✕")
        archive_btn.clicked.connect(self._handle_archive)
        lay.addWidget(archive_btn, 0, Qt.AlignTop)

    def _handle_check(self, state: int) -> None:
        self._on_toggle(self._occ_id, state == Qt.Checked)

    def _handle_archive(self) -> None:
        self._on_archive(self._occ_id)


class TodoLeftPanel(QWidget):
    """
    Inbox-style To Do left panel.
    Keeps existing controller wiring (today list + add today).
    """

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self._ctl = TodoController(self)
        self._ctl.changed.connect(self._refresh)

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(12)

        # Header
        header_row = QHBoxLayout()
        header_row.setContentsMargins(0, 0, 0, 0)
        header_row.setSpacing(10)

        header = QLabel("To Do")
        header.setObjectName("MetaCaption")
        header_row.addWidget(header, 1, Qt.AlignVCenter)

        plan_btn = LuxButton("Plan")
        plan_btn.setMinimumHeight(36)
        header_row.addWidget(plan_btn, 0)

        root.addLayout(header_row)

        # Quick add card
        add_card = Card()
        add_lay = QVBoxLayout(add_card)
        add_lay.setContentsMargins(12, 12, 12, 12)
        add_lay.setSpacing(10)

        add_title = QLabel("Add")
        add_title.setObjectName("MetaCaption")
        add_lay.addWidget(add_title)

        add_row = QHBoxLayout()
        add_row.setContentsMargins(0, 0, 0, 0)
        add_row.setSpacing(10)

        self._input = QLineEdit()
        self._input.setPlaceholderText("Add a task for today…")
        self._input.returnPressed.connect(self._on_add)
        add_row.addWidget(self._input, 1)

        add_btn = LuxButton("Add")
        add_btn.setMinimumHeight(36)
        add_btn.clicked.connect(self._on_add)
        add_row.addWidget(add_btn, 0)

        add_lay.addLayout(add_row)

        hint = QLabel("Tip: keep titles short. Details can live in notes later.")
        hint.setObjectName("MetaCaption")
        hint.setWordWrap(True)
        add_lay.addWidget(hint)

        root.addWidget(add_card)

        # List container (scroll)
        list_card = Card()
        list_lay = QVBoxLayout(list_card)
        list_lay.setContentsMargins(12, 12, 12, 12)
        list_lay.setSpacing(10)

        list_title = QLabel("Today")
        list_title.setObjectName("MetaCaption")
        list_lay.addWidget(list_title)

        self._scroll = QScrollArea()
        self._scroll.setWidgetResizable(True)
        self._scroll.setFrameShape(QFrame.NoFrame)

        self._list_host = QWidget()
        self._list_lay = QVBoxLayout(self._list_host)
        self._list_lay.setContentsMargins(0, 0, 0, 0)
        self._list_lay.setSpacing(10)
        self._list_lay.addStretch(1)

        self._scroll.setWidget(self._list_host)
        list_lay.addWidget(self._scroll, 1)

        root.addWidget(list_card, 1)

        # Footer (non-functional placeholders)
        footer = QHBoxLayout()
        footer.setContentsMargins(0, 0, 0, 0)
        footer.setSpacing(10)

        backlog = LuxButton("Backlog")
        backlog.setMinimumHeight(36)
        footer.addWidget(backlog, 1)

        archive = LuxButton("Archive")
        archive.setMinimumHeight(36)
        footer.addWidget(archive, 1)

        root.addLayout(footer)

        self._refresh()

    def _on_add(self) -> None:
        text = self._input.text().strip()
        if not text:
            return
        self._input.clear()
        self._ctl.add_today(text)

    def _refresh(self) -> None:
        # clear rows but keep trailing stretch
        while self._list_lay.count():
            item = self._list_lay.takeAt(0)
            w = item.widget()
            if w is not None:
                w.setParent(None)
                w.deleteLater()

        occs = self._ctl.today()

        if not occs:
            empty = QLabel("No tasks for today yet.")
            empty.setObjectName("MetaCaption")
            self._list_lay.addWidget(empty)
        else:
            for occ in occs:
                row = _OccRow(
                    occ_id=occ.id,
                    title=occ.title,
                    completed=occ.completed,
                    on_toggle=self._ctl.set_completed,
                    on_archive=self._ctl.archive,
                )
                self._list_lay.addWidget(row)

        self._list_lay.addStretch(1)

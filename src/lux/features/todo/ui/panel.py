from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QHBoxLayout, QLineEdit, QScrollArea, QFrame, QCheckBox, QToolButton
)

from lux.features.todo.ui.controller import TodoController


class _OccRow(QWidget):
    def __init__(self, occ_id: int, title: str, completed: bool, on_toggle, on_archive, parent=None) -> None:
        super().__init__(parent)
        self._occ_id = occ_id
        self._on_toggle = on_toggle
        self._on_archive = on_archive

        lay = QHBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(10)

        self.chk = QCheckBox()
        self.chk.setChecked(completed)
        self.chk.stateChanged.connect(self._handle_check)
        lay.addWidget(self.chk, 0, Qt.AlignTop)

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
    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self._ctl = TodoController(self)
        self._ctl.changed.connect(self._refresh)

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(12)

        header = QLabel("To Do")
        header.setObjectName("MetaCaption")
        root.addWidget(header)

        # Add row
        add_row = QHBoxLayout()
        add_row.setContentsMargins(0, 0, 0, 0)
        add_row.setSpacing(10)

        self._input = QLineEdit()
        self._input.setPlaceholderText("Add a task for today…")
        self._input.returnPressed.connect(self._on_add)
        add_row.addWidget(self._input, 1)

        add_btn = QToolButton()
        add_btn.setAutoRaise(True)
        add_btn.setCursor(Qt.PointingHandCursor)
        add_btn.setText("Add")
        add_btn.clicked.connect(self._on_add)
        add_row.addWidget(add_btn, 0)

        root.addLayout(add_row)

        # List container (scroll)
        self._scroll = QScrollArea()
        self._scroll.setWidgetResizable(True)
        self._scroll.setFrameShape(QFrame.NoFrame)

        self._list_host = QWidget()
        self._list_lay = QVBoxLayout(self._list_host)
        self._list_lay.setContentsMargins(0, 0, 0, 0)
        self._list_lay.setSpacing(10)
        self._list_lay.addStretch(1)

        self._scroll.setWidget(self._list_host)
        root.addWidget(self._scroll, 1)

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

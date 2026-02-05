from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QCheckBox, QFrame, QScrollArea

from lux.features.todo.ui.controller import TodoController


class TodoRightView(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self._ctl = TodoController(self)
        self._ctl.changed.connect(self._refresh)

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(12)

        title = QLabel("To Do")
        title.setObjectName("TitleUnified")
        title.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        root.addWidget(title)

        self._scroll = QScrollArea()
        self._scroll.setWidgetResizable(True)
        self._scroll.setFrameShape(QFrame.NoFrame)

        self._host = QWidget()
        self._lay = QVBoxLayout(self._host)
        self._lay.setContentsMargins(0, 0, 0, 0)
        self._lay.setSpacing(10)

        self._scroll.setWidget(self._host)
        root.addWidget(self._scroll, 1)

        self._refresh()

    def _refresh(self) -> None:
        while self._lay.count():
            item = self._lay.takeAt(0)
            w = item.widget()
            if w is not None:
                w.setParent(None)
                w.deleteLater()

        # Today
        today_lbl = QLabel("Today")
        today_lbl.setObjectName("MetaCaption")
        self._lay.addWidget(today_lbl)

        today = self._ctl.today()
        if not today:
            e = QLabel("Nothing scheduled for today.")
            e.setObjectName("MetaCaption")
            self._lay.addWidget(e)
        else:
            for occ in today:
                row = QWidget()
                r = QHBoxLayout(row)
                r.setContentsMargins(0, 0, 0, 0)
                r.setSpacing(10)

                chk = QCheckBox()
                chk.setChecked(occ.completed)
                chk.stateChanged.connect(lambda state, oid=occ.id: self._ctl.set_completed(oid, state == Qt.Checked))
                r.addWidget(chk, 0)

                lbl = QLabel(occ.title)
                lbl.setWordWrap(True)
                r.addWidget(lbl, 1)

                self._lay.addWidget(row)

        # Upcoming
        upcoming_lbl = QLabel("Upcoming (7 days)")
        upcoming_lbl.setObjectName("MetaCaption")
        self._lay.addWidget(upcoming_lbl)

        upcoming = [o for o in self._ctl.upcoming(7) if o.due_date != today[0].due_date] if today else self._ctl.upcoming(7)
        if not upcoming:
            e2 = QLabel("No upcoming tasks.")
            e2.setObjectName("MetaCaption")
            self._lay.addWidget(e2)
        else:
            for occ in upcoming:
                lbl = QLabel(f"{occ.due_date} — {occ.title}")
                lbl.setWordWrap(True)
                self._lay.addWidget(lbl)

        self._lay.addStretch(1)

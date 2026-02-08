from __future__ import annotations

from datetime import date, timedelta

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QHBoxLayout,
    QCheckBox,
    QFrame,
    QScrollArea,
)

from lux.app.services import SystemServices
from lux.ui.qt.dragdrop import decode_mime
from lux.ui.qt.widgets.buttons import LuxButton
from lux.ui.qt.widgets.cards import Card
from lux.features.todo.ui.controller import TodoController


class _DateDropCard(Card):
    """
    System DnD target that resolves to a specific date string.
    """

    def __init__(self, target_date: str, controller: TodoController, parent=None) -> None:
        super().__init__(parent)
        self._target_date = target_date
        self._ctl = controller
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event) -> None:  # noqa: N802 (Qt override)
        payload = decode_mime(event.mimeData())
        if payload and payload.kind in ("task_occurrence", "task_definition"):
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event) -> None:  # noqa: N802 (Qt override)
        payload = decode_mime(event.mimeData())
        if not payload:
            event.ignore()
            return

        self._ctl.handle_drop(payload, self._target_date)
        event.acceptProposedAction()


class TodoRightView(QWidget):
    """
    Dashboard-style To Do view.

    - Data/service access is injected via SystemServices.
    - State-changing drops are only accepted on specific-date targets.
    """

    def __init__(self, services: SystemServices, parent=None) -> None:
        super().__init__(parent)

        self._ctl = TodoController(services, self)
        self._ctl.changed.connect(self._refresh)

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(12)

        header_row = QHBoxLayout()
        header_row.setContentsMargins(0, 0, 0, 0)
        header_row.setSpacing(10)

        title = QLabel("To Do")
        title.setObjectName("TitleUnified")
        title.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        header_row.addWidget(title, 1)

        new_btn = LuxButton("New task")
        new_btn.setMinimumHeight(40)
        header_row.addWidget(new_btn, 0)

        focus_btn = LuxButton("Focus mode")
        focus_btn.setMinimumHeight(40)
        header_row.addWidget(focus_btn, 0)

        root.addLayout(header_row)

        self._scroll = QScrollArea()
        self._scroll.setWidgetResizable(True)
        self._scroll.setFrameShape(QFrame.NoFrame)

        self._host = QWidget()
        self._lay = QVBoxLayout(self._host)
        self._lay.setContentsMargins(0, 0, 0, 0)
        self._lay.setSpacing(12)

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

        today_str = date.today().isoformat()

        # Today card (specific-date drop target)
        today_card = _DateDropCard(target_date=today_str, controller=self._ctl)
        t_lay = QVBoxLayout(today_card)
        t_lay.setContentsMargins(14, 14, 14, 14)
        t_lay.setSpacing(10)

        today_lbl = QLabel(f"Today ({today_str})")
        today_lbl.setObjectName("MetaCaption")
        t_lay.addWidget(today_lbl)

        today = self._ctl.today()
        if not today:
            e = QLabel("Nothing scheduled for today.")
            e.setObjectName("MetaCaption")
            t_lay.addWidget(e)
        else:
            for occ in today:
                row = QWidget()
                r = QHBoxLayout(row)
                r.setContentsMargins(0, 0, 0, 0)
                r.setSpacing(10)

                chk = QCheckBox()
                chk.setChecked(occ.completed)
                chk.stateChanged.connect(
                    lambda state, oid=occ.id: self._ctl.set_completed(oid, state == Qt.Checked)
                )
                r.addWidget(chk, 0, Qt.AlignTop)

                lbl = QLabel(occ.title)
                lbl.setWordWrap(True)
                r.addWidget(lbl, 1)

                t_lay.addWidget(row)

        self._lay.addWidget(today_card)

        # Upcoming card (date-resolving drop targets only)
        up_card = Card()
        u_lay = QVBoxLayout(up_card)
        u_lay.setContentsMargins(14, 14, 14, 14)
        u_lay.setSpacing(10)

        upcoming_lbl = QLabel("Upcoming (7 days)")
        upcoming_lbl.setObjectName("MetaCaption")
        u_lay.addWidget(upcoming_lbl)

        # Build a simple per-date section so drop targets always resolve to a specific date.
        upcoming = self._ctl.upcoming(7)
        by_date: dict[str, list[str]] = {}
        for occ in upcoming:
            by_date.setdefault(occ.due_date, []).append(occ.title)

        for i in range(7):
            d = (date.today() + timedelta(days=i)).isoformat()
            date_card = _DateDropCard(target_date=d, controller=self._ctl)
            dc_lay = QVBoxLayout(date_card)
            dc_lay.setContentsMargins(10, 10, 10, 10)
            dc_lay.setSpacing(6)

            d_lbl = QLabel(d)
            d_lbl.setObjectName("MetaCaption")
            dc_lay.addWidget(d_lbl)

            titles = by_date.get(d, [])
            if not titles:
                empty = QLabel("—")
                empty.setObjectName("MetaCaption")
                dc_lay.addWidget(empty)
            else:
                for title in titles:
                    lbl = QLabel(title)
                    lbl.setWordWrap(True)
                    dc_lay.addWidget(lbl)

            u_lay.addWidget(date_card)

        actions = QHBoxLayout()
        actions.setContentsMargins(0, 0, 0, 0)
        actions.setSpacing(10)
        actions.addStretch(1)

        sched = LuxButton("Open scheduler")
        sched.setMinimumHeight(38)
        actions.addWidget(sched)

        review = LuxButton("Weekly review")
        review.setMinimumHeight(38)
        actions.addWidget(review)

        u_lay.addLayout(actions)
        self._lay.addWidget(up_card)

        # Placeholder: details panel hint
        hint_card = Card()
        h_lay = QVBoxLayout(hint_card)
        h_lay.setContentsMargins(14, 14, 14, 14)
        h_lay.setSpacing(6)

        h_title = QLabel("Details (placeholder)")
        h_title.setObjectName("MetaCaption")
        h_lay.addWidget(h_title)

        hint = QLabel("Later: selecting a task will show notes, subtasks, and history here.")
        hint.setWordWrap(True)
        hint.setObjectName("MetaCaption")
        h_lay.addWidget(hint)

        self._lay.addWidget(hint_card)

        self._lay.addStretch(1)

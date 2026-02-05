from __future__ import annotations

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from lux.ui.qt.widgets.buttons import LuxButton


class ExerciseLeftPanel(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(10)

        lbl = QLabel("Exercise")
        lbl.setObjectName("MetaCaption")
        lay.addWidget(lbl)

        for name in ["Today", "Plan", "History"]:
            b = LuxButton(name)
            b.setMinimumHeight(40)
            lay.addWidget(b)

        lay.addStretch(1)

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel


class SchedulerDayView(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(12)

        title = QLabel("Scheduler (placeholder day view)")
        title.setObjectName("TitleUnified")
        title.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        lay.addWidget(title)

        hint = QLabel("Next step: plug in the real day planner widget here.")
        hint.setWordWrap(True)
        hint.setStyleSheet("color: rgba(230,237,243,0.75);")
        lay.addWidget(hint)

        lay.addStretch(1)

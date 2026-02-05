from __future__ import annotations

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel


class JournalLeftPanel(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(12)

        lbl = QLabel("Journal panel (placeholder)")
        lbl.setObjectName("MetaCaption")
        lay.addWidget(lbl)

        lay.addStretch(1)

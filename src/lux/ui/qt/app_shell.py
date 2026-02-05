from __future__ import annotations

from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QFrame

from lux.ui.qt.widgets.cards import Card


class AppShell(QWidget):
    """
    Owns the split layout and the left overlay menu animation.

    Stable version:
    - Overlay always exists
    - Geometry never changes
    - No clipping, resizing, or height tricks
    - Only opacity is animated
    """

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        root = QHBoxLayout(self)
        root.setContentsMargins(24, 22, 24, 22)
        root.setSpacing(16)

        self.left_panel = Card()
        self.left_panel.setFixedWidth(360)

        self.right_panel = Card()

        root.addWidget(self.left_panel, 0)
        root.addWidget(self.right_panel, 1)

        self._left_lay = QVBoxLayout(self.left_panel)
        self._left_lay.setContentsMargins(14, 14, 14, 14)
        self._left_lay.setSpacing(12)

        self._right_lay = QVBoxLayout(self.right_panel)
        self._right_lay.setContentsMargins(18, 18, 18, 18)
        self._right_lay.setSpacing(12)

        self._left_content: QWidget | None = None
        self._right_content: QWidget | None = None

        # -------------------------------
        # MENU OVERLAY (stable structure)
        # -------------------------------
        self.nav_overlay = QFrame(self.left_panel)
        self.nav_overlay.setObjectName("Card")
        self.nav_overlay.setFrameShape(QFrame.NoFrame)
        self.nav_overlay.setFocusPolicy(Qt.NoFocus)

        self._nav_layout = QVBoxLayout(self.nav_overlay)
        self._nav_layout.setContentsMargins(24, 14, 14, 14)
        self._nav_layout.setSpacing(10)

        self.nav_overlay.setEnabled(False)
        self.nav_overlay.setWindowOpacity(0.0)
        self.nav_overlay.setVisible(False)
        self.nav_overlay.setAttribute(Qt.WA_TransparentForMouseEvents, True)

        self._nav_anim: QPropertyAnimation | None = None
        self._nav_open = False


    # -----------------------------------
    # Panel content
    # -----------------------------------
    def set_left_content(self, w: QWidget) -> None:
        if self._left_content is not None:
            self._left_content.setParent(None)
            self._left_content.deleteLater()
        self._left_content = w
        self._left_lay.addWidget(w, 1)

    def set_right_content(self, w: QWidget) -> None:
        if self._right_content is not None:
            self._right_content.setParent(None)
            self._right_content.deleteLater()
        self._right_content = w
        self._right_lay.addWidget(w, 1)

    def set_overlay_content(self, w: QWidget) -> None:
        while self._nav_layout.count():
            item = self._nav_layout.takeAt(0)
            ww = item.widget()
            if ww is not None:
                ww.setParent(None)
                ww.deleteLater()

        self._nav_layout.addWidget(w, 1)

    # -----------------------------------
    # Menu control (opacity animation)
    # -----------------------------------
    def toggle_nav_overlay(self) -> None:
        self._animate_nav(not self._nav_open)

    def close_nav_overlay(self) -> None:
        if self._nav_open:
            self._animate_nav(False)

    def _animate_nav(self, opening: bool) -> None:
        if self._nav_anim:
            self._nav_anim.stop()

        # IMPORTANT:
        # The overlay is a full-geometry widget. Even at opacity 0 / disabled, it can
        # still block mouse events. We explicitly make it non-blocking when closed.
        if opening:
            self.nav_overlay.setVisible(True)
            self.nav_overlay.setEnabled(True)
            self.nav_overlay.setAttribute(Qt.WA_TransparentForMouseEvents, False)
        else:
            # During fade-out, we want clicks to pass through immediately.
            self.nav_overlay.setEnabled(False)
            self.nav_overlay.setAttribute(Qt.WA_TransparentForMouseEvents, True)

        self.nav_overlay.raise_()

        self._nav_anim = QPropertyAnimation(self.nav_overlay, b"windowOpacity", self)
        self._nav_anim.setDuration(220)
        self._nav_anim.setEasingCurve(QEasingCurve.InOutCubic)

        if opening:
            self.nav_overlay.setWindowOpacity(0.0)
            self._nav_anim.setStartValue(0.0)
            self._nav_anim.setEndValue(1.0)
        else:
            self._nav_anim.setStartValue(self.nav_overlay.windowOpacity())
            self._nav_anim.setEndValue(0.0)

        def finished() -> None:
            if not opening:
                # Fully remove it from interaction + hit testing.
                self.nav_overlay.setWindowOpacity(0.0)
                self.nav_overlay.setVisible(False)

        self._nav_anim.finished.connect(finished)
        self._nav_anim.start()

        self._nav_open = opening


    # -----------------------------------
    # Keep overlay full size
    # -----------------------------------
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.nav_overlay.setGeometry(0, 0, self.left_panel.width(), self.left_panel.height())

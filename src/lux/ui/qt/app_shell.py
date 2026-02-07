from __future__ import annotations

from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QFrame, QSizePolicy, QSplitter

from lux.ui.qt.widgets.cards import Card


class AppShell(QWidget):
    """
    System-owned AppShell with hard surface boundaries on the left.

    Left side structure (system-owned):
      LeftColumnContainer
        HeaderSurface (always visible; title/menu anchor)
        LeftRow
          NavSurface (system-owned; width controlled ONLY by system nav state)
          FeatureLeftSurface (system-owned; expanding; single child swapped)

    Right side:
      RightContentSurface (system-owned)

    Overlay menu remains a dropdown from the title area, but nav width is still
    policy-bound by system nav state (expanded vs collapsed).
    """

    NAV_WIDTH_EXPANDED = 240
    NAV_WIDTH_COLLAPSED = 0  # per clarified contract: can be 0 or icon-strip width

    # Splitter bounds (system-enforced): left pane width clamped to [25%, 50%] of AppShell width.
    LEFT_PANE_MIN_RATIO = 0.25
    LEFT_PANE_MAX_RATIO = 0.50

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        root = QHBoxLayout(self)
        root.setContentsMargins(24, 22, 24, 22)
        root.setSpacing(16)

        # -----------------------------------
        # Root splitter (system-owned)
        # Exactly two children:
        #   LeftColumnContainer (system-owned)
        #   RightContentSurface (system-owned)
        # -----------------------------------
        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.setChildrenCollapsible(False)
        # Left pane stable, right pane flexible.
        self.splitter.setStretchFactor(0, 0)
        self.splitter.setStretchFactor(1, 1)



        # -----------------------------------
        # Left column container (system-owned)
        # -----------------------------------
        self.left_column = QWidget()
        left_col_lay = QVBoxLayout(self.left_column)
        left_col_lay.setContentsMargins(0, 0, 0, 0)
        left_col_lay.setSpacing(12)

        # HeaderSurface: always visible; menu anchor lives here.
        self.header_surface = Card()
        self.header_surface.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self._header_lay = QVBoxLayout(self.header_surface)
        self._header_lay.setContentsMargins(14, 14, 14, 14)
        self._header_lay.setSpacing(0)

        # LeftRow: nav + feature-left as separate QWidget roots.
        self.left_row = QWidget()
        left_row_lay = QHBoxLayout(self.left_row)
        left_row_lay.setContentsMargins(0, 0, 0, 0)
        left_row_lay.setSpacing(16)

        # NavSurface: width controlled ONLY by system nav state.
        self.nav_surface = Card()
        self.nav_surface.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        self.nav_surface.setFixedWidth(self.NAV_WIDTH_COLLAPSED)

        self._nav_surface_lay = QVBoxLayout(self.nav_surface)
        self._nav_surface_lay.setContentsMargins(14, 14, 14, 14)
        self._nav_surface_lay.setSpacing(12)

        # FeatureLeftSurface: expanding.
        self.feature_left_surface = Card()
        self.feature_left_surface.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self._feature_left_lay = QVBoxLayout(self.feature_left_surface)
        self._feature_left_lay.setContentsMargins(14, 14, 14, 14)
        self._feature_left_lay.setSpacing(12)

        left_row_lay.addWidget(self.nav_surface, 0)
        left_row_lay.addWidget(self.feature_left_surface, 1)

        left_col_lay.addWidget(self.header_surface, 0)
        left_col_lay.addWidget(self.left_row, 1)

        # -----------------------------------
        # Right content surface (system-owned)
        # -----------------------------------
        self.right_panel = Card()
        self._right_lay = QVBoxLayout(self.right_panel)
        self._right_lay.setContentsMargins(18, 18, 18, 18)
        self._right_lay.setSpacing(12)

        self.splitter.addWidget(self.left_column)
        self.splitter.addWidget(self.right_panel)
        root.addWidget(self.splitter, 1)

        # Initial splitter sizing (will be clamped on first resize/layout).
        self.splitter.setSizes([int(self.width() * 0.33), int(self.width() * 0.67)])
        self.splitter.splitterMoved.connect(self._on_splitter_moved)

        # Ensure initial left-pane policy is applied before first paint.
        self._clamp_left_pane_width()
        self._apply_left_pane_policy(False)

        self._header_content: QWidget | None = None
        self._nav_content: QWidget | None = None
        self._feature_left_content: QWidget | None = None
        self._right_content: QWidget | None = None

        # -------------------------------
        # MENU OVERLAY (dropdown)
        # Parented to left_column so it can drop over header + left surfaces.
        # -------------------------------
        self.nav_overlay = QFrame(self.left_column)
        self.nav_overlay.setObjectName("Card")
        self.nav_overlay.setFrameShape(QFrame.NoFrame)
        self.nav_overlay.setFocusPolicy(Qt.NoFocus)

        self._nav_overlay_lay = QVBoxLayout(self.nav_overlay)
        self._nav_overlay_lay.setContentsMargins(24, 14, 14, 14)
        self._nav_overlay_lay.setSpacing(10)

        self.nav_overlay.setEnabled(False)
        self.nav_overlay.setWindowOpacity(0.0)
        self.nav_overlay.setVisible(False)
        self.nav_overlay.setAttribute(Qt.WA_TransparentForMouseEvents, True)

        self._nav_anim: QPropertyAnimation | None = None
        self._nav_open = False

    # -----------------------------------
    # System-owned surfaces: content slots
    # -----------------------------------
    def set_left_header_content(self, w: QWidget) -> None:
        if self._header_content is not None:
            self._header_content.setParent(None)
            self._header_content.deleteLater()
        self._header_content = w
        self._header_lay.addWidget(w, 1)

    def set_nav_content(self, w: QWidget) -> None:
        if self._nav_content is not None:
            self._nav_content.setParent(None)
            self._nav_content.deleteLater()
        self._nav_content = w
        self._nav_surface_lay.addWidget(w, 1)

    def set_feature_left_content(self, w: QWidget) -> None:
        if self._feature_left_content is not None:
            self._feature_left_content.setParent(None)
            self._feature_left_content.deleteLater()
        self._feature_left_content = w
        self._feature_left_lay.addWidget(w, 1)

    # Back-compat: treat "left content" as the feature-left surface content.
    def set_left_content(self, w: QWidget) -> None:
        self.set_feature_left_content(w)

    def set_right_content(self, w: QWidget) -> None:
        if self._right_content is not None:
            self._right_content.setParent(None)
            self._right_content.deleteLater()
        self._right_content = w
        self._right_lay.addWidget(w, 1)

    def set_overlay_content(self, w: QWidget) -> None:
        while self._nav_overlay_lay.count():
            item = self._nav_overlay_lay.takeAt(0)
            ww = item.widget()
            if ww is not None:
                ww.setParent(None)
                ww.deleteLater()

        self._nav_overlay_lay.addWidget(w, 1)

    # -----------------------------------
    # Nav width policy (system-only)
    # -----------------------------------
    def _left_pane_bounds_px(self) -> tuple[int, int]:
        w = max(1, int(self.width()))
        mn = int(round(w * self.LEFT_PANE_MIN_RATIO))
        mx = int(round(w * self.LEFT_PANE_MAX_RATIO))
        # Fail-soft ordering.
        if mx < mn:
            mx = mn
        return mn, mx

    def _clamp_left_pane_width(self) -> None:
        """Enforce splitter left pane width bounds (system-owned policy)."""
        sizes = self.splitter.sizes()
        if len(sizes) != 2:
            return
        total = max(1, int(sizes[0] + sizes[1]))
        mn, mx = self._left_pane_bounds_px()
        left = max(mn, min(mx, int(sizes[0])))
        right = max(1, total - left)
        if left != sizes[0]:
            self.splitter.setSizes([left, right])

    def _w_left(self) -> int:
        sizes = self.splitter.sizes()
        if len(sizes) != 2:
            return max(0, int(self.left_column.width()))
        return max(0, int(sizes[0]))

    def _apply_left_pane_policy(self, nav_expanded: bool) -> None:
        """Apply nav/feature-left width policy against the current splitter pane width."""
        # NOTE: Do NOT set nav_surface fixed width to W_left. That creates a minimum width
        # that prevents dragging the splitter smaller while nav is open.
        _w_left = self._w_left()  # kept for debugging/clarity; layout will satisfy this naturally.

        if nav_expanded:
            # NAV OWNS ENTIRE LEFT PANE (via layout, not fixed width)
            self.nav_surface.setVisible(True)
            self.nav_surface.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.nav_surface.setMinimumWidth(0)
            self.nav_surface.setMaximumWidth(16777215)

            # Remove feature-left from layout influence
            self.feature_left_surface.setVisible(False)
            self.feature_left_surface.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)

        else:
            # FEATURE-LEFT OWNS ENTIRE LEFT PANE
            self.feature_left_surface.setVisible(True)
            self.feature_left_surface.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

            # Remove nav from layout influence
            self.nav_surface.setVisible(False)
            self.nav_surface.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
            self.nav_surface.setFixedWidth(self.NAV_WIDTH_COLLAPSED)

        # Overlay must follow current left column geometry (if overlay exists yet).
        self._update_overlay_geometry()


    def _update_overlay_geometry(self) -> None:
        # During __init__, policy may run before overlay is constructed.
        if not hasattr(self, "nav_overlay"):
            return

        # Dropdown should start under header_surface and cover the left column area.
        y = self.header_surface.y() + self.header_surface.height()
        h = max(0, self.left_column.height() - y)
        self.nav_overlay.setGeometry(0, y, self.left_column.width(), h)


    def _on_splitter_moved(self, *_args) -> None:
        # Clamp policy first, then update dependent geometry.
        self._clamp_left_pane_width()
        self._apply_left_pane_policy(self._nav_open)
        self._update_overlay_geometry()


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

        # Clamp left pane before applying policy.
        self._clamp_left_pane_width()
        self._apply_left_pane_policy(opening)

        if opening:
            self.nav_overlay.setVisible(True)
            self.nav_overlay.setEnabled(True)
            self.nav_overlay.setAttribute(Qt.WA_TransparentForMouseEvents, False)
        else:
            # During fade-out, clicks should pass through immediately.
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
                self.nav_overlay.setVisible(False)
                self.nav_overlay.setWindowOpacity(0.0)
                self._apply_left_pane_policy(False)
            self._nav_open = opening

        self._nav_anim.finished.connect(finished)
        self._nav_anim.start()

    # -----------------------------------
    # Keep overlay positioned as dropdown
    # -----------------------------------
    def resizeEvent(self, event):
        super().resizeEvent(event)

        # Enforce splitter bounds on resize (policy is ratio-based).
        self._clamp_left_pane_width()
        self._apply_left_pane_policy(self._nav_open)

        # Keep overlay aligned to the current left column geometry.
        self._update_overlay_geometry()

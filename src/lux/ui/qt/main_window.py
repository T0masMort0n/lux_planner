from __future__ import annotations

from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QToolButton,
    QComboBox,
)

from lux.app.navigation import AppModuleSpec
from lux.app.services import SystemServices
from lux.core.settings.store import SettingsStore
from lux.core.settings.schema import THEMES_AVAILABLE
from lux.ui.qt.app_shell import AppShell
from lux.ui.qt.settings_view import SettingsLeftPanel, SettingsRightView, SettingsCallbacks
from lux.ui.qt.theme import apply_theme_by_name
from lux.ui.qt.widgets.buttons import LuxButton


class MainWindow(QMainWindow):
    def __init__(
        self,
        settings: SettingsStore,
        registry: list[AppModuleSpec],
        services: SystemServices,
        app,
        parent=None,
    ) -> None:
        super().__init__(parent)
        self._settings = settings
        self._registry = registry
        self._services = services
        self._app = app

        self._settings_right: SettingsRightView | None = None
        self._in_settings = False

        self.setWindowTitle("Lux Planner")
        self.resize(1200, 780)

        self.shell = AppShell()
        self.setCentralWidget(self.shell)

        # -----------------------------------
        # HeaderSurface content (system-owned)
        # Dropdown menu anchor remains here.
        # -----------------------------------
        header_root = QWidget()
        header_lay = QHBoxLayout(header_root)
        header_lay.setContentsMargins(0, 0, 0, 0)
        header_lay.setSpacing(0)

        self.title_btn = QToolButton()
        self.title_btn.setAutoRaise(True)
        self.title_btn.setCursor(Qt.PointingHandCursor)
        self.title_btn.clicked.connect(self._toggle_menu)
        self.title_btn.setObjectName("AppTitleButton")

        header_lay.addWidget(self.title_btn, 1, alignment=Qt.AlignLeft)

        self.shell.set_left_header_content(header_root)

        # -----------------------------------
        # FeatureLeftSurface content holder
        # (feature switching swaps ONLY child widgets here)
        # -----------------------------------
        self._feature_left_holder = QWidget()
        self._feature_left_lay = QVBoxLayout(self._feature_left_holder)
        self._feature_left_lay.setContentsMargins(0, 0, 0, 0)
        self._feature_left_lay.setSpacing(12)

        self.shell.set_feature_left_content(self._feature_left_holder)

        # NavSurface stays system-owned. We don't populate it yet (width is policy-bound in AppShell).
        # Overlay menu content
        self.shell.set_overlay_content(self._build_nav_menu())

        # Start on Journal by default
        self._active_key = "journal"
        self._switch_to(self._active_key)

    def _toggle_menu(self) -> None:
        self.shell.toggle_nav_overlay()

    def _build_nav_menu(self) -> QWidget:
        w = QWidget()
        lay = QVBoxLayout(w)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(12)

        # Quick title
        hdr = QLabel("Menu")
        hdr.setObjectName("TitleUnified")
        lay.addWidget(hdr)

        # Quick theme row
        theme_row = QWidget()
        tr = QHBoxLayout(theme_row)
        tr.setContentsMargins(0, 0, 0, 0)
        tr.setSpacing(10)

        t_lbl = QLabel("Theme")
        t_lbl.setObjectName("MetaCaption")

        self._theme_combo = QComboBox()
        self._theme_combo.addItems(THEMES_AVAILABLE)
        self._theme_combo.setCurrentText(self._settings.get_theme())
        self._theme_combo.currentTextChanged.connect(self._on_theme_changed)

        tr.addWidget(t_lbl)
        tr.addWidget(self._theme_combo, 1)
        lay.addWidget(theme_row)

        # Feature list
        for spec in self._registry:
            b = LuxButton(spec.title)
            b.setMinimumHeight(44)
            b.pressed.connect(lambda k=spec.key: self._on_select_app(k))
            lay.addWidget(b)

        # Settings / Exit
        settings_btn = LuxButton("Settings")
        settings_btn.setMinimumHeight(44)
        settings_btn.pressed.connect(self._on_open_settings)
        lay.addWidget(settings_btn)

        exit_btn = LuxButton("Exit")
        exit_btn.setMinimumHeight(44)
        exit_btn.pressed.connect(self.close)
        lay.addWidget(exit_btn)

        return w

    def _apply_theme(self) -> None:
        apply_theme_by_name(
            self._app,
            theme_name=self._settings.get_theme(),
            font_scale=self._settings.get_font_scale(),
            font_scheme_id=self._settings.get_font_scheme_id(),
        )

    def _on_theme_changed(self, theme: str) -> None:
        self._settings.set_theme(theme)
        self._apply_theme()

    def _on_open_settings(self) -> None:
        self._open_settings()
        QTimer.singleShot(0, self.shell.close_nav_overlay)

    def _open_settings(self) -> None:
        self._in_settings = True
        self.title_btn.setText("Settings")

        # Replace left panel with system-owned Settings categories.
        self._clear_left_surface()

        def on_select_category(key: str) -> None:
            if self._settings_right is not None:
                self._settings_right.show_category(key)

        left = SettingsLeftPanel(on_select_category=on_select_category)
        self._feature_left_lay.addWidget(left, 1)

        callbacks = SettingsCallbacks(
            apply_theme=self._apply_theme,
            apply_font_scale=self._apply_theme,
        )
        self._settings_right = SettingsRightView(settings=self._settings, callbacks=callbacks)
        self.shell.set_right_content(self._settings_right)

    def _on_select_app(self, key: str):
        self._switch_to(key)
        QTimer.singleShot(0, self.shell.close_nav_overlay)

    def _clear_left_surface(self) -> None:
        while self._feature_left_lay.count():
            item = self._feature_left_lay.takeAt(0)
            ww = item.widget()
            if ww is not None:
                ww.setParent(None)
                ww.deleteLater()

    def _switch_to(self, key: str) -> None:
        spec = next((s for s in self._registry if s.key == key), None)
        if spec is None:
            return

        self._in_settings = False
        self._settings_right = None

        self._active_key = key
        self.title_btn.setText(spec.title)

        # Replace left/right surfaces. Fail-soft: if a module view throws,
        # show an on-screen error instead of silently failing to switch.
        self._clear_left_surface()

        try:
            left = spec.make_left_panel(self._services)
            right = spec.make_right_view(self._services)
        except Exception as e:
            err = QLabel(
                "Failed to open this module.\n\n"
                f"{type(e).__name__}: {e}"
            )
            err.setWordWrap(True)
            err.setObjectName("MetaCaption")
            self._feature_left_lay.addWidget(QLabel(""), 1)
            self.shell.set_right_content(err)
            return

        self._feature_left_lay.addWidget(left, 1)
        self.shell.set_right_content(right)
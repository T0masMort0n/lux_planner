from __future__ import annotations

from PySide6.QtCore import Qt, QTimer

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QToolButton, QComboBox
)

from lux.app.navigation import AppModuleSpec
from lux.core.settings.store import SettingsStore
from lux.core.settings.schema import THEMES_AVAILABLE
from lux.ui.qt.app_shell import AppShell
from lux.ui.qt.theme import apply_theme_by_name
from lux.ui.qt.widgets.buttons import LuxButton


class MainWindow(QMainWindow):
    def __init__(self, settings: SettingsStore, registry: list[AppModuleSpec], app, parent=None) -> None:
        super().__init__(parent)
        self._settings = settings
        self._registry = registry
        self._app = app

        self.setWindowTitle("Lux Planner")
        self.resize(1200, 780)

        self.shell = AppShell()
        self.setCentralWidget(self.shell)

        # Top-of-left content: title button + feature-provided panel below
        self._left_root = QWidget()
        left_root_lay = QVBoxLayout(self._left_root)
        left_root_lay.setContentsMargins(0, 0, 0, 0)
        left_root_lay.setSpacing(12)

        # Title row (click opens overlay menu)
        title_row = QHBoxLayout()
        title_row.setContentsMargins(0, 0, 0, 0)

        self.title_btn = QToolButton()
        self.title_btn.setAutoRaise(True)
        self.title_btn.setCursor(Qt.PointingHandCursor)
        self.title_btn.clicked.connect(self._toggle_menu)
        self.title_btn.setObjectName("AppTitleButton")

        title_row.addStretch(1)
        title_row.addWidget(self.title_btn)
        title_row.addStretch(1)

        left_root_lay.addLayout(title_row)

        self._feature_left_holder = QWidget()
        self._feature_left_lay = QVBoxLayout(self._feature_left_holder)
        self._feature_left_lay.setContentsMargins(0, 0, 0, 0)
        self._feature_left_lay.setSpacing(12)

        left_root_lay.addWidget(self._feature_left_holder, 1)

        self.shell.set_left_content(self._left_root)

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
        lay.setSpacing(10)

        # App buttons
        #
        # IMPORTANT:
        # Use `pressed` (not `clicked`) so selection works reliably even if the
        # mouse release happens after the user has already moved to another button.
        for spec in self._registry:
            b = LuxButton(spec.title.replace("Lux ", ""))
            b.setMinimumHeight(44)
            b.pressed.connect(lambda key=spec.key: self._on_select_app(key))
            lay.addWidget(b)

        lay.addStretch(1)

        # Settings: theme dropdown (simple and modular)
        settings_row = QWidget()
        s_lay = QHBoxLayout(settings_row)
        s_lay.setContentsMargins(0, 0, 0, 0)
        s_lay.setSpacing(10)

        lbl = QLabel("Theme")
        lbl.setObjectName("MetaCaption")
        combo = QComboBox()
        combo.addItems(THEMES_AVAILABLE)
        combo.setCurrentText(self._settings.get_theme())
        combo.currentTextChanged.connect(self._on_theme_changed)

        s_lay.addWidget(lbl)
        s_lay.addWidget(combo, 1)
        lay.addWidget(settings_row)

        exit_btn = LuxButton("Exit")
        exit_btn.setMinimumHeight(44)
        exit_btn.pressed.connect(self.close)
        lay.addWidget(exit_btn)

        return w

    def _on_theme_changed(self, theme: str) -> None:
        self._settings.set_theme(theme)
        apply_theme_by_name(self._app, theme_name=theme)

    def _on_select_app(self, key: str):
        # Switch immediately (on press), then collapse the menu on the next tick so
        # we don't interfere with the press event delivery.
        self._switch_to(key)
        QTimer.singleShot(0, self.shell.close_nav_overlay)

    def _switch_to(self, key: str) -> None:
        spec = next((s for s in self._registry if s.key == key), None)
        if spec is None:
            return

        self._active_key = key
        self.title_btn.setText(spec.title)

        # Replace left feature panel (safe clear: widgets + spacers)
        while self._feature_left_lay.count():
            item = self._feature_left_lay.takeAt(0)
            ww = item.widget()
            if ww is not None:
                ww.setParent(None)
                ww.deleteLater()

        self._feature_left_lay.addWidget(spec.make_left_panel(), 1)

        # Replace right view
        self.shell.set_right_content(spec.make_right_view())

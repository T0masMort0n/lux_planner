from __future__ import annotations

import sys

from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication

from lux.app.navigation import build_default_registry
from lux.core.settings.store import SettingsStore
from lux.data.db import ensure_db_ready
from lux.ui.qt.theme import apply_theme_by_name
from lux.ui.qt.main_window import MainWindow

def run_app() -> None:
    app = QApplication(sys.argv)

    # Ensure shared system DB is initialized + migrated before UI.
    # (Single DB for all modules; features still access it only via repos/services.)
    _conn = ensure_db_ready()

    settings = SettingsStore()
    theme = settings.get_theme()

    # Apply QSS early so the window draws correctly on first show.
    apply_theme_by_name(app, theme_name=theme)

    registry = build_default_registry()

    win = MainWindow(
        settings=settings,
        registry=registry,
        app=app,
    )
    win.show()

    sys.exit(app.exec())


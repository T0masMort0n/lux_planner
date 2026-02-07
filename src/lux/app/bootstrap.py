from __future__ import annotations

import sys

from PySide6.QtWidgets import QApplication

from lux.app.navigation import build_default_registry
from lux.app.services import SystemServices
from lux.core.scheduler.provider_registry import SchedulerProviderRegistry
from lux.core.scheduler.service import SchedulerService
from lux.core.settings.store import SettingsStore
from lux.data.db import ensure_db_ready
from lux.data.repositories.schedule_repo import ScheduledEntryRepo
from lux.ui.qt.main_window import MainWindow
from lux.ui.qt.theme import apply_theme_by_name


def run_app() -> None:
    app = QApplication(sys.argv)

    # Settings must be created in bootstrap (composition root)
    settings = SettingsStore()

    # DB lifecycle is bootstrap-owned (NOT inside services)
    conn = ensure_db_ready()

    # Scheduler system spine (repo injected; registry accessed via service.registry)
    scheduler_repo = ScheduledEntryRepo(conn)
    scheduler_registry = SchedulerProviderRegistry()
    scheduler_service = SchedulerService(repo=scheduler_repo, registry=scheduler_registry)

    services = SystemServices(
        scheduler_service=scheduler_service,
    )

    # Apply theme once we have settings + app
    apply_theme_by_name(
        app=app,
        theme_name=settings.get_theme(),
        font_scale=settings.get_font_scale(),
        font_scheme_id=settings.get_font_scheme_id(),
    )

    registry = build_default_registry()

    win = MainWindow(
        settings=settings,
        registry=registry,
        services=services,
        app=app,
    )
    win.show()

    sys.exit(app.exec())

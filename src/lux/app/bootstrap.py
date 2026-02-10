from __future__ import annotations

import logging
import sys

from PySide6.QtWidgets import QApplication

from lux.app.navigation import build_default_registry
from lux.app.services import SystemServices
from lux.core.scheduler.provider_registry import SchedulerProviderRegistry
from lux.core.scheduler.service import SchedulerService
from lux.core.settings.store import SettingsStore
from lux.data.db import ensure_db_ready
from lux.data.repositories.schedule_repo import ScheduledEntryRepo
from lux.data.repositories.tasks_repo import TasksRepository
from lux.features.tasks.repo import TasksRepo
from lux.features.tasks.service import TasksService
from lux.ui.qt.main_window import MainWindow
import lux.ui.qt.theme as theme_mod

log = logging.getLogger(__name__)



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

    # Tasks feature spine (repo/service constructed here; no feature-owned DB init)
    tasks_repo = TasksRepository(conn)
    tasks_repo_adapter = TasksRepo(tasks_repo)
    tasks_service = TasksService(repo=tasks_repo_adapter)

    services = SystemServices(
        scheduler_service=scheduler_service,
        tasks_service=tasks_service,
    )

    # Apply theme once we have settings + app (SSOT path)
    try:
        theme_mod.apply_theme_by_name(
            app=app,
            theme_name=settings.get_theme(),
            font_scale=settings.get_font_scale(),
            font_scheme_id=settings.get_font_scheme_id(),
        )
    except Exception:
        # Exception-path only diagnostics (no new mechanisms; log only)
        log.exception("Theme application failed")
        log.error("THEME_MODULE_PATH: %s", getattr(theme_mod, "__file__", "<??>"))
        fn = getattr(theme_mod, "apply_theme_by_name", None)
        log.error("THEME_APPLY_FN: %r", fn)
        log.error("THEME_APPLY_CODE: %r", getattr(fn, "__code__", None))
        raise

    registry = build_default_registry()

    win = MainWindow(
        settings=settings,
        registry=registry,
        services=services,
        app=app,
    )
    win.show()

    sys.exit(app.exec())

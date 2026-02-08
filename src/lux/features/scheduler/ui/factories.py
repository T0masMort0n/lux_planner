from __future__ import annotations

from typing import Callable

from PySide6.QtWidgets import QWidget

from lux.app.services import SystemServices
from lux.features.scheduler.ui.day_view import SchedulerDayView
from lux.features.scheduler.ui.panel import SchedulerLeftPanel
from lux.features.scheduler.ui.state import SchedulerState


def make_scheduler_factories() -> tuple[Callable[[SystemServices], QWidget], Callable[[SystemServices], QWidget]]:
    """Return left/right widget factories that share feature-owned state internally.

    System navigation remains dumb: it only holds the returned callables.
    """
    state = SchedulerState()

    def make_left(services: SystemServices) -> QWidget:
        return SchedulerLeftPanel(services.scheduler_service, state)

    def make_right(services: SystemServices) -> QWidget:
        return SchedulerDayView(services.scheduler_service, state)

    return make_left, make_right

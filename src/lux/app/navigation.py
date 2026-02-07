from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from PySide6.QtWidgets import QWidget

from lux.app.services import SystemServices

@dataclass(frozen=True)
class AppModuleSpec:
    key: str                 # "journal"
    title: str               # "Lux Journal"
    make_left_panel: Callable[[SystemServices], QWidget]
    make_right_view: Callable[[SystemServices], QWidget]

def build_default_registry() -> list[AppModuleSpec]:
    # Import here to avoid import cycles at startup.

    # Journal
    from lux.features.journal.ui.panel import JournalLeftPanel
    from lux.features.journal.ui.view import JournalRightView

    # Scheduler
    from lux.features.scheduler.ui.panel import SchedulerLeftPanel
    from lux.features.scheduler.ui.day_view import SchedulerDayView

    # Meals
    from lux.features.meals.ui.panel import MealsLeftPanel
    from lux.features.meals.ui.view import MealsRightView

    # Exercise
    from lux.features.exercise.ui.panel import ExerciseLeftPanel
    from lux.features.exercise.ui.view import ExerciseRightView

    # Goals
    from lux.features.goals.ui.panel import GoalsLeftPanel
    from lux.features.goals.ui.view import GoalsRightView

    # To Do (Inbox / unassigned tasks)
    from lux.features.todo.ui.panel import TodoLeftPanel
    from lux.features.todo.ui.view import TodoRightView

    return [
        AppModuleSpec(
            key="journal",
            title="Lux Journal",
            make_left_panel=lambda services: JournalLeftPanel(),
            make_right_view=lambda services: JournalRightView(),
        ),
        AppModuleSpec(
            key="scheduler",
            title="Lux Scheduler",
            make_left_panel=lambda services: SchedulerLeftPanel(services.scheduler_service),
            make_right_view=lambda services: SchedulerDayView(services.scheduler_service),
        ),
        AppModuleSpec(
            key="meals",
            title="Lux Meals",
            make_left_panel=lambda services: MealsLeftPanel(),
            make_right_view=lambda services: MealsRightView(),
        ),
        AppModuleSpec(
            key="exercise",
            title="Lux Exercise",
            make_left_panel=lambda services: ExerciseLeftPanel(),
            make_right_view=lambda services: ExerciseRightView(),
        ),
        AppModuleSpec(
            key="goals",
            title="Lux Goals",
            make_left_panel=lambda services: GoalsLeftPanel(),
            make_right_view=lambda services: GoalsRightView(),
        ),
        AppModuleSpec(
            key="todo",
            title="Lux To Do",
            make_left_panel=lambda services: TodoLeftPanel(),
            make_right_view=lambda services: TodoRightView(),
        ),
    ]

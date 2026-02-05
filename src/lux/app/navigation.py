from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from PySide6.QtWidgets import QWidget


@dataclass(frozen=True)
class AppModuleSpec:
    key: str                 # "journal"
    title: str               # "Lux Journal"
    make_left_panel: Callable[[], QWidget]
    make_right_view: Callable[[], QWidget]


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
            make_left_panel=lambda: JournalLeftPanel(),
            make_right_view=lambda: JournalRightView(),
        ),
        AppModuleSpec(
            key="scheduler",
            title="Lux Scheduler",
            make_left_panel=lambda: SchedulerLeftPanel(),
            make_right_view=lambda: SchedulerDayView(),
        ),
        AppModuleSpec(
            key="meals",
            title="Lux Meals",
            make_left_panel=lambda: MealsLeftPanel(),
            make_right_view=lambda: MealsRightView(),
        ),
        AppModuleSpec(
            key="exercise",
            title="Lux Exercise",
            make_left_panel=lambda: ExerciseLeftPanel(),
            make_right_view=lambda: ExerciseRightView(),
        ),
        AppModuleSpec(
            key="goals",
            title="Lux Goals",
            make_left_panel=lambda: GoalsLeftPanel(),
            make_right_view=lambda: GoalsRightView(),
        ),
        AppModuleSpec(
            key="todo",
            title="Lux To Do",
            make_left_panel=lambda: TodoLeftPanel(),
            make_right_view=lambda: TodoRightView(),
        ),
    ]

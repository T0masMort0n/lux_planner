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

    # Scheduler (feature-owned shared state is encapsulated inside the feature factory)
    from lux.features.scheduler.ui.factories import make_scheduler_factories

    # Meals
    from lux.features.meals.ui.panel import MealsLeftPanel
    from lux.features.meals.ui.view import MealsRightView

    # Exercise
    from lux.features.exercise.ui.panel import ExerciseLeftPanel
    from lux.features.exercise.ui.view import ExerciseRightView

    # Goals
    from lux.features.goals.ui.panel import GoalsLeftPanel
    from lux.features.goals.ui.view import GoalsRightView

    # Tasks (Inbox / unassigned tasks)
    from lux.features.tasks.ui.panel import TasksLeftPanel
    from lux.features.tasks.ui.view import TasksRightView

    scheduler_left_factory, scheduler_right_factory = make_scheduler_factories()

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
            make_left_panel=scheduler_left_factory,
            make_right_view=scheduler_right_factory,
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
            key="tasks",
            title="Lux Tasks",
            make_left_panel=lambda services: TasksLeftPanel(services=services),
            make_right_view=lambda services: TasksRightView(services=services),
        ),
    ]

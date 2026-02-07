from __future__ import annotations

from dataclasses import dataclass

from lux.core.scheduler.service import SchedulerService


@dataclass(frozen=True)
class SystemServices:
    """
    System-owned service bundle injected into module UI factories.

    Guardrails:
    - No global singletons / service locators.
    - Bootstrapping owns DB lifecycle and constructs services once.
    - Features receive only what they need via injection.
    """
    scheduler_service: SchedulerService

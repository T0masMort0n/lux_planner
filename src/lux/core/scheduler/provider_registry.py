from __future__ import annotations

from typing import Protocol


class SchedulerProvider(Protocol):
    def resolve_label(self, item_ref: str) -> str | None:
        ...


class SchedulerProviderRegistry:
    """System-level registry to resolve labels without feature-to-feature imports."""

    def __init__(self) -> None:
        self._providers: dict[str, SchedulerProvider] = {}

    def register(self, kind: str, provider: SchedulerProvider) -> None:
        kk = str(kind).strip()
        if not kk:
            return
        self._providers[kk] = provider

    def get(self, kind: str) -> SchedulerProvider | None:
        kk = str(kind).strip()
        if not kk:
            return None
        return self._providers.get(kk)

from __future__ import annotations

from datetime import date, datetime
from typing import Any

from lux.core.scheduler.provider_registry import SchedulerProviderRegistry
from lux.data.models.schedule import ScheduledEntryRow
from lux.data.repositories.schedule_repo import ScheduledEntryRepo


def _to_iso(dt: str | datetime | date) -> str:
    if isinstance(dt, datetime):
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    if isinstance(dt, date):
        return datetime(dt.year, dt.month, dt.day, 0, 0, 0).strftime("%Y-%m-%d %H:%M:%S")
    s = str(dt).strip()
    return s.replace("T", " ")


class SchedulerService:
    """
    System write path for scheduled entries.

    Guardrails:
    - UI must never write DB directly.
    - No delete: archive only.
    - Feature-agnostic: item_kind/item_ref only, no foreign keys.
    - DB lifecycle is bootstrap-owned: this service never opens connections.
    """

    def __init__(
        self,
        repo: ScheduledEntryRepo,
        registry: SchedulerProviderRegistry,
    ) -> None:
        self._repo = repo
        self._registry = registry

    @property
    def registry(self) -> SchedulerProviderRegistry:
        return self._registry

    def schedule(
        self,
        item_kind: str,
        item_ref: Any,
        start: str | datetime | date,
        end: str | datetime | date,
        title_cache: str | None = None,
        notes_cache: str | None = None,
    ) -> int:
        kind = str(item_kind or "").strip()
        if not kind:
            raise ValueError("item_kind is required")

        ref = str(item_ref).strip()
        if not ref:
            raise ValueError("item_ref is required")

        start_iso = _to_iso(start)
        end_iso = _to_iso(end)
        if not start_iso or not end_iso:
            raise ValueError("start/end are required")

        # Contract: strict range validity (end must be after start)
        if start_iso >= end_iso:
            raise ValueError("end must be after start")

        entry_id = self._repo.create(
            {
                "item_kind": kind,
                "item_ref": ref,
                "start_dt": start_iso,
                "end_dt": end_iso,
                "title_cache": title_cache,
                "notes_cache": notes_cache,
            }
        )
        return int(entry_id)

    def reschedule(
        self,
        entry_id: int | str,
        new_start: str | datetime | date,
        new_end: str | datetime | date,
    ) -> None:
        try:
            eid = int(entry_id)
        except Exception:
            raise ValueError("entry_id is required")

        start_iso = _to_iso(new_start)
        end_iso = _to_iso(new_end)

        # Contract: strict range validity (end must be after start)
        if start_iso >= end_iso:
            raise ValueError("new_end must be after new_start")

        self._repo.update_time(eid, start_iso, end_iso)

    def archive(self, entry_id: int | str) -> None:
        try:
            eid = int(entry_id)
        except Exception:
            raise ValueError("entry_id is required")
        self._repo.archive(eid)

    def list_range(
        self,
        start: str | datetime | date,
        end: str | datetime | date,
        include_archived: bool = False,
        limit: int = 500,
    ) -> list[ScheduledEntryRow]:
        start_iso = _to_iso(start)
        end_iso = _to_iso(end)

        # For listing, inclusive ranges are acceptable but keep bounded and ordered.
        if start_iso > end_iso:
            raise ValueError("start must be <= end")

        return self._repo.list_for_range(
            start_iso,
            end_iso,
            include_archived=include_archived,
            limit=limit,
        )

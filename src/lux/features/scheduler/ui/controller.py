from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timedelta
from uuid import uuid4

from PySide6.QtCore import QDate, QTime

from lux.core.scheduler.service import SchedulerService


@dataclass(frozen=True)
class SchedulerEntryVM:
    id: int
    start_dt: str
    end_dt: str
    title: str


class SchedulerController:
    """Thin UI adapter over SchedulerService (feature-layer convenience only).

    Guardrails:
    - UI never talks to DB/repo directly.
    - All writes go through SchedulerService.
    - Registry access is only via service.registry.
    - Scheduler-native items use item_kind="adhoc" with uuid4 string refs.
    """

    def __init__(self, service: SchedulerService) -> None:
        self._service = service

    @staticmethod
    def _day_bounds_iso(qd: QDate) -> tuple[str, str]:
        d = date(qd.year(), qd.month(), qd.day())
        start = datetime(d.year, d.month, d.day, 0, 0, 0)
        end = start + timedelta(days=1)
        return (
            start.strftime("%Y-%m-%d %H:%M:%S"),
            end.strftime("%Y-%m-%d %H:%M:%S"),
        )

    @staticmethod
    def _combine_date_time(qd: QDate, qt: QTime) -> str:
        d = date(qd.year(), qd.month(), qd.day())
        dt = datetime(d.year, d.month, d.day, int(qt.hour()), int(qt.minute()), 0)
        return dt.strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def _fmt_time(dt_str: str) -> str:
        try:
            s = str(dt_str).replace("T", " ")
            return s.split(" ")[1][:5]
        except Exception:
            return ""

    def _resolve_title(self, item_kind: str, item_ref: str, title_cache: str | None) -> str:
        kind = str(item_kind or "").strip()

        # Scheduler-native adhoc entries: always use title_cache (no provider required).
        if kind == "adhoc":
            return (title_cache or "").strip() or "Scheduled Item"

        provider = self._service.registry.get(kind)
        if provider is not None:
            try:
                label = provider.resolve_label(str(item_ref))
                if label:
                    return str(label)
            except Exception:
                pass

        return (title_cache or "").strip() or "Scheduled Item"

    def list_entries_for_date(self, qd: QDate) -> list[SchedulerEntryVM]:
        start, end = self._day_bounds_iso(qd)
        entries = self._service.list_range(start, end, include_archived=False)

        out: list[SchedulerEntryVM] = []
        for e in entries:
            title = self._resolve_title(e.item_kind, e.item_ref, getattr(e, "title_cache", None))
            out.append(
                SchedulerEntryVM(
                    id=int(e.id),
                    start_dt=str(e.start_dt),
                    end_dt=str(e.end_dt),
                    title=title,
                )
            )
        return out

    def create_adhoc(
        self,
        qd: QDate,
        title: str,
        start_time: QTime,
        end_time: QTime,
        notes: str | None = None,
    ) -> int:
        ttl = (title or "").strip()
        if not ttl:
            raise ValueError("title is required")

        start_iso = self._combine_date_time(qd, start_time)
        end_iso = self._combine_date_time(qd, end_time)

        entry_id = self._service.schedule(
            item_kind="adhoc",
            item_ref=str(uuid4()),
            start=start_iso,
            end=end_iso,
            title_cache=ttl,
            notes_cache=notes,
        )
        return int(entry_id)

    def reschedule_entry(
        self,
        entry_id: int,
        qd: QDate,
        new_start_time: QTime,
        new_end_time: QTime,
    ) -> None:
        start_iso = self._combine_date_time(qd, new_start_time)
        end_iso = self._combine_date_time(qd, new_end_time)
        self._service.reschedule(int(entry_id), start_iso, end_iso)

    def archive_entry(self, entry_id: int) -> None:
        self._service.archive(int(entry_id))

    def format_time_range(self, start_dt: str, end_dt: str) -> str:
        a = self._fmt_time(start_dt)
        b = self._fmt_time(end_dt)
        if a and b:
            return f"{a}–{b}"
        return a or b or ""

from __future__ import annotations

from datetime import date, datetime, timedelta

from PySide6.QtCore import QDate

from lux.core.scheduler.service import SchedulerService


class SchedulerController:
    """
    UI-facing controller for the Scheduler feature.

    Phase 0 scope:
    - Read-only UI surface that queries SchedulerService for a day-range.
    - No scheduling/rescheduling actions are exposed to UI yet.
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
    def _fmt_time(dt_str: str) -> str:
        # Expecting "YYYY-MM-DD HH:MM:SS" (or ISO-ish). Keep fail-soft.
        try:
            s = dt_str.replace("T", " ")
            return s.split(" ")[1][:5]
        except Exception:
            return ""

    def list_entries_for_date(self, qd: QDate) -> list[str]:
        start, end = self._day_bounds_iso(qd)
        entries = self._service.list_range(start, end)

        out: list[str] = []
        for e in entries:
            t = self._fmt_time(e.start_dt)
            title = self._service.resolve_display_title(e)
            out.append(f"{t} · {title}" if t else title)
        return out

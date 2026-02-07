from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(frozen=True)
class ScheduledEntryRow:
    id: int
    item_kind: str
    item_ref: str
    start_dt: str
    end_dt: str
    title_cache: Optional[str]
    notes_cache: Optional[str]
    archived: bool
    created_at: str
    updated_at: str


def bool_from_int(v: object) -> bool:
    try:
        return int(v) == 1
    except Exception:
        return False


def now_sqlite() -> str:
    return datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

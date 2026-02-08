from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(frozen=True)
class TaskDefinitionRow:
    id: int
    title: str
    notes: str
    parent_task_id: Optional[int]
    archived: bool
    created_at: str
    updated_at: str


@dataclass(frozen=True)
class TaskOccurrenceRow:
    id: int
    task_id: int
    due_date: str                 # YYYY-MM-DD
    due_time: Optional[str]       # HH:MM or None
    sort_key: int
    completed_at: Optional[str]   # ISO-ish sqlite datetime string
    archived: bool
    created_at: str
    updated_at: str


@dataclass(frozen=True)
class TaskOccurrenceJoinedRow:
    """
    Occurrence joined to its definition so UI/services can avoid N+1 task lookups.
    """
    id: int
    task_id: int
    title: str
    notes: str
    due_date: str
    due_time: Optional[str]
    sort_key: int
    completed_at: Optional[str]
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

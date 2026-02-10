from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class TaskDefinition:
    id: int
    title: str
    notes: str = ""
    archived: bool = False


@dataclass(frozen=True)
class TaskOccurrence:
    id: int
    task_id: int
    title: str
    due_date: str                  # YYYY-MM-DD
    due_time: Optional[str] = None # HH:MM or None
    completed: bool = False
    archived: bool = False

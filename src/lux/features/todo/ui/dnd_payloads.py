from __future__ import annotations

"""
To‑Do drag‑and‑drop payload helpers.

This module lives in the To‑Do feature layer and provides thin wrappers around
the system drag‑and‑drop payload constructor. By keeping these helpers in
feature code, we avoid polluting the system drag module with feature‑specific
knowledge, while still offering convenient constructors for To‑Do UI code.
"""

from lux.ui.qt.dragdrop import LuxDragPayload, make_payload


def make_task_definition_payload(task_id: int) -> LuxDragPayload:
    """Build a payload for dragging a task definition."""
    return make_payload("task_definition", {"task_id": task_id})


def make_task_occurrence_payload(occurrence_id: int) -> LuxDragPayload:
    """Build a payload for dragging a task occurrence."""
    return make_payload("task_occurrence", {"occurrence_id": occurrence_id})


__all__ = [
    "make_task_definition_payload",
    "make_task_occurrence_payload",
]

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import json
import uuid
from typing import Any, Optional

from PySide6.QtCore import QEvent, QObject, QMimeData, Qt
from PySide6.QtGui import QDrag, QKeyEvent
from PySide6.QtWidgets import QApplication, QWidget


MIME_LUX_DND = "application/x-lux-dnd+json"
_PAYLOAD_VERSION = 1


@dataclass(frozen=True)
class LuxDragPayload:
    """
    Canonical system-owned payload format for drag & drop.

    Mechanics-only:
    - No feature imports
    - No feature-specific constructors
    - Single decode path (decode_mime)
    """
    kind: str
    data: dict[str, Any]


class DragResult(str, Enum):
    COMPLETED = "completed"
    CANCELED_ESCAPE = "canceled_escape"
    CANCELED_RESIZE = "canceled_resize"
    IGNORED = "ignored"  # invalid drop / dropped nowhere / no-op


def make_payload(kind: str, data: dict[str, Any]) -> LuxDragPayload:
    """
    Feature-agnostic constructor. Features define their own helpers if desired.
    """
    return LuxDragPayload(kind=str(kind), data=dict(data))


def encode_payload(payload: LuxDragPayload, session_id: str) -> bytes:
    blob = {
        "v": _PAYLOAD_VERSION,
        "session": session_id,
        "kind": payload.kind,
        "data": payload.data,
    }
    return json.dumps(blob, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def decode_payload_bytes(raw: bytes) -> Optional[LuxDragPayload]:
    try:
        if not raw:
            return None
        blob = json.loads(raw.decode("utf-8"))
        if int(blob.get("v", 0)) != _PAYLOAD_VERSION:
            return None
        session = str(blob.get("session", ""))
        if not session:
            return None
        kind = str(blob.get("kind", ""))
        data = blob.get("data", None)
        if not kind or not isinstance(data, dict):
            return None
        return LuxDragPayload(kind=kind, data=data)
    except Exception:
        return None


def decode_mime(mime: QMimeData) -> Optional[LuxDragPayload]:
    """
    Single canonical decode path. Drop targets must not parse payloads ad hoc.
    """
    try:
        if not mime or not mime.hasFormat(MIME_LUX_DND):
            return None
        raw = bytes(mime.data(MIME_LUX_DND))
        return decode_payload_bytes(raw)
    except Exception:
        return None


def is_supported_drop(mime: QMimeData) -> bool:
    return decode_mime(mime) is not None


class _DragCancelFilter(QObject):
    """
    Session-local cancellation:
    - No module-level shared state.
    - On cancel, clear the mime payload so decode_mime() returns None everywhere.
    """

    def __init__(self, mime: QMimeData) -> None:
        super().__init__()
        self._mime = mime
        self.cancel_reason: DragResult | None = None

    def _cancel(self, reason: DragResult) -> None:
        self.cancel_reason = reason
        try:
            self._mime.setData(MIME_LUX_DND, b"")
        except Exception:
            pass

    def eventFilter(self, obj: QObject, event: QEvent) -> bool:  # noqa: N802 (Qt override)
        et = event.type()

        if et == QEvent.KeyPress:
            try:
                ke = event  # type: ignore[assignment]
                if isinstance(ke, QKeyEvent) and ke.key() == Qt.Key_Escape:
                    self._cancel(DragResult.CANCELED_ESCAPE)
                    return True
            except Exception:
                return False

        if et == QEvent.Resize:
            self._cancel(DragResult.CANCELED_RESIZE)
            return False

        return False


def start_system_drag(source: QWidget, payload: LuxDragPayload) -> DragResult:
    """
    System-owned drag start helper.

    Safe-release behaviors:
    - ESC cancels (payload cleared)
    - resize cancels (payload cleared)
    - invalid drop / drop nowhere => IGNORED
    """
    app = QApplication.instance()
    if app is None:
        return DragResult.IGNORED

    session_id = str(uuid.uuid4())

    drag = QDrag(source)
    mime = QMimeData()
    mime.setData(MIME_LUX_DND, encode_payload(payload, session_id))
    drag.setMimeData(mime)

    cancel_filter = _DragCancelFilter(mime)
    app.installEventFilter(cancel_filter)

    try:
        action = drag.exec(Qt.CopyAction | Qt.MoveAction)
    finally:
        try:
            app.removeEventFilter(cancel_filter)
        except Exception:
            pass

    if cancel_filter.cancel_reason is not None:
        return cancel_filter.cancel_reason

    if action == Qt.IgnoreAction:
        return DragResult.IGNORED

    return DragResult.COMPLETED

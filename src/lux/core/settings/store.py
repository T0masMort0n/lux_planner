from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path

from lux.app.config import app_data_dir
from lux.core.settings.schema import THEME_DEFAULT, THEMES_AVAILABLE, FONT_SCHEME_DEFAULT


FONT_SCALE_DEFAULT = 1.00
FONT_SCALE_MIN = 0.85
FONT_SCALE_MAX = 1.50

_SAFE_SCHEME_ID_RE = re.compile(r"^[a-z0-9_-]+$")


@dataclass
class SettingsData:
    theme: str = THEME_DEFAULT
    font_scale: float = FONT_SCALE_DEFAULT
    font_scheme_id: str = FONT_SCHEME_DEFAULT


class SettingsStore:
    def __init__(self) -> None:
        self._path = self._settings_path()
        self._data = self._load()

    def _settings_path(self) -> Path:
        return app_data_dir("Lux Planner") / "settings.json"

    def _load(self) -> SettingsData:
        if not self._path.exists():
            return SettingsData()

        try:
            raw = json.loads(self._path.read_text(encoding="utf-8"))
            theme = str(raw.get("theme", THEME_DEFAULT)).strip().lower()
            if theme not in THEMES_AVAILABLE:
                theme = THEME_DEFAULT

            font_scale_raw = raw.get("font_scale", FONT_SCALE_DEFAULT)
            try:
                font_scale = float(font_scale_raw)
            except Exception:
                font_scale = FONT_SCALE_DEFAULT
            font_scale = max(FONT_SCALE_MIN, min(FONT_SCALE_MAX, font_scale))

            scheme_raw = raw.get("font_scheme_id", FONT_SCHEME_DEFAULT)
            scheme = str(scheme_raw).strip().lower()
            if not _SAFE_SCHEME_ID_RE.match(scheme):
                scheme = FONT_SCHEME_DEFAULT

            return SettingsData(theme=theme, font_scale=font_scale, font_scheme_id=scheme)
        except Exception:
            return SettingsData()

    def _save(self) -> None:
        payload = {
            "theme": self._data.theme,
            "font_scale": float(self._data.font_scale),
            "font_scheme_id": self._data.font_scheme_id,
        }
        self._path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    def get_theme(self) -> str:
        return self._data.theme

    def set_theme(self, theme: str) -> None:
        t = str(theme).strip().lower()
        if t not in THEMES_AVAILABLE:
            return
        self._data.theme = t
        self._save()

    def get_font_scheme_id(self) -> str:
        return self._data.font_scheme_id

    def set_font_scheme_id(self, scheme_id: str) -> None:
        sid = str(scheme_id).strip().lower()
        if not _SAFE_SCHEME_ID_RE.match(sid):
            return
        self._data.font_scheme_id = sid
        self._save()

    def get_font_scale(self) -> float:
        return float(self._data.font_scale)

    def set_font_scale(self, scale: float) -> None:
        try:
            v = float(scale)
        except Exception:
            return
        v = max(FONT_SCALE_MIN, min(FONT_SCALE_MAX, v))
        self._data.font_scale = v
        self._save()

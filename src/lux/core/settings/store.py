from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from lux.app.config import app_data_dir
from lux.core.settings.schema import THEME_DEFAULT, THEMES_AVAILABLE


@dataclass
class SettingsData:
    theme: str = THEME_DEFAULT


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
            return SettingsData(theme=theme)
        except Exception:
            return SettingsData()

    def _save(self) -> None:
        payload = {"theme": self._data.theme}
        self._path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    def get_theme(self) -> str:
        return self._data.theme

    def set_theme(self, theme: str) -> None:
        t = str(theme).strip().lower()
        if t not in THEMES_AVAILABLE:
            return
        self._data.theme = t
        self._save()

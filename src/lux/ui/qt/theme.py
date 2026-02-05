from __future__ import annotations

from pathlib import Path

from PySide6.QtWidgets import QApplication

from lux.app.config import repo_root_from_file
from lux.core.settings.schema import THEMES_AVAILABLE, THEME_DEFAULT


def _themes_dir() -> Path:
    root = repo_root_from_file(__file__)
    return root / "assets" / "themes"


def apply_theme_by_name(app: QApplication, theme_name: str) -> None:
    theme = (theme_name or "").strip().lower()
    if theme not in THEMES_AVAILABLE:
        theme = THEME_DEFAULT

    qss_path = _themes_dir() / f"{theme}.qss"
    if not qss_path.exists():
        # Fail soft: clear stylesheet instead of crashing.
        app.setStyleSheet("")
        return

    qss = qss_path.read_text(encoding="utf-8")
    app.setStyleSheet(qss)

from __future__ import annotations

import os
from pathlib import Path


def app_data_dir(app_name: str = "Lux Planner") -> Path:
    """
    Cross-platform-ish app data location.
    Windows: %APPDATA%/Lux Planner
    macOS/Linux: ~/.config/Lux Planner
    """
    if os.name == "nt":
        base = Path(os.environ.get("APPDATA", Path.home()))
    else:
        base = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))
    p = base / app_name
    p.mkdir(parents=True, exist_ok=True)
    return p


def repo_root_from_file(__file_path: str) -> Path:
    """
    Locate repo root relative to src/lux/app/config.py:
      src/lux/app/config.py -> repo root is 4 parents up.
    """
    return Path(__file_path).resolve().parents[4]

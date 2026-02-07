from __future__ import annotations

import json
import logging
import re
import sys
from pathlib import Path

from PySide6.QtGui import QFontDatabase
from PySide6.QtWidgets import QApplication

from lux.app.config import repo_root_from_file
from lux.core.settings.schema import FONT_SCHEME_DEFAULT, THEME_DEFAULT, THEMES_AVAILABLE

log = logging.getLogger(__name__)

# ----------------------------
# Asset path resolution
# ----------------------------


def _asset_root() -> Path:
    """
    Resolve the app's asset root in both dev and packaged builds.

    Dev: repo_root/assets
    Packaged (PyInstaller-style): sys._MEIPASS/assets (if present)
    """
    meipass = getattr(sys, "_MEIPASS", None)
    if meipass:
        return Path(meipass) / "assets"
    return repo_root_from_file(__file__) / "assets"


def _themes_dir() -> Path:
    return _asset_root() / "themes"


def _fonts_dir() -> Path:
    return _asset_root() / "fonts"


def _font_schemes_dir() -> Path:
    return _asset_root() / "font_schemes"


# ----------------------------
# Bundled font registration
# ----------------------------
_FONTS_LOADED = False


def _load_app_fonts() -> None:
    """
    Register all app-bundled fonts (ttf/otf) from assets/fonts so QSS can refer to them by family name.

    Guardrails:
    - Run once per app lifecycle (module-level idempotent guard).
    - Bounded scan (only assets/fonts).
    - Deterministic ordering.
    - Fail-soft: registration failures never block startup/theme application.
    - Single summary log line (no per-file spam).
    """
    global _FONTS_LOADED
    if _FONTS_LOADED:
        return

    fonts_root = _fonts_dir()
    loaded = 0
    failed = 0

    if fonts_root.exists():
        # Deterministic order helps debugging / packaged parity.
        files: list[Path] = []
        for ext in ("*.ttf", "*.otf"):
            files.extend(fonts_root.rglob(ext))

        for p in sorted(set(files), key=lambda x: str(x).lower()):
            try:
                font_id = QFontDatabase.addApplicationFont(str(p))
                if int(font_id) >= 0:
                    loaded += 1
                else:
                    failed += 1
            except Exception:
                failed += 1

    _FONTS_LOADED = True
    log.debug(
        "Font registration complete: loaded=%d failed=%d root=%s",
        loaded,
        failed,
        str(fonts_root),
    )


# ----------------------------
# Typography token substitution / font schemes
# ----------------------------

# Scheme id sanitization: keep exactly as specified.
_SAFE_SCHEME_ID_RE = re.compile(r"^[a-z0-9_-]+$")

# System-owned typography token interface (contract).
TYPO_TOKENS = {
    "--font-ui",
    "--font-body",
    "--font-heading",
    "--font-mono",
    "--font-micro",
}

# Qt-compatible substitution target:
# Only substitute inside font-family declarations and only for var(--font-*) forms.
_FONT_FAMILY_VAR_RE = re.compile(
    r"(font-family\s*:\s*)var\(\s*(--font-(?:ui|body|heading|mono|micro))\s*\)",
    re.IGNORECASE,
)


def _sanitize_font_scheme_id(scheme_id: str | None) -> str | None:
    sid = (scheme_id or "").strip().lower()
    if not sid:
        return None
    if not _SAFE_SCHEME_ID_RE.match(sid):
        return None
    return sid


def list_available_font_schemes() -> list[tuple[str, str]]:
    """Return [(id, label)] from assets/font_schemes/*.json. Fail-soft / bounded."""
    root = _font_schemes_dir()
    if not root.exists():
        return []

    out: list[tuple[str, str]] = []
    for p in sorted(root.glob("*.json"), key=lambda x: str(x).lower()):
        sid = _sanitize_font_scheme_id(p.stem)
        if not sid:
            continue
        label = sid
        try:
            raw = json.loads(p.read_text(encoding="utf-8"))
            label_raw = raw.get("label")
            if isinstance(label_raw, str) and label_raw.strip():
                label = label_raw.strip()
        except Exception:
            # Ignore unreadable schemes; keep scanning.
            continue
        out.append((sid, label))
    return out


def _load_font_scheme_mapping(font_scheme_id: str | None) -> dict[str, str]:
    sid = _sanitize_font_scheme_id(font_scheme_id) or _sanitize_font_scheme_id(FONT_SCHEME_DEFAULT)
    if not sid:
        return {}

    path = _font_schemes_dir() / f"{sid}.json"
    if not path.exists():
        return {}

    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}

    fonts = raw.get("fonts")
    if not isinstance(fonts, dict):
        return {}

    out: dict[str, str] = {}
    for k, v in fonts.items():
        if not isinstance(k, str) or not isinstance(v, str):
            continue

        # Required: normalize keys so scheme application is deterministic.
        kk = str(k).strip().lower()
        vv = str(v).strip()

        # Required: only allow approved system typography tokens.
        if kk not in TYPO_TOKENS:
            continue
        if not vv:
            continue

        out[kk] = vv

    return out


def _substitute_typography_tokens(qss: str, token_to_family: dict[str, str]) -> str:
    """
    Qt stylesheets do not reliably support CSS custom properties or var().

    System safety rules:
    - Only substitute var(--font-*) inside font-family declarations.
    - Never perform global string replacement.
    - Unknown tokens remain untouched.
    """
    if not qss or not token_to_family:
        return qss

    def repl(m: re.Match) -> str:
        prefix = m.group(1)  # 'font-family:'
        token = m.group(2)   # '--font-body' etc (case-insensitive match)
        token_norm = token.lower()
        value = token_to_family.get(token_norm)
        if not value:
            return m.group(0)
        return f"{prefix}{value}"

    return _FONT_FAMILY_VAR_RE.sub(repl, qss)


def _apply_font_scale_to_qss(qss: str, font_scale: float) -> str:
    try:
        scale = float(font_scale)
    except Exception:
        scale = 1.0

    # Clamp hard to avoid unreadable extremes.
    scale = max(0.70, min(2.00, scale))

    def repl(m: re.Match) -> str:
        px = int(m.group(1))
        scaled = int(round(px * scale))
        scaled = max(9, min(64, scaled))
        return f"font-size: {scaled}px;"

    return re.sub(r"font-size:\s*(\d+)px\s*;", repl, qss)


def apply_theme_by_name(
    app: QApplication,
    theme_name: str,
    font_scale: float = 1.0,
    font_scheme_id: str | None = None,
) -> None:
    # Ensure packaged/app-local fonts are available to QSS before styles apply.
    _load_app_fonts()

    theme = (theme_name or "").strip().lower()
    if theme not in THEMES_AVAILABLE:
        theme = THEME_DEFAULT

    qss_path = _themes_dir() / f"{theme}.qss"
    if not qss_path.exists():
        # Fail soft: clear stylesheet instead of crashing.
        app.setStyleSheet("")
        return

    qss = qss_path.read_text(encoding="utf-8")
    qss = _apply_font_scale_to_qss(qss, font_scale=font_scale)

    mapping = _load_font_scheme_mapping(font_scheme_id)
    qss = _substitute_typography_tokens(qss, mapping)

    # NOTE: Scheme info is comment-only for debugging; no CSS var overlay emitted.
    sid = _sanitize_font_scheme_id(font_scheme_id) or _sanitize_font_scheme_id(FONT_SCHEME_DEFAULT) or ""
    if sid:
        qss = f"/* font-scheme: {sid} */\n" + qss

    app.setStyleSheet(qss)

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QComboBox,
    QStackedWidget,
)

from lux.core.settings.schema import THEMES_AVAILABLE
from lux.core.settings.store import SettingsStore
from lux.ui.qt.theme import list_available_font_schemes


@dataclass(frozen=True)
class SettingsCallbacks:
    apply_theme: Callable[[], None]
    apply_font_scale: Callable[[], None]


class SettingsLeftPanel(QWidget):
    def __init__(self, on_select_category: Callable[[str], None], parent=None) -> None:
        super().__init__(parent)
        self._on_select_category = on_select_category

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(12)

        lbl = QLabel("Settings")
        lbl.setObjectName("MetaCaption")
        root.addWidget(lbl)

        for title, key in [
            ("Appearance", "appearance"),
            ("Shortcuts", "shortcuts"),
            ("Notifications", "notifications"),
            ("About", "about"),
        ]:
            b = _list_item_button(title)
            b.pressed.connect(lambda k=key: self._on_select_category(k))
            root.addWidget(b)

        root.addStretch(1)


class SettingsRightView(QWidget):
    def __init__(self, settings: SettingsStore, callbacks: SettingsCallbacks, parent=None) -> None:
        super().__init__(parent)
        self._settings = settings
        self._callbacks = callbacks

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(12)

        title = QLabel("Settings")
        title.setObjectName("TitleUnified")
        root.addWidget(title)

        meta = QLabel("System-wide preferences (features inherit).")
        meta.setObjectName("MetaCaption")
        root.addWidget(meta)

        self._stack = QStackedWidget()
        root.addWidget(self._stack, 1)

        self._stack.addWidget(self._build_appearance_page())     # 0
        self._stack.addWidget(self._build_shortcuts_page())      # 1
        self._stack.addWidget(self._build_notifications_page())  # 2
        self._stack.addWidget(self._build_about_page())          # 3

        self.show_category("appearance")

    def show_category(self, key: str) -> None:
        k = (key or "").strip().lower()
        mapping = {
            "appearance": 0,
            "shortcuts": 1,
            "notifications": 2,
            "about": 3,
        }
        self._stack.setCurrentIndex(mapping.get(k, 0))

    def _build_appearance_page(self) -> QWidget:
        w = QWidget()
        lay = QVBoxLayout(w)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(12)

        # Theme row
        theme_row = QWidget()
        t_lay = QHBoxLayout(theme_row)
        t_lay.setContentsMargins(0, 0, 0, 0)
        t_lay.setSpacing(10)

        theme_lbl = QLabel("Theme")
        theme_lbl.setObjectName("MetaCaption")

        theme_combo = QComboBox()
        theme_combo.addItems(THEMES_AVAILABLE)
        theme_combo.setCurrentText(self._settings.get_theme())
        theme_combo.currentTextChanged.connect(self._on_theme_changed)

        t_lay.addWidget(theme_lbl)
        t_lay.addWidget(theme_combo, 1)
        lay.addWidget(theme_row)

        # Font scheme row
        scheme_row = QWidget()
        fs_lay = QHBoxLayout(scheme_row)
        fs_lay.setContentsMargins(0, 0, 0, 0)
        fs_lay.setSpacing(10)

        scheme_lbl = QLabel("Font scheme")
        scheme_lbl.setObjectName("MetaCaption")

        scheme_combo = QComboBox()
        schemes = list_available_font_schemes()
        if not schemes:
            # Fail-soft: keep UI usable even if assets are missing.
            schemes = [("default", "Default")]
        for sid, label in schemes:
            scheme_combo.addItem(label, userData=sid)

        current_sid = getattr(self._settings, "get_font_scheme_id", lambda: "default")()
        # select by userData
        for i in range(scheme_combo.count()):
            if str(scheme_combo.itemData(i)) == str(current_sid):
                scheme_combo.setCurrentIndex(i)
                break
        scheme_combo.currentIndexChanged.connect(lambda _i: self._on_font_scheme_changed(scheme_combo))

        fs_lay.addWidget(scheme_lbl)
        fs_lay.addWidget(scheme_combo, 1)
        lay.addWidget(scheme_row)

        # Interface scale row
        scale_row = QWidget()
        s_lay = QHBoxLayout(scale_row)
        s_lay.setContentsMargins(0, 0, 0, 0)
        s_lay.setSpacing(10)

        scale_lbl = QLabel("Interface scale")
        scale_lbl.setObjectName("MetaCaption")

        scale_combo = QComboBox()
        options: list[tuple[str, float]] = [
            ("90%", 0.90),
            ("100%", 1.00),
            ("110%", 1.10),
            ("125%", 1.25),
        ]
        for label, _v in options:
            scale_combo.addItem(label)

        current = float(self._settings.get_font_scale())
        best_idx = 1
        best_dist = 999.0
        for i, (_label, v) in enumerate(options):
            d = abs(current - float(v))
            if d < best_dist:
                best_dist = d
                best_idx = i
        scale_combo.setCurrentIndex(best_idx)
        scale_combo.currentIndexChanged.connect(lambda idx: self._on_scale_changed(int(idx), options))

        s_lay.addWidget(scale_lbl)
        s_lay.addWidget(scale_combo, 1)
        lay.addWidget(scale_row)

        help_lbl = QLabel("Applies across the entire app. Features inherit system typography.")
        help_lbl.setObjectName("MetaCaption")
        help_lbl.setWordWrap(True)
        lay.addWidget(help_lbl)

        lay.addStretch(1)
        return w

    def _build_shortcuts_page(self) -> QWidget:
        return _placeholder_page(
            "Shortcuts",
            [
                "MVP: view-only placeholder.",
                "Esc — Close overlay / dialogs",
            ],
        )

    def _build_notifications_page(self) -> QWidget:
        return _placeholder_page(
            "Notifications",
            [
                "MVP: not implemented yet.",
                "Global notification preferences will live here.",
            ],
        )

    def _build_about_page(self) -> QWidget:
        return _placeholder_page(
            "About",
            [
                "Lux Planner — MVP",
                f"Theme: {self._settings.get_theme()}",
                f"Interface scale: {self._settings.get_font_scale():.2f}",
                f'Font scheme: {getattr(self._settings, "get_font_scheme_id", lambda: "default")()}',
            ],
        )

    def _on_theme_changed(self, theme: str) -> None:
        self._settings.set_theme(theme)
        self._callbacks.apply_theme()

    def _on_font_scheme_changed(self, combo: QComboBox) -> None:
        try:
            sid = str(combo.currentData()).strip().lower()
        except Exception:
            return

        # SettingsStore validates scheme id; fail-soft if invalid.
        setter = getattr(self._settings, "set_font_scheme_id", None)
        if callable(setter):
            setter(sid)
        self._callbacks.apply_theme()

    def _on_scale_changed(self, idx: int, options: list[tuple[str, float]]) -> None:
        try:
            _label, scale = options[int(idx)]
        except Exception:
            return

        self._settings.set_font_scale(float(scale))
        QTimer.singleShot(0, self._callbacks.apply_font_scale)


def _list_item_button(text: str) -> QWidget:
    from lux.ui.qt.widgets.buttons import LuxButton

    b = LuxButton(text)
    b.setMinimumHeight(40)
    return b


def _placeholder_page(title: str, lines: list[str]) -> QWidget:
    w = QWidget()
    lay = QVBoxLayout(w)
    lay.setContentsMargins(0, 0, 0, 0)
    lay.setSpacing(10)

    t = QLabel(title)
    t.setObjectName("TitleUnified")
    lay.addWidget(t)

    for s in lines:
        lbl = QLabel(s)
        lbl.setObjectName("MetaCaption")
        lbl.setWordWrap(True)
        lay.addWidget(lbl)

    lay.addStretch(1)
    return w

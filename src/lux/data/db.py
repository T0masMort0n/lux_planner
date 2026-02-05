from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Iterable

from lux.app.config import app_data_dir


def db_path(app_name: str = "Lux Planner", filename: str = "planner.db") -> Path:
    """
    Single shared DB for the whole system.
    """
    return app_data_dir(app_name) / filename


def connect(path: Path | None = None) -> sqlite3.Connection:
    p = path or db_path()
    conn = sqlite3.connect(str(p))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.execute("PRAGMA journal_mode = WAL;")
    conn.execute("PRAGMA synchronous = NORMAL;")
    return conn


def _migrations_dir() -> Path:
    # src/lux/data/db.py -> src/lux/data/migrations
    return Path(__file__).resolve().parent / "migrations"


def _ensure_migrations_table(conn: sqlite3.Connection) -> None:
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS lux_migrations (
            filename TEXT PRIMARY KEY,
            applied_at TEXT NOT NULL DEFAULT (datetime('now'))
        );
        """
    )


def _iter_migration_files() -> Iterable[Path]:
    d = _migrations_dir()
    if not d.exists():
        return []
    # files like 0001_init.sql, 0002_journal.sql, ...
    return sorted([p for p in d.glob("*.sql") if p.is_file()])


def apply_migrations(conn: sqlite3.Connection) -> None:
    """
    Apply all SQL migrations in lexicographic order, exactly once each.

    NOTE:
    - This is intentionally simple and deterministic.
    - No heavy work at startup beyond running unapplied migrations.
    """
    _ensure_migrations_table(conn)

    applied = {
        row["filename"]
        for row in conn.execute("SELECT filename FROM lux_migrations").fetchall()
    }

    for path in _iter_migration_files():
        if path.name in applied:
            continue

        sql = path.read_text(encoding="utf-8").strip()
        if not sql:
            # Allow empty placeholders without breaking startup
            conn.execute(
                "INSERT INTO lux_migrations(filename) VALUES (?)",
                (path.name,),
            )
            conn.commit()
            continue

        conn.executescript(sql)
        conn.execute(
            "INSERT INTO lux_migrations(filename) VALUES (?)",
            (path.name,),
        )
        conn.commit()


def ensure_db_ready() -> sqlite3.Connection:
    """
    Convenience: open connection + run migrations.
    Returns a ready-to-use connection.
    """
    conn = connect()
    apply_migrations(conn)
    return conn

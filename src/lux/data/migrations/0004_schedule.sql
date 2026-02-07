-- 0004_schedule.sql
-- Phase 0 Scheduler core table (system-owned, feature-agnostic)

CREATE TABLE IF NOT EXISTS scheduled_entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_kind TEXT NOT NULL,
    item_ref TEXT NOT NULL,
    start_dt TEXT NOT NULL,
    end_dt TEXT NOT NULL,
    title_cache TEXT,
    notes_cache TEXT,
    archived INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_scheduled_entries_start_dt ON scheduled_entries(start_dt);
CREATE INDEX IF NOT EXISTS idx_scheduled_entries_end_dt ON scheduled_entries(end_dt);
CREATE INDEX IF NOT EXISTS idx_scheduled_entries_range ON scheduled_entries(start_dt, end_dt);
CREATE INDEX IF NOT EXISTS idx_scheduled_entries_archived ON scheduled_entries(archived);

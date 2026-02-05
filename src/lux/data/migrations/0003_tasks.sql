-- 0003_tasks.sql
-- Tasks are definitions; occurrences are instances.
-- Completion lives on occurrences (not on definitions).

CREATE TABLE IF NOT EXISTS task_definitions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  notes TEXT NOT NULL DEFAULT '',
  archived INTEGER NOT NULL DEFAULT 0, -- 0/1
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);

-- One row per scheduled instance (date/time).
-- For recurring tasks, the app/service generates occurrences ahead of time.
CREATE TABLE IF NOT EXISTS task_occurrences (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  task_id INTEGER NOT NULL,
  due_date TEXT NOT NULL,             -- YYYY-MM-DD
  due_time TEXT NULL,                 -- HH:MM (24h) optional
  sort_key INTEGER NOT NULL DEFAULT 0, -- stable ordering within a day
  completed_at TEXT NULL,             -- datetime('now') when completed
  archived INTEGER NOT NULL DEFAULT 0, -- 0/1
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  updated_at TEXT NOT NULL DEFAULT (datetime('now')),
  FOREIGN KEY(task_id) REFERENCES task_definitions(id) ON DELETE RESTRICT
);

CREATE INDEX IF NOT EXISTS idx_task_occ_due_date ON task_occurrences(due_date);
CREATE INDEX IF NOT EXISTS idx_task_occ_task_id ON task_occurrences(task_id);
CREATE INDEX IF NOT EXISTS idx_task_occ_completed ON task_occurrences(completed_at);

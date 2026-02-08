-- 0005_task_hierarchy.sql
-- Phase 1 To-Do hierarchy (definition-only; occurrences do not form a hierarchy)

-- NOTE: SQLite ALTER TABLE ADD COLUMN runs once via lux_migrations tracking.
ALTER TABLE task_definitions
ADD COLUMN parent_task_id INTEGER NULL;

CREATE INDEX IF NOT EXISTS idx_task_def_parent_task_id
ON task_definitions(parent_task_id);

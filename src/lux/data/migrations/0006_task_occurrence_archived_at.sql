-- 0006_task_occurrence_archived_at.sql
-- Adds archived_at timestamp to task_occurrences for consistent archival metadata.
-- Timestamp contract: values are UTC strings written by repositories via now_sqlite().

ALTER TABLE task_occurrences
ADD COLUMN archived_at TEXT NULL;

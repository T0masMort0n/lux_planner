
# UPDATED IMPLEMENTATION LOG — To‑Do Phase 1

## Objective
Bring To‑Do feature into alignment with Lux System Contracts without introducing new system‑wide mechanisms.

---

## Implementation Steps

### Step 1 — Hierarchy Data Support
- Added DB migration for `parent_task_id`
- Updated data model and repo mappings

### Step 2 — Repository Stabilization
- Rebuilt truncated `tasks_repo.py`
- Added occurrence reschedule method
- Ensured bounded queries and JOIN usage

### Step 3 — Lifecycle Integrity
- Removed DB creation from To‑Do service
- Moved ownership to bootstrap
- Injected service via `SystemServices`

### Step 4 — System Drag & Drop Framework
Created minimal system DnD module providing:
- Typed payload contract
- Single decode path
- Session‑local cancel logic
- Result enum for deterministic behavior

No feature logic included.

### Step 5 — Feature Integration
To‑Do now:
- Uses system DnD helpers
- Defines feature‑local payload helper
- Applies state changes only after payload decode
- Accepts drops only on specific‑date targets

---

## Architectural Outcomes

| Area | Before | After |
|------|-------|------|
| DB Ownership | Feature‑owned | Bootstrap‑owned |
| Drag Systems | None / ad hoc | Central system module |
| Payload Parsing | Widget‑level | Single system decode |
| Cancellation | Undefined | Safe‑release compliant |
| Hierarchy | None | Definition‑only |

---

## Compliance
✔ No feature → feature coupling  
✔ No new global state systems  
✔ UI layout unchanged  
✔ Interaction framework system‑owned  
✔ Repositories remain bounded and query‑based

---

## Next Phase Candidates (Not Implemented)
- Definition hierarchy UI
- Drag visual affordances (system layer)
- Occurrence reorder within a day

### Step 6 — System DnD Compliance
- Removed feature-specific payload constructors from system module
- Introduced feature-local payload helpers
- Eliminated module-level cancellation state
- Added `DragResult` enum for deterministic outcomes

## 2026-02-08 — Documentation Consolidation (No Code Changes)
- Refactored AI_BRAIN documentation for redundancy removal and SSOT clarity.
- Moved contract details into LUX_SYSTEM_CONTRACTS; left PROJECT_RULES as operational index + role summary.
- Standardized Architecture Notes references to the master contracts for dump generation.
- Signed: Documentation Auditor (GPT-5.2)


## Patch — Archived Timestamp Schema Alignment

### Context
Archive flow in `TasksRepository` sets:
- `archived = 1`
- `archived_at = now_sqlite()`
- `updated_at = now_sqlite()`

Schema lacked `archived_at`, creating a contract violation between repo and DB.

### Action Taken
Created migration `0006_task_occurrence_archived_at.sql`:

```sql
ALTER TABLE task_occurrences
ADD COLUMN archived_at TEXT NULL;
```

### Result
- Repository code remains unchanged.
- Archive behavior now schema-safe.
- Timestamp Contract remains enforced (UTC via `now_sqlite()`).

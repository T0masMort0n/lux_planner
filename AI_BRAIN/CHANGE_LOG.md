
# UPDATED CHANGE LOG — To‑Do Phase 1 Stabilization

## Summary
This update completes the Systems Designer’s Phase‑1 stabilization requirements for the To‑Do feature. Work focused on enforcing system contracts, removing architectural violations, and introducing a system‑owned Drag & Drop framework.

---

## 1. Database & Data Model

### Added
- **Migration `0005_task_hierarchy.sql`**
  - Adds `parent_task_id` (nullable) to `task_definitions`
  - Establishes definition‑only hierarchy (no occurrence hierarchy)

### Updated
- `TaskDefinitionRow`
  - Now includes: `parent_task_id: Optional[int]`
  - Repo read paths default to `None` if column absent (migration safety)

---

## 2. Repository Layer

### Fixed
- Repaired truncated `tasks_repo.py` implementation.
- Added:
  - `update_occurrence_due_date()` → rescheduling logic
  - Proper JOIN‑based occurrence queries (prevents N+1 reads)

### Contract Alignment
- Panels are now strictly query‑based over occurrences.
- No parallel “Today/Upcoming” collections introduced.

---

## 3. To‑Do Service Lifecycle (Critical Fix)

### Removed (Violation)
- Feature‑owned DB initialization (`ensure_db_ready()` inside To‑Do service)

### Implemented
- DB connection created **only in bootstrap**
- Dependency flow:
  `bootstrap → TasksRepository → TodoRepo → TodoService → SystemServices → UI`

This resolves lifecycle ownership and matches system DI rules.

---

## 4. System‑Owned Drag & Drop Framework

### New Module
`src/lux/ui/qt/dragdrop.py`

### Provides
- Canonical typed payload format (`LuxDragPayload`)
- Feature‑agnostic constructor: `make_payload(kind, data)`
- Single decode path: `decode_mime()`
- Safe‑release handling:
  - ESC cancel
  - Resize during drag cancel
  - Invalid drop ignored
- Session‑local cancellation (no global shared state)
- `DragResult` enum for deterministic testing

### Removed from System Layer
- To‑Do specific helpers (moved into feature layer)

---

## 5. To‑Do UI DnD Integration

### Behavior
| Payload Kind        | Drop Effect |
|---------------------|-------------|
| `task_occurrence`   | Reschedules occurrence (`due_date = target_date`) |
| `task_definition`   | Creates new occurrence on target date |

### Guardrails
- Only specific‑date targets accept state‑changing drops
- Drop targets implemented via system decode path
- No feature‑level drag systems introduced

---

## 6. Risk Mitigation Coverage

Known interruption risks addressed:
- ESC mid‑drag → no stuck state
- Window resize during drag → canceled safely
- Invalid drop → no mutation

---


## 7. Timestamp Contract (Docs)
- Added a "Timestamp Contract" rule to AI_BRAIN (`PROJECT_RULES.md`): all persisted timestamps are UTC; repositories must use `now_sqlite()`; SQLite `datetime('now')` is forbidden in domain writes.
## Status
✔ System contract compliant  
✔ Lifecycle ownership corrected  
✔ Interaction framework centralized  
✔ No cross‑feature coupling introduced

## AI Workflow Update
- Established split workflow:
  - GPT-5.2 for design & decision-making
  - GPT-5.1 for repo-level code verification

## 2026-02-08 — Documentation Consolidation (AI_BRAIN)
- Compressed PROJECT_RULES to remove duplicated contract prose; PROJECT_RULES now indexes master contracts instead of redefining them.
- Updated AGENT_SCOPES to reflect the Documentation Auditor’s responsibilities and lane limits.
- Expanded LUX_SYSTEM_CONTRACTS into a single master reference for interaction, dump, and theme SSOT contracts (capturing already-accepted decisions only).
- Normalized PROJECT_ROADMAP phase status wording (Phase 1 marked complete; Phase 2 marked current) to remove internal contradictions.
- Signed: Documentation Auditor (GPT-5.2)

---

## 2026-02-09 — Tasks naming cleanup + timestamp contract enforcement (Coder)

### Changed
- Renamed feature identifiers and wiring from **todo → tasks** to eliminate ambiguity (UI wording unaffected).
  - `lux.features.todo` → `lux.features.tasks`
  - `Todo*` identifiers → `Tasks*` equivalents
  - `SystemServices.todo_service` → `SystemServices.tasks_service`
  - Navigation module key updated to `"tasks"`.

### Fixed
- Standardized persisted timestamp writes to use `now_sqlite()` (UTC) via bound parameters (no SQLite `datetime('now')` in domain writes).
- Added migration **0006_task_occurrence_archived_at.sql** to add `archived_at` to `task_occurrences`, aligning schema with repository archive behavior.

### Docs
- Added a single-source **Timestamp Contract** section to AI_BRAIN (UTC-only timestamps; repositories must use `now_sqlite()`; forbid `datetime('now')` in domain writes).

**Sign-off:** Coder

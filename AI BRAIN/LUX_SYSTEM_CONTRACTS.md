# LUX PLANNER — SYSTEM INTERACTION & SHARING CONTRACTS (MASTER)

**Status:** System-owned contracts (binding)  
**Last Updated:** 2026-02-08  
**Owner:** Systems Designer Agent (system)  
**Maintainer:** Documentation Auditor (clarity + compression)

---

## 0) Core Interaction Philosophy
"If it exists, you can yeet it somewhere else."

Direct manipulation is a **system-level** principle. Features provide content; the system provides interaction frameworks.

---

## 1) Governance & Change Rules
- These contracts override feature decisions.
- Systems Designer approval is required for **structural** changes (layout, interaction frameworks, data ownership).
- Visual Designer approval is required for **aesthetic** contract changes (theme tokens, typography content rules).
- A change is not “done” until CHANGE_LOG + IMPLEMENTATION_LOG are updated.

---

## 2) Drag & Drop Contract (System-Owned)

### 2.1 Scope
- **System DnD is the only drag/drop mechanism.**
- No feature-level drag systems, global state managers, or bespoke payload formats.

### 2.2 Payload Contract
- All drags must use a typed payload discriminator (e.g., `kind`) and a single decode path.
- Payload encoding/decoding is system-owned; features may provide **feature-local helpers** that produce/consume system payloads.

### 2.3 Safe Release (Interruption Safety)
All drags must be interruption-safe:
- ESC cancels safely (no mutation, no stuck UI).
- Invalid drops are ignored safely.
- Resize/interruptions cancel safely.
- Cancellation state must be **session-local** (no global shared cancellation state).

### 2.4 Deterministic Outcomes
DnD operations must produce deterministic results suitable for testing (e.g., a result enum such as `DragResult`).

---

## 3) State-Changing Drop Contract (Tasks / Scheduler-aligned)

### 3.1 Canonical mutations
Drops onto date buckets mutate **exactly one canonical field**:

- **Occurrence drop** → update `due_date`
- **Definition drop** → create new occurrence for target date

### 3.2 Target requirements
- Drop targets must resolve to a **specific date** (no fuzzy buckets / “sometime soon”).
- Only specific-date targets may accept state-changing drops.

---

## 4) Task Hierarchy Contract (Definition-only)

- Hierarchy lives on `task_definitions.parent_task_id` (nullable).
- Task occurrences do **not** own hierarchy.
- Parent completion is derived from descendant occurrences **within the current panel query scope**.
  - This means parent completion may legitimately differ across panels.

---

## 5) Secondary Source Panel Contract (System-Owned)

Cross-feature workflows require simultaneous access to a primary workspace and secondary item sources.

### 5.1 Regions
| Region | Role |
|-------|------|
| Left Panel | Feature-local navigation |
| Right Main Panel | Primary feature workspace |
| Secondary Source Panel (collapsible) | System-owned source surface for cross-feature item access |

### 5.2 Behavioral model
- Primary feature = workspace/canvas
- Secondary panel = item source library
- Secondary panel is opened intentionally and dismissible
- Secondary panel is **not** a second “full feature” surface

### 5.3 Content rules
Secondary panel may include:
- Item lists
- Search/filter
- Drag-enabled item surfaces

Secondary panel must NOT include:
- Deep feature navigation
- Settings
- Multi-step flows
- Full feature UI replicas

### 5.4 Governance
- Implemented at AppShell/system layer.
- Features may register item sources; features may not introduce new layout behaviors.

---

## 6) Explore Mode (System-Owned) — Minimum Contract
**Status:** Framework exists; content specifics are feature-registered.

Binding constraints:
- Explore Mode is a system-owned inspection layer (e.g., bottom panel).
- Features may register metadata; features must not create their own explore frameworks.
- This contract does not yet define UI affordances beyond “system-owned surface + feature metadata registration”.

(Details intentionally omitted until accepted by Systems Designer.)

---

## 7) Sharing (System-Owned) — Minimum Contract
Binding constraints:
- **Copy-first model** (no auto-overwrite).
- “Update sharing” is intentional/explicit.

(Details intentionally omitted until accepted by Systems Designer.)

---

## 8) Template Packs (System-Owned) — Minimum Contract
Binding constraints:
- Packs behave like playlists.
- Items can belong to multiple packs.
- Import uses deduplication rules.
- Imported data is treated as “proposals,” not canonical truth.

(Details intentionally omitted until accepted by Systems Designer.)

---

## 9) Project Dump Generation Contract (System-Owned)

Dump generation is **system infrastructure**. Purpose: prevent stale artifacts and phantom duplicates from contaminating agent work.

### 9.1 Canonical generator
- There is exactly one canonical dump generator script (path+name) defined by the project (see tooling docs).
- No alternative dump tools are allowed.

### 9.2 Scope allowlist
- Allowlist-only dump contents: `src/**`, `assets/**`, minimal tooling + root build metadata.
- `/AI_BRAIN/**` (including archives) must be excluded entirely.

### 9.3 Output location
- Dump outputs are written **outside repo root** (sibling directory) to prevent self-ingestion.

### 9.4 Determinism & verification
- Each run overwrites outputs deterministically; stable ordering.
- Verification checks:
  - No `==== FILE: AI BRAIN\...` entries in the dump.
  - No `AI BRAIN` substring present in the dump output.

---

## 10) Theme Pipeline SSOT (System-Owned)

### 10.1 Single authoritative module
- One canonical theme module (e.g., `src/lux/ui/qt/theme.py`) is the **only** module allowed to apply QSS / call `app.setStyleSheet(...)`.

### 10.2 Single authoritative API
- One canonical API signature for theme application is allowed.
- Duplicate definitions (even if compatible) are prohibited (Python will silently override earlier defs).

### 10.3 Typography tokens + substitution
- Themes must reference system typography tokens (e.g., `font-family: var(--font-body);`).
- The system applies schemes via **bounded substitution** limited to `font-family:` declarations and must fail-soft.
- Bundled fonts must be registered once per app lifecycle before applying QSS.

---

## 11) Appendix — Task System DnD Integration (To‑Do Phase 1)
Accepted behavior mapping:

| Payload Kind | Drop Effect |
|---|---|
| `task_occurrence` | Reschedules occurrence (`due_date = target_date`) |
| `task_definition` | Creates new occurrence on target date |

Guardrails:
- Only specific-date targets accept state-changing drops.
- Drop targets use the system decode path.
- No feature-level drag systems.

---

Signed: Documentation Auditor (GPT-5.2)

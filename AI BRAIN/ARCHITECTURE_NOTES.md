# LUX PLANNER — ARCHITECTURE NOTES

### Decision: Establish System Interaction Contracts + Admin Governance
**Date:** 2026-02-06  
**Owner:** Systems Designer Agent (Admin Decision — Product Driver + AI Admin)  
**Context:** The project matured from feature scaffolding to a system-level life platform. Multiple cross-feature interaction models (drag/drop, sharing, packs, explore mode) were being defined without a single architectural consolidation point.  
**Decision:** Adopt **LUX_SYSTEM_CONTRACTS** as system law. Formalize Drag/Drop, Explore Mode, Sharing, Template Packs, and System Area Taxonomy as system-layer frameworks. Introduce Visual Designer Agent as separate aesthetic authority. Establish Product Driver + AI as admin governance layer.  
**Why:** Prevent architectural drift, feature silos, and visual inconsistency. Enable scalable system evolution while preserving simplicity and trust-first UX.  
**Rules Introduced / Updated:**
- System owns interaction frameworks
- Features provide content only
- Copy-first sharing model
- Packs behave like playlists
- Visual Designer owns cosmetics only
- Admin decisions must be signed
**System Implications:**
- New system directories/services expected
- Future features must integrate via system contracts
- Visual work separated from structural work
**Files / Areas Affected (high level):**
- LUX_SYSTEM_CONTRACTS
- PROJECT_RULES
- PROJECT_ARCHITECTURE
- AGENT_SCOPES

**Signed:** Product Driver & AI Admin

---

### Decision: Typography as a System-Owned Surface (Tokens + Font Schemes)
**Date:** 2026-02-06  
**Owner:** Systems Designer Agent (Reviewed implementation by Coder Agent)  
**Context:** Visual themes need to support multiple typography “schemes” (like Obsidian) without duplicating font-family stacks across every theme QSS. Qt/QSS also does not reliably support CSS custom properties at runtime, and bundled fonts are not automatically registered.  
**Decision:**  
- Typography is treated as a **system surface** (mechanism + storage + settings), not a theme-by-theme one-off.  
- The System defines a **Typography Token Contract** (system-owned names): `--font-ui`, `--font-body`, `--font-heading`, `--font-mono`, `--font-micro`.  
- The Visual Designer provides **Font Scheme content** as reusable mappings (token → `font-family` stack) in `assets/font_schemes/<id>.json`.  
- Theme QSS must reference tokens (e.g., `font-family: var(--font-body);`) and must not hardcode scheme-specific font stacks.  
- Because Qt/QSS support for `var(...)` is unreliable, the System applies schemes via **safe, bounded substitution** (only inside `font-family:` declarations).  
- The System performs **bundled font registration once per app lifecycle** (bounded to `assets/fonts/**`) before any QSS is applied.

**Why:**  
- Prevents theme coupling and reduces duplication/drift (any theme can pair with any scheme).  
- Keeps typography scalable and theme-agnostic while preserving clear ownership boundaries: mechanism/system vs content/visual.  
- Maintains fail-soft startup: invalid or missing scheme files never block app launch.

**Rules Introduced / Updated:**  
- Themes must use typography tokens; schemes define font stacks.  
- New typography tokens require Systems Designer approval (system contract change).  
- Font scheme IDs must be sanitized to prevent path traversal; scheme loading must fail-soft.

**Files / Areas Affected (high level):**  
- System UI bootstrap (`src/lux/ui/qt/theme.py`)  
- Assets (`assets/fonts/**`, `assets/font_schemes/**`)  
- System settings + Settings UI (font scheme selection)

**Signed:** Systems Designer Agent

---

### Decision: Theme Pipeline SSOT Enforcement (Single Source of Truth)
**Date:** 2026-02-07  
**Owner:** Systems Designer Agent  
**Context:** Theme/typography pipeline drift risk: conflicting `apply_theme_by_name` signatures and duplicate theme modules can cause runtime import ambiguity and silent loss of typography token substitution (Qt/QSS `var(...)` support is unreliable).  
**Decision:** Establish a single authoritative theme pipeline (SSOT) with one canonical module (`src/lux/ui/qt/theme.py`) and one canonical API (`apply_theme_by_name(app, theme_name, font_scale, font_scheme_id)`). All theme application and typography substitution must route through this function.  
**Why:** Prevents branch drift, feature-level workarounds, and silent typography regressions; preserves system ownership of visual mechanisms while allowing Visual Designer ownership of scheme content.  
**Rules Introduced / Updated:**  
- Only canonical theme module may call `app.setStyleSheet(...)`.  
- No duplicate `apply_theme_by_name` definitions permitted.  
- Typography token substitution must be bounded to `font-family:` declarations and fail-soft.  
**Signed:** Systems Designer Agent

---

### Decision: Dump Generation Contract (Allowlist + Output Outside Repo)
**Date:** 2026-02-07  
**Owner:** Systems Designer Agent (Admin Decision)  
**Decision:** Dump generation is system infrastructure and must be SSOT-friendly:
- Allowlist-only dump contents: `src/**`, `assets/**`, minimal tooling + root build metadata.
- `/AI_BRAIN/**` is excluded entirely (including Archive/**).
- Dump outputs are written outside repo root to a sibling directory to prevent self-ingestion.
- Each run overwrites outputs deterministically; stable ordering.

**Verification:**
- No `==== FILE: AI BRAIN\...` entries in PROJECT_DUMP.txt.
- No `AI BRAIN` substring present in the dump output.

**Canonical contract location:** LUX_SYSTEM_CONTRACTS.md → “Project Dump Generation Contract”.

**Signed:** Product Driver & AI Admin


## 2026-02-08 — To-Do Phase-1 System Stabilization

**Owner:** Systems Designer Agent  
**Signed By:** Systems Designer Agent + Product Driver  

### Context
To-Do feature required stabilization to meet System Interaction Contracts and lifecycle ownership rules. Prior implementation violated system DI patterns and lacked system-owned interaction plumbing.

### Decisions

#### 1. Definition-Only Hierarchy (System Contract Extension)
- Task hierarchy lives exclusively on `task_definitions.parent_task_id`.
- Occurrences do NOT own hierarchy.
- Parent completion is derived from descendant occurrences **within the current panel query scope**.
- Parent completion may legitimately differ across panels.

#### 2. State-Changing Drop Contract
- System Drag & Drop is the only DnD mechanism.
- Drops onto date buckets mutate a **single canonical field**:
  - Occurrence → update `due_date`
  - Definition → create occurrence
- Drop targets must resolve to a specific date (no fuzzy buckets).

#### 3. Lifecycle Ownership Enforcement
- Feature-owned DB initialization removed from To-Do.
- Bootstrap is sole DB lifecycle owner.
- Dependency chain: bootstrap → repositories → service → SystemServices → UI.

#### 4. System Drag & Drop Framework Introduced
Module: `src/lux/ui/qt/dragdrop.py`

Provides:
- Typed payload contract
- Single decode path
- Session-local cancellation
- Deterministic `DragResult`

No feature logic inside.

---

## 2026-02-08 — AI Workflow Architecture Decision

**Owner:** Systems Designer Agent + Product Driver  

### Decision
AI roles now split by capability:

| AI Mode | Purpose |
|--------|---------|
| **GPT-5.2** | Systems design, architecture decisions, UX logic |
| **GPT-5.1 (repo access)** | Code review, integration verification, wiring validation |

### Why
Repo visibility improves system integrity enforcement, but strategic reasoning remains better handled by 5.2.

---

**Status:** System stabilized for Phase-1 To-Do acceptance.

Signed: Documentation Auditor (GPT-5.2)

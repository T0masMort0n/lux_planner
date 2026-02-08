
# LUX PLANNER — SYSTEM INTERACTION & SHARING CONTRACTS

## CORE INTERACTION PHILOSOPHY
"If it exists, you can yeet it somewhere else."
Direct manipulation is a system-level principle. Items should be draggable and composable with minimal exceptions.

---

## UNIVERSAL DRAG & DROP CONTRACT
**Ownership:** System-owned interaction model. Features provide items and zones but do not implement drag logic.

### Allowed Operations
- Schedule
- Reschedule
- Add to Collection
- Compose / Add to Plan
- Assign
- Reorder
- Move
- Copy

### Anchor Interactions
- Task → Scheduler = Schedule
- Event → Different time = Reschedule
- Ingredient/Recipe → Grocery list = Add
- Exercise → Workout plan = Compose
- Workout plan → Scheduler = Schedule

### Safe Release
Cancel Drop Zone, invalid drop areas, and ESC must always cancel without side effects.

### Privacy
Drag/drop never implies sharing; sharing requires explicit flow.

---

## EXPLORE MODE CONTRACT
Purpose: "What is this and what can I do with it?"

- Activated via Help button
- Highlights interactive elements only
- Uses calm visual tone
- Bottom info panel displays element info

### Element Info Structure
- Identity
- System Connections
- Example Use

### Metadata Model Fields
id, label, description, use_context, connections, example_action, element_type, locations

---

## SHARING & CONTACT RELATIONSHIP CONTRACT
- Nothing shared by default
- Sharing creates copies
- Updates handled as proposed updates
- Contacts have relationship tiers: External, Trusted, Household
- Journal never auto-accepted

---

## TEMPLATE PACKS (PLAYLIST MODEL)
- Packs are user-owned collections of items
- Items can belong to multiple packs
- Packs used for export/share/import
- Import creates copies
- Dependencies included in pack

---

## PACK IMPORT & DEDUP CONTRACT

### Canonical Identity
Items use canonical keys (normalized label + qualifiers). Display names are not identity keys.

### Two-Layer Metadata
Layer A: Canonical Item (user truth)
Layer B: Provenance Records (import sources)

### Import Modes
1. Safe (default)
2. Smart Merge
3. Always Separate

### Conflict Rules
User-entered data always wins. Imported values stored as sources.

### Variant Handling
Different states/forms create variants, not merges.

### Review Workspace
After import, users may merge or keep variants. Import never blocks workflow.

### Confidence Scoring
High confidence → merge
Low confidence → variant + review queue

---


---

## TYPOGRAPHY SCHEMES CONTRACT (SYSTEM-OWNED)

Typography schemes are a **shared system resource**. The system owns the mechanism; the Visual Designer owns the scheme content.

### Token Contract (System-Owned Names)
Themes must reference **only** these typography tokens (no per-theme font-family stacks):
- `--font-ui`
- `--font-body`
- `--font-heading`
- `--font-mono`
- `--font-micro`

### Theme Rule (No Hardcoded Families)
Theme QSS must use token references in `font-family` declarations (example):
- `font-family: var(--font-body);`

Themes must **not** embed concrete font-family stacks intended to vary by scheme.

### Scheme Content (Visual Designer-Owned)
Font schemes are provided as JSON files:
- `assets/font_schemes/<scheme-id>.json`

Each scheme maps approved tokens → a `font-family` stack (with fallbacks).
Scheme IDs must be sanitized and stable (lowercase, digits, `_` and `-`).

### Application Mechanism (System-Owned)
Qt stylesheets do not reliably support CSS custom properties at runtime. Therefore:
- The system applies schemes via **safe, bounded substitution** limited to `font-family: var(--font-*)` usage.
- No global string replacement is permitted.
- Missing/invalid scheme files must **fail soft** (never block startup).

### Bundled Font Registration (System-Owned)
Bundled fonts under `assets/fonts/**` (`.ttf` / `.otf`) must be registered:
- once per app lifecycle
- before any QSS is applied
- bounded to the fonts directory
- deterministic ordering
- fail-soft (no startup blocking)

### Governance
Changes to:
- the token set / token names,
- scheme resolution mechanism,
- theme application pipeline,
require Systems Designer approval.


## SYSTEM UI LAYERS
Left: Navigation
Right: Feature Content
Bottom: Explore Info Surface

---

## GOVERNANCE
These contracts override feature decisions. Systems Designer approval required for changes.

## SCHEDULER INTERACTION SURFACE (SYSTEM-OWNED)

Scheduling is a **system interaction framework**, not a feature mechanic.

### Ownership
- System layer owns scheduling orchestration.
- Features may request scheduling through system services.
- Features must not implement their own scheduling write paths.

### Integration Pattern
- Access via: `services.scheduler_service`
- Registry accessed via: `scheduler_service.registry`
- No feature-to-feature imports allowed for scheduling.

### Architectural Role
Scheduler acts as a cross-feature coordination surface enabling:
- Task scheduling
- Plan scheduling
- Future domain integrations

This surface must remain:
- Feature-agnostic
- DB-lifecycle neutral (bootstrap-owned)
- Single-registry consistent

## THEME PIPELINE SSOT (SYSTEM-OWNED)

Theme + typography application is a **single-source-of-truth (SSOT)** system pipeline. No other module may apply QSS, resolve typography tokens, or call `app.setStyleSheet(...)`.

### Canonical Module Path (One True Theme Module)
- `src/lux/ui/qt/theme.py` (import path: `lux.ui.qt.theme`)

Any duplicate `theme.py` or alternate `apply_theme_*` helpers are prohibited and must be removed to avoid import ambiguity.

### Canonical API (Authoritative Signature)
`apply_theme_by_name(app, theme_name, font_scale=1.0, font_scheme_id=None)`

### Canonical Call Sites (Who May Call It)
Allowed callers:
- **System bootstrap / composition root** (initial theme application)
- **System settings change handler** (re-apply theme on theme/scheme/scale changes)

Disallowed callers:
- Feature modules
- Feature UI widgets
- Any non-system layer code

### Pipeline Order (Binding)
1) Register bundled fonts (idempotent; once per app lifecycle)
2) Resolve theme name (fallback to default)
3) Load theme QSS
4) Apply font scale transform (bounded; fail-soft)
5) Load font scheme mapping (sanitized scheme id; fail-soft)
6) Substitute typography tokens **only inside** `font-family: var(--font-*)` declarations (bounded substitution)
7) Apply stylesheet: `app.setStyleSheet(qss)`

### Ban List (Hard Prohibitions)
- No other `apply_theme_by_name` definitions anywhere else
- No other module calling `QApplication.setStyleSheet(...)` besides the canonical theme module
- No feature-layer font stack hardcoding intended to vary by scheme
- No reliance on Qt runtime support for CSS custom properties (`var(...)`) without substitution

### Fail-Soft Requirements
- Missing theme file → apply fallback theme (or empty QSS) and continue startup
- Missing/invalid scheme JSON → continue with default mapping (or leave tokens unresolved) and continue startup
- Bundled font registration failures → log and continue (no startup block)

### Governance
Any change to:
- canonical module path,
- canonical API signature,
- substitution boundaries,
- theme application ordering,
requires Systems Designer approval.


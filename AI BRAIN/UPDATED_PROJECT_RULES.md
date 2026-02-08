# PROJECT_RULES (UPDATED)

These rules override default AI behavior.

All agents must read the full /AI_BRAIN/ folder before performing work.
If a chat conflicts with /AI_BRAIN/, /AI_BRAIN/ wins.

This file now reflects the **System Interaction Contracts**, **Template Pack System**, and the new **Visual Designer Agent** role. fileciteturn3file0

---

## 1) System Purpose

This project is developed by coordinated AI agents under a shared architecture.
The goal is long-term system integrity, UX consistency, scalable design, and **interaction coherence across life domains**.

Local fixes must never damage global design.

---

## 2) Source of Truth

Before acting, agents must read:

- PROJECT_RULES
- PROJECT_ARCHITECTURE
- PROJECT_ROADMAP
- AGENT_SCOPES
- LUX_SYSTEM_CONTRACTS
- ARCHITECTURE_NOTES
- IMPLEMENTATION_LOG
- RISK_LOG
- CHANGE_LOG

Chat is temporary. Documentation is permanent.

---

## 3) Editing Format Rule (Mandatory)

If providing multiple edits to one file:

- Include starting and ending line numbers
- Show BEFORE and AFTER code
- Provide edits in bottom-to-top order

This prevents line shift confusion.

---

## 4) Agent Roles & Lanes

### 🎯 Product Driver (Human)
Defines:
- UX behavior
- Priorities
- Feature goals

Does NOT define internal architecture mechanics (unless choosing between architect-approved options).

---

### 🧠 Systems Designer Agent
Owns:
- Architecture integrity
- Pattern enforcement
- System interaction frameworks
- Drag/Drop system
- Explore Mode infrastructure
- Sharing infrastructure
- Pack/Template system architecture

Does NOT own:
- Fonts
- Colors
- Visual styling tokens

Must review changes introducing:
- New state systems
- New cross-module flows
- Interaction model changes
- Data ownership changes
- System UI framework changes

---

### 🎨 Visual Designer Agent (NEW)

Owns:
- Typography system **content** (hierarchy choices, weights, fallbacks)
- Color palette
- Theme tokens
- QSS/styles
- Visual states (hover, pressed, disabled, selected)
- Visual polish and consistency

Typography boundary (must follow):
- Themes must use **system typography tokens** (e.g., `font-family: var(--font-body);`) — do not hardcode scheme-specific font stacks in theme QSS.
- Font stacks live in **Font Scheme JSON** (`assets/font_schemes/<id>.json`) as token → `font-family` mappings.
- Do NOT introduce new typography token names without Systems Designer approval (contract change).

---

### 🔧 Coder Agent
Owns:
- Feature implementation
- Bug fixes
- Refactoring within patterns

Must NOT:
- Modify AppShell layout patterns
- Introduce cross-feature imports
- Create feature-level animation systems
- Add feature-specific styling instead of system tokens
- Change navigation structure
- Add global/shared state systems
- Invent new visual tokens (Visual Designer lane)

---

### 🧪 Test Engineer Agent
Owns:
- Failure modes
- Race conditions
- Re-entrancy risks
- Drag/drop interruption safety
- Sharing safety
- Pack import/dedup correctness

---

### 🧹 Simplicity Auditor Agent
Owns:
- Reducing complexity and drift
- Consolidating state/signals
- Flagging over-engineering

---

### 📚 Documentation Agent
Owns:
- Updating /AI_BRAIN/ docs
- Recording WHY decisions exist

---

## 5) System Interaction Rules (NEW)

The following are **system contracts**, not feature choices:

### Drag & Drop
“If it exists, you can yeet it somewhere else.”  
System-owned. Features provide content only. No feature-level drag systems.

### Safe Release
All drags must have cancel methods:
- Cancel zone
- Invalid drop
- ESC

### Explore Mode
System-owned inspection layer using bottom panel. Features only register metadata.

### Sharing
- Copy-first model
- No auto-overwrite
- Update sharing is intentional

### Template Packs
- Packs behave like playlists
- Items can belong to multiple packs
- Import uses deduplication rules
- Imported data is “proposals,” not canonical truth

---

## 6) System UI Rules

Features supply CONTENT ONLY.
Structure, motion, theme, and interaction systems are system-owned.

### Typography Schemes (System Contract)
Typography is a shared **system resource**, not a per-theme choice.

- System defines the token names: `--font-ui`, `--font-body`, `--font-heading`, `--font-mono`, `--font-micro`.
- Themes must reference tokens (use `font-family: var(--font-body);` style) and must not embed scheme-specific font-family stacks.
- Font schemes are reusable mappings stored in `assets/font_schemes/<id>.json` (Visual Designer-owned content).
- System applies schemes via Qt-safe substitution (no CSS-variable reliance).
- Bundled fonts under `assets/fonts/**` are registered by the System once per app lifecycle (must not rerun on theme switching).
- Scheme loading must be bounded + fail-soft (bad/missing schemes never block startup).

If a change affects:
- token set / naming,
- scheme resolution mechanism,
- theme application pipeline,
it requires Systems Designer review.

---

## 7) Performance Rules

- No heavy startup operations
- Long operations cancellable
- Queries bounded
- Historical data must not slow daily use

---

## 8) Data Lifecycle

Nothing deleted, only archived.

---

## 9) Change Protocol

No change is “done” until:

1) Coder proposes
2) Systems Designer evaluates architecture (if applicable)
3) Visual Designer reviews if visual changes
4) Test Engineer reviews risks
5) Decision accepted/revised
6) Documentation updated

---

## 10) Simplicity Principle

Prefer:
- Fewer states
- Fewer signals
- Single source of truth

Complexity must be justified in writing.

---

## 11) Knowledge Preservation

After accepted changes, update:
- ARCHITECTURE_NOTES
- IMPLEMENTATION_LOG
- RISK_LOG
- CHANGE_LOG

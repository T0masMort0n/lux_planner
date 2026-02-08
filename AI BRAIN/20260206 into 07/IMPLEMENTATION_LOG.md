
### Change: Documentation & Governance Alignment
**Date:** 2026-02-06  
**Owner:** Coder Agent (Docs Update under Admin Direction)  
**Problem:** Core governance documents did not reflect system contracts and admin authority.  
**Solution:** Updated rules, roadmap, architecture, and agent scopes.  
**Files Changed:**
- PROJECT_RULES
- PROJECT_ROADMAP
- PROJECT_ARCHITECTURE
- AGENT_SCOPES
**Notes (mechanics only):**
- Text updates only
- No runtime code changes
**New mechanisms introduced (if any):**
- None

**Signed:** Product Driver & AI Admin

### Change: System Typography Schemes (Fonts + Tokens + Settings)
**Date:** 2026-02-06  
**Owner:** Coder Agent (System implementation)  
**Problem:**  
- Bundled fonts under `assets/fonts/**` were not registered, causing QSS `font-family` to fall back to OS fonts.  
- Font “schemes” needed to be switchable across themes without duplicating font-family stacks inside each QSS file.  
**Solution (mechanics only):**  
- Register all `.ttf`/`.otf` under `assets/fonts/**` once per app lifecycle before applying QSS.  
- Introduce system typography tokens (`--font-ui`, `--font-body`, `--font-heading`, `--font-mono`, `--font-micro`).  
- Add a system font scheme loader (`assets/font_schemes/<id>.json`) that maps tokens → font-family stacks.  
- Apply scheme via bounded substitution inside `font-family:` declarations for Qt compatibility (no global replacements).  
- Add persistent setting `font_scheme_id` + Settings UI control to select schemes.  
- Harden scheme loading (sanitized scheme IDs; fail-soft on missing/invalid JSON).

**Files Changed (high level):**
- System UI theme application (`src/lux/ui/qt/theme.py`)
- System settings (schema/store) + Settings UI (font scheme selector)
- Assets directory contract (`assets/fonts/**`, `assets/font_schemes/**`)

**New mechanisms introduced (if any):**
- Font registration bootstrap (idempotent)
- Font scheme mapping loader + token substitution pipeline
- Persistent font scheme selection

**Signed:** Systems Designer Agent (review) + Coder Agent (implementation)

Change: Cross-Theme Typography Tokenization & Visual Font Schemes

Date: 2026-02-06
Owner: Visual Designer Agent

Problem:
Themes used hardcoded font-family stacks, preventing system typography schemes from controlling visual identity across themes. Hierarchy (UI vs headings vs micro text) was not explicitly defined at the theme level.

Solution (visual layer only):

Replaced all concrete font-family stacks in theme QSS with system typography tokens:
--font-ui, --font-heading, --font-micro (no new tokens introduced).

Established consistent hierarchy usage:

App/UI surfaces → --font-ui

Titles & section headers → --font-heading

Metadata / captions → --font-micro

Ensured changes were typography-only (no layout, spacing, color, or interaction edits).

Added a bundled-safe visual scheme definition to support cohesive typography personality without system-mechanism changes.

Files Changed (visual only):

assets/themes/cloudy.qss

assets/themes/graphite.qss

assets/themes/obsidian.qss

assets/themes/sunkissed.qss

assets/font_schemes/bundled_core.json

Notes (scope compliance):

No settings logic modified

No token system changes

No theme structure or component styling altered

Fully compliant with Typography Token Contract and Agent Scope boundaries

Result:
Typography is now system-driven, scheme-switchable, and visually hierarchical across all themes with no regressions.

Signed: Visual Designer Agent 🎨

## 2026-02-07 — Scheduler DI Consistency & System Spine Hardening

**User Problem / Goal:**  
Resolve repeated system review rejections related to inconsistent Scheduler dependency injection and DB lifecycle ownership.

**What Changed (high level):**
- Removed `scheduler_registry` from `SystemServices` so only `scheduler_service` is exported to UI/module layers.
- Consolidated registry access through `services.scheduler_service.registry`.
- Eliminated all internal DB initialization logic from `SchedulerService`:
  - No `ensure_db_ready()` calls.
  - No repository construction inside service.
  - Repo and registry are required constructor dependencies.
- Reconfirmed bootstrap as the sole composition root for DB and system service construction.

**System Architectural Significance:**
This change establishes the **Scheduler System Spine**:
- Scheduler is now a **System Interaction Surface**, not a feature-owned mechanic.
- All future cross-feature scheduling will route through this system surface.
- DB lifecycle is fully centralized and predictable.
- A single registry instance exists by construction.

**Rules / Constraints Observed:**
- UI layer continues to avoid `lux.data.*` imports.
- No feature-to-feature imports introduced.
- No singletons or service locators added.
- No AppShell/layout/navigation changes made.

**Follow-ups / TODOs:**
- Systems Designer acceptance review of DI consistency. ✔
- Next phase: higher-level scheduling capabilities built on this system spine.

**Signed:**  
Coder Agent (Implementation)  
Systems Designer Agent (Architecture Acceptance)


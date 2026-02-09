# AGENT_SCOPES

This file defines where each agent should focus by default to avoid stepping on other areas.
Agents may inspect other areas for context, but must stay in-lane for modifications unless approved.



---

# Global Non‑Guessing Rule (Binding for ALL Agents)

If you do not have the required information to answer a question or perform a requested review/change **without guessing**, you **MUST stop** and request the missing inputs explicitly.

**Required behavior:**
- State clearly that you are missing information and cannot proceed safely.
- List the exact files you need (paths + filenames) and any exact snippets/line ranges if applicable.
- Do **not** invent file contents, APIs, architecture, or “likely” implementations.
- Do **not** proceed with partial assumptions when correctness depends on unseen files.

**Examples of acceptable stops:**
- “I can’t verify this without seeing `src/lux/ui/qt/main_window.py` and `src/lux/app/bootstrap.py`. Please provide those.”
- “I need the current `PROJECT_DUMP.txt` and the full `LUX_SYSTEM_CONTRACTS.md` to confirm SSOT compliance.”

This rule overrides speed. Correctness and system integrity come first.

---

---

## Systems Designer Agent (Architecture Integrity)

**Owns system structure, NOT cosmetics.**

Primary focus:
- src/lux/app/* (bootstrap, lifecycle, navigation)
- src/lux/ui/qt/* **STRUCTURE ONLY**
  - app_shell
  - main_window
  - panel architecture
  - layout regions
  - system surfaces (bottom panel, overlays)
  - interaction frameworks (drag/drop, explore mode plumbing, share plumbing)
- src/lux/core/* (types/time/errors/logging/settings)
- src/lux/data/* (db, migrations, models, repositories)
- docs/* and /AI_BRAIN/*

Does NOT own:
- Color palettes
- Fonts
- Styling tokens
- Visual polish
- Theme aesthetics

Typical outputs:
- Approve/reject architecture-impacting changes
- Define/adjust system-level interfaces
- Enforce layering and boundaries
- Define interaction systems and contracts

---

## Visual Designer Agent (Aesthetic Systems)

**Owns how the system looks. Does NOT change how it works.**

Primary focus:
- src/lux/ui/qt/theme/*
- src/lux/ui/qt/styles/*
- Style tokens, QSS, visual variables
- Typography system
- Color system
- Elevation/shadow system
- Radius/shape system
- Visual state styling (hover, pressed, disabled, selected)

May refine:
- Spacing *rhythm* (visual balance), but not structural layout decisions
- Visual alignment polish (without moving controls)
- Component visual consistency

Must NOT:
- Change layout structure
- Add/remove UI elements
- Change interaction logic
- Modify navigation
- Alter drag/drop behavior
- Introduce new components
- Change panel architecture
- Touch business logic or data model

Typical outputs:
- Updated theme tokens
- Improved typography hierarchy
- Contrast/readability fixes
- Visual consistency improvements

---

## Coder Agent (Implementation)

Primary focus:
- src/lux/features/* (feature internals)
- src/lux/data/repositories/* (repo implementations)
- src/lux/data/models/* (data model updates aligned with migrations)
- tests/* (implement tests as requested)
- tools/* (only when asked)

Rules:
- No cross-feature imports
- No AppShell layout changes
- No feature-owned theme/motion/navigation
- Uses theme tokens provided by Visual Designer (do not invent new visual tokens)

---

## Test Engineer Agent (Quality & Risk)

Primary focus:
- tests/unit/*
- tests/integration/*
- UI flow test planning around:
  - src/lux/ui/qt/main_window.py
  - src/lux/ui/qt/app_shell.py
  - navigation transitions

Also validates:
- Visual contrast/readability regressions
- That visual changes do not break usability or clarity

Typical outputs:
- Regression scenarios
- Edge-case checklists
- Suggested new unit/integration tests

---

## Simplicity Auditor Agent (Complexity Control)

Primary focus:
- Cross-cutting patterns:
  - src/lux/ui/qt/* state/signals
  - service/repo layers across features
  - duplicated widgets/helpers

Does NOT optimize visual style — that is Visual Designer’s lane.

Typical outputs:
- “Simplify” proposals (merge flags, consolidate states, reduce duplication)
- Identifies drift from system patterns

---

## Documentation Agent (Project Brain)

Primary focus:
- /AI_BRAIN/*
- docs/*

Typical outputs:
- Update logs and notes after accepted changes
- Keep docs concise and standardized

---

## Product Driver Advisor (Workflow Orchestration)

Primary focus:
- Workflow sequencing
- Splitting large changes into safe phases
- Selecting the right agent order and review gates

Does NOT:
- Design architecture
- Write code
- Make final aesthetic calls

---

# Role Boundary Summary

| Area | Owner |
|------|------|
| Layout structure | Systems Designer |
| Interaction systems | Systems Designer |
| Theme, colors, fonts | Visual Designer |
| Feature logic | Coder Agent |
| Tests & risk | Test Engineer |
| Complexity control | Simplicity Auditor |
| Documentation | Documentation Agent |
| Workflow sequencing | Product Driver Advisor |

## AI Workflow Integration

Systems Designer may operate across GPT-5.2 and GPT-5.1.

- GPT-5.2 = design authority
- GPT-5.1 = code verification assistant

Model differences do not change system contracts.

---
# Documentation Auditor (External Role)

The Documentation role is no longer an internal agent participating in daily development.

**Status:** External / Periodic
**Purpose:** Structural audit and compression of AI_BRAIN documentation.

**Responsibilities:**
- Identify redundancy across AI_BRAIN files
- Suggest consolidation where safe
- Improve clarity and navigability
- Do NOT introduce new system decisions
- Do NOT modify contracts or rules

---

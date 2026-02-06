# AGENT_SCOPES

This file defines where each agent should focus by default to avoid stepping on other areas.
Agents may inspect other areas for context, but must stay in-lane for modifications unless approved.

---

## Systems Designer Agent (Architecture Integrity)

Primary focus:
- src/lux/app/* (bootstrap, lifecycle, navigation)
- src/lux/ui/qt/* (app_shell, main_window, theme, styles, widgets)
- src/lux/core/* (types/time/errors/logging/settings)
- src/lux/data/* (db, migrations, models, repositories)
- docs/* and /AI_BRAIN/*

Typical outputs:
- Approve/reject architecture-impacting changes
- Define/adjust system-level interfaces
- Enforce layering and boundaries

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

---

## Test Engineer Agent (Quality & Risk)

Primary focus:
- tests/unit/*
- tests/integration/*
- UI flow test planning around:
  - src/lux/ui/qt/main_window.py
  - src/lux/ui/qt/app_shell.py
  - navigation transitions

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

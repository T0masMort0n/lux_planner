# PROJECT_ARCHITECTURE

## Layered Structure (Non-Negotiable)

### System Layer (UI + orchestration)
Owns:
- AppShell (global layout + structure)
- Navigation
- Theme system (QSS/tokens/widgets)
- UI primitives and reusable widgets

### Feature Layer (business capability modules)
Owns:
- Feature-specific domain/service/repo abstractions (when applicable)
- Feature UI content (panels/views/controllers) that plugs into system UI patterns

Rule: Features never import each other.

### Core Layer (shared foundations)
Owns:
- Settings
- Shared utilities (time/types/errors/logging)
- Storage infrastructure and shared DB access patterns

---

## Repo Implementation Map (Current)

### System Layer (primary locations)
- src/lux/ui/qt/app_shell.py
- src/lux/ui/qt/main_window.py
- src/lux/ui/qt/theme.py
- src/lux/ui/qt/styles/*  (tokens, constants, qss_build)
- src/lux/ui/qt/widgets/* (buttons/cards/dialogs/splitters/typography)
- src/lux/app/navigation.py
- assets/themes/*.qss

### Core Layer
- src/lux/core/* (settings, time, types, errors, logging)
- src/lux/data/db.py
- src/lux/data/migrations/*
- src/lux/data/models/*
- src/lux/data/repositories/*

### Feature Layer (examples)
- src/lux/features/journal/*
- src/lux/features/scheduler/*
- src/lux/features/todo/*
- src/lux/features/meals/*
- src/lux/features/exercise/*
- src/lux/features/goals/*

---

## Boundary Rules

### Features MUST NOT:
- Import another feature module (directly or indirectly)
- Modify AppShell layout patterns
- Implement their own theming or animation systems
- Implement navigation/routing logic internally

### Features MAY:
- Define feature-level domain/service/repo (internal to that feature)
- Use system widgets/tokens
- Expose feature entry points via the system registry / navigation

---

## Communication Between Features

All cross-feature communication must happen via system-level services/interfaces.
No feature-to-feature imports.

If feature A needs data from feature B:
- define a system-level interface/service (Core/System layer) that both can depend on
- feature B provides an implementation behind that interface (without A importing B)

---

## DB / Repository Pattern

- UI layer never talks to DB directly.
- Repositories encapsulate DB operations.
- Services orchestrate repository calls + business logic.
- DB is shared across modules via the shared db layer.

---

## UX Consistency Ownership

- Motion consistency is system-owned (no feature animations).
- Theme consistency is system-owned (no feature styling beyond tokens).
- Layout patterns are system-owned (features supply content).

---

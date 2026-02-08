# PROJECT_ARCHITECTURE (UPDATED)

This document defines the **non‑negotiable structural architecture** of Lux.
It now reflects the **System Interaction Contracts**, **Template Pack system**, and the **Visual Designer role separation**. fileciteturn4file0

---

## Layered Structure (Non‑Negotiable)

### 🧱 System Layer (UI + Orchestration)
Owns all **global behavior, interaction frameworks, and visual systems**.

Includes:
- AppShell (global layout + structure)
- Navigation framework
- Theme system (tokens, QSS, visual variables)
- UI primitives and reusable widgets
- **Drag & Drop framework**
- **Explore Mode framework**
- **Sharing infrastructure (share service, inbox, update proposals)**
- **Template Pack infrastructure**
- System overlays (bottom panel, safe release zones, system surfaces)
- Element metadata registry (for Explore Mode)

System layer defines **how the app behaves** at an interaction level.

---

### 🧩 Feature Layer (Business Capability Modules)
Owns:
- Feature-specific domain logic
- Feature services and repositories (internal)
- Feature UI content that plugs into system UI patterns
- Feature metadata registration (for Explore Mode)

Features provide **content and meaning**, not system behavior.

Rule: **Features never import each other.**

---

### ⚙️ Core Layer (Shared Foundations)
Owns:
- Settings
- Shared utilities (time/types/errors/logging)
- Storage infrastructure and DB access patterns
- Canonicalization utilities (for deduplication, packs, sharing)
- Identity / scope concepts (personal, household, trusted, external)

Core supports both System and Features without introducing UI behavior.

---

## Repo Implementation Map (Current)

### System Layer (Primary Locations)
- src/lux/ui/qt/app_shell.py
- src/lux/ui/qt/main_window.py
- src/lux/ui/qt/theme.py
- src/lux/ui/qt/styles/*
- src/lux/ui/qt/widgets/*
- src/lux/app/navigation.py
- src/lux/system/dragdrop/*
- src/lux/system/explore_mode/*
- src/lux/system/sharing/*
- src/lux/system/packs/*
- assets/themes/*.qss
- assets/font_schemes/*.json  # typography schemes (token → font-family stacks)

### Scheduler System Spine (System Interaction Surface)

Scheduler is classified as a system-level orchestration surface.

System layer responsibilities:
- Scheduling data service
- Provider registry
- Cross-feature scheduling contracts

Features:
- Must use system scheduler service
- Must not implement scheduling write paths
- Must not import other features for scheduling

This ensures scheduling remains platform infrastructure rather than feature coupling.

### Core Layer
- src/lux/core/*
- src/lux/data/db.py
- src/lux/data/migrations/*
- src/lux/data/models/*
- src/lux/data/repositories/*

### Feature Layer (Examples)
- src/lux/features/journal/*
- src/lux/features/scheduler/*
- src/lux/features/todo/*
- src/lux/features/meals/*
- src/lux/features/exercise/*
- src/lux/features/goals/*

---

## System Interaction Ownership (Critical)

The following are **system-level frameworks**:

| Framework | Owner |
|-----------|-------|
| Drag & Drop | System Layer |
| Safe Release | System Layer |
| Explore Mode | System Layer |
| Sharing / Inbox | System Layer |
| Template Packs | System Layer |
| Navigation | System Layer |
| Theme Tokens | System Layer (Visual Designer defines visuals) |

Features may only **register with** these systems, not implement their own versions.

---

## Boundary Rules

### Features MUST NOT:
- Import another feature module
- Modify AppShell layout patterns
- Implement their own theming or animation systems
- Implement navigation logic
- Implement drag/drop logic
- Implement sharing flows
- Implement pack import/export systems

### Features MAY:
- Define internal domain/service/repo logic
- Use system widgets and tokens
- Register drop zones, draggable items, metadata, or pack adapters via system interfaces
- Expose entry points via the system registry

---

## Communication Between Features

All cross-feature interaction must happen via **system-level services or contracts**.

Example patterns:
- Task → Scheduler uses **Schedule operation** in drag/drop framework
- Recipe → Grocery uses **Add to Collection operation**
- Packs import items via **system pack service**
- Sharing uses **system share service**

No feature-to-feature imports are allowed.

---

## Data Scope & Ownership

Every item must support scope concepts:
- Personal
- Household
- Shared copy
- Trusted contact (optional auto-accept for allowed types)

Sharing is copy-first. No automatic propagation.

---

## DB / Repository Pattern

- UI layer never talks to DB directly
- Repositories encapsulate DB operations
- Services orchestrate repository calls and logic
- DB is shared via Core data layer

---

## Visual System Ownership

- Visual Designer owns fonts, colors, tokens, QSS
- Systems Designer owns layout structure and UI frameworks
- Features may only consume tokens, never define their own styles

### Typography Schemes (Tokens + Font Packs)

Typography schemes are system-owned **mechanism** + visual-owned **content**:

- System defines typography token names and applies schemes during QSS application.
- Visual Designer provides scheme JSON mappings in `assets/font_schemes/*.json`.
- Theme QSS must reference tokens (e.g., `font-family: var(--font-body);`) and must not hardcode scheme-specific stacks.
- The system applies schemes via Qt-safe substitution limited to `font-family` declarations (no global replacements).

---

## UX Consistency Ownership

System owns:
- Motion consistency
- Interaction patterns
- Layout patterns
- Visual token system

Features supply content only.

---

## Architectural Intent

Lux is structured as a **life system platform**, not a feature collection.
System layer ensures:

- Consistent interaction model
- Predictable behavior
- Scalable expansion
- Low cognitive load
- Long-term maintainability


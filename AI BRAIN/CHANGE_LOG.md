
## 2026-02-06 — System Contracts & Governance Consolidation
**User Problem / Goal:**  
Prevent system drift and ensure all future development aligns with interaction-first life system design.

**What Changed (high level):**  
- Adopted System Interaction Contracts as governing law  
- Defined Drag/Drop, Explore Mode, Sharing, Packs as system frameworks  
- Introduced Visual Designer role  
- Formalized admin governance (Product Driver + AI)

**Why This Matters:**  
Establishes Lux as a coherent platform rather than feature collection.

**Rules / Constraints Updated:**  
System contracts now override local design choices.

**Follow-ups / TODOs:**  
- Implement system service scaffolding
- Expand pack adapters

**Signed:** Product Driver & AI Admin

2026-02-06 — Cross-Theme Typography System Activation (Visual Layer)

User Problem / Goal:
Ensure font schemes selected in Settings visually propagate across all themes with consistent hierarchy and without hardcoded font stacks blocking the system.

What Changed (high level):

All theme QSS files converted from fixed font-family stacks to system typography tokens

Visual hierarchy standardized across themes:

UI surfaces → --font-ui

Titles / section headers → --font-heading

Metadata / captions → --font-micro

Added a bundled-safe visual font scheme to ensure reliable typography identity using included fonts

Why This Matters:
Typography is now:

centrally controlled

theme-independent

instantly switchable via scheme selector

visually consistent across the product

This unlocks typography as a system-level design lever rather than a per-theme styling detail.

Rules / Constraints Observed:

No system mechanics altered

No new tokens introduced

No layout, spacing, color, or interaction changes

Strict adherence to Typography Token Contract and Agent Scope boundaries

Follow-ups / TODOs:

Test cross-theme switching for visual regressions

Monitor layout density under Compact & Editorial schemes

Signed: Visual Designer Agent 🎨

### Change: Scheduler System Spine Hardening (DI Consistency)
**Date:** 2026-02-07  
**Owner:** Coder Agent (System Layer Revision under Systems Designer Direction)

**Problem:**  
Scheduler system layer had inconsistent dependency injection patterns and registry exposure.

**Solution (system mechanics only):**
- `SystemServices` exposes only `scheduler_service`.
- Registry access consolidated via `scheduler_service.registry`.
- `SchedulerService` now requires injected repo + registry.
- Bootstrap is sole DB lifecycle owner.

**Architectural Impact:**
This locks Scheduler into the platform’s system layer:
- Scheduler becomes a **system orchestration surface**.
- Future features will schedule via system service, not feature imports.
- Prevents duplicate registry/state patterns.

**Files Changed:**
- src/lux/app/services.py
- src/lux/app/bootstrap.py
- src/lux/core/scheduler/service.py

**Signed:**  
Systems Designer Agent (Architecture Review)  
Coder Agent (Implementation)

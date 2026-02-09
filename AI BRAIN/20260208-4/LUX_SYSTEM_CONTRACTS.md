
# LUX PLANNER — SYSTEM INTERACTION & SHARING CONTRACTS (MASTER)

---

## CORE INTERACTION PHILOSOPHY
"If it exists, you can yeet it somewhere else."
Direct manipulation is a system-level principle. Items should be draggable and composable with minimal exceptions.

---

## SECONDARY SOURCE PANEL CONTRACT (SYSTEM-OWNED)

Cross-feature workflows require simultaneous access to a primary workspace and secondary item sources. This contract defines the system pattern for that interaction.

### Purpose
Enable composition workflows (e.g., Meals → Scheduler, Workouts → Planner) without fragmenting AppShell structure or creating multi-feature layout chaos.

### Structural Role
| Region | Role |
|-------|------|
| Left Panel | Feature-local navigation |
| Right Main Panel | Primary feature workspace |
| Secondary Source Panel (collapsible) | System-owned source surface for cross-feature item access |

### Behavioral Model
- Primary feature = workspace/canvas
- Secondary panel = item source library
- Secondary panel does NOT function as a second primary feature
- Secondary panel is opened intentionally and is dismissible

### Content Rules
Secondary panel may include:
- Item lists
- Search/filter
- Drag-enabled item surfaces

Secondary panel must NOT include:
- Deep feature navigation
- Settings
- Multi-step flows
- Full feature UI replicas

### Source Curation
Only item types relevant to the active primary feature may appear in the source panel. Type eligibility is determined by the system interaction registry.

### Interaction Rules
- Drag/drop from source panel uses existing system drop contracts
- Secondary panel does not own scheduling, saving, or global actions
- Secondary panel cannot alter AppShell layout

### Governance
This pattern is system-owned and must be implemented at the AppShell layer. Features may provide item sources but may not define new layout behaviors.

---

## LAYOUT CONTRACT SPECIFICATION — APPSHELL LEFT COLUMN ISOLATION
Surface isolation, containment guarantees, resize rules, and prohibited patterns governing NavSurface, FeatureLeftSurface, and RightContentSurface.

---

## PROJECT DUMP GENERATION CONTRACT (SYSTEM-OWNED)
Dump generation is system infrastructure. Only canonical tools, strict exclusions, and external output locations are permitted.

---

## THEME PIPELINE SSOT (SYSTEM-OWNED)
Theme and typography application is a single-source-of-truth pipeline. Only the canonical module may apply QSS or call setStyleSheet.

---

## GOVERNANCE
These contracts override feature decisions. Systems Designer approval required for structural changes.

## Appendix — Task Hierarchy & State-Changing Drop Contract

- Hierarchy field: `task_definitions.parent_task_id`
- Completion derived by panel query scope
- System DnD only; no feature drag systems
- Typed payload discriminator required
- Session-local cancellation only
- Drops mutate due_date or create occurrence

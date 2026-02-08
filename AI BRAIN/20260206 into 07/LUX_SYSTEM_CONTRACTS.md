
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

## SYSTEM UI LAYERS
Left: Navigation
Right: Feature Content
Bottom: Explore Info Surface

---

## GOVERNANCE
These contracts override feature decisions. Systems Designer approval required for changes.

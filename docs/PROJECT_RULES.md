PROJECT_RULES.md



These rules override default GPT behavior.

🧩 EDITING FORMAT RULE

If providing multiple edits to one file:

Give starting and ending line numbers

Show before and after code

Provide edits bottom-to-top order

This prevents line shift confusion.

🏗 SYSTEM UI RULES

System UI defines layout patterns

Features only supply content

No feature-level animation systems

No feature-level theming

All styling comes from system theme layer

🚧 FIRM BOUNDARIES (DO NOT CROSS)

- A feature tries to modify AppShell layout
- Feature starts importing another feature
- Feature introduces its own animation system
- You add feature-specific styling instead of system tokens
- Navigation logic leaks into features

⚡ PERFORMANCE RULES

No heavy operations on startup

Long operations must be cancellable

Queries must be bounded

Historical data must not slow daily use

🗂 DATA LIFECYCLE

Nothing is deleted, only archived

Archived data hidden, not removed

🧠 TASK MODEL

Tasks are definitions
Occurrences are instances
Completion is stored on occurrences

🎨 UI PHILOSOPHY

Stable layouts

Soft animations

No jumpiness

Visual calmness

Luxury feel, not flashy

🗺 FILE 3 — PROJECT_ROADMAP.md
PROJECT_ROADMAP.md
PHASE 1 — SYSTEM FOUNDATION (Current)

✔ AppShell layout
✔ Overlay navigation
✔ Theme system
✔ Feature registry
✔ Modular project structure

PHASE 2 — CORE FEATURES

Journal module

Scheduler module

Shared data interfaces

PHASE 3 — CROSS-FEATURE INTERACTION

Linking journal to days

Tasks visible in scheduler

Habit data influencing planner

PHASE 4 — POLISH LAYER

Typography refinement

Spacing system

Motion consistency

PHASE 5 — EXTENSION

Meals app

Exercise app

Goals app

PHASE 6 — SYSTEM INTELLIGENCE

Smart suggestions

Behavior insights

Automation layer
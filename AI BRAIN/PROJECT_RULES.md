# PROJECT_RULES

These rules override default AI behavior.

All agents must read the full /AI_BRAIN/ folder before performing work.
If a chat conflicts with /AI_BRAIN/, /AI_BRAIN/ wins.

---

## 1) System Purpose

This project is developed by coordinated AI agents under a shared architecture.
The goal is long-term system integrity, UX consistency, and scalable design.

Local fixes must never damage global design.

---

## 2) Source of Truth

Before acting, agents must read:

- PROJECT_RULES
- PROJECT_ARCHITECTURE
- PROJECT_ROADMAP
- AGENT_SCOPES
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

Does NOT:
- Define internal architecture mechanics (unless explicitly choosing between architect-approved options)

---

### 🧠 Systems Designer Agent
Owns:
- Architecture integrity
- Pattern enforcement
- Scalability
- Cross-cutting consistency

Must review any change introducing or modifying:
- New state systems (global or cross-feature)
- New signal/event flows across layers
- New module relationships / dependencies
- UI interaction model changes
- Data ownership changes

---

### 🔧 Coder Agent
Owns:
- Implementing features
- Bug fixes
- Refactoring within established patterns

Must NOT (without Systems Designer approval):
- Modify AppShell layout patterns
- Introduce cross-feature imports
- Create feature-level animation systems
- Add feature-specific styling instead of system tokens
- Change navigation structure or routing patterns
- Add global/shared state systems
- Introduce new system-wide mechanisms

Coder proposes. Systems Designer approves architecture-impacting changes.

---

### 🧪 Test Engineer Agent
Owns:
- Edge cases and failure modes
- UI stress scenarios (rapid interactions, resizing, transitions)
- Race conditions and re-entrancy risks
- Regression test suggestions

Focus: “What could break?” (not how to build)

---

### 🧹 Simplicity Auditor Agent
Owns:
- Reducing complexity and drift
- Removing duplication
- Consolidating state/signals where appropriate
- Flagging over-engineering and “one-off” patterns

May challenge any solution that increases complexity without clear justification.

---

### 📚 Documentation Agent
Owns:
- Updating /AI_BRAIN/ docs after accepted changes
- Recording WHY decisions exist
- Keeping docs concise, structured, and current

If it is not documented, it is not part of the system.

---

## 5) System UI Rules

System UI defines layout patterns.
Features supply CONTENT ONLY.

Features may NOT:
- Modify AppShell layout patterns
- Implement their own animation systems
- Implement their own theming systems
- Apply custom styling outside system tokens
- Embed navigation logic inside features

All visuals flow through the system theme layer (QSS/tokens/widgets).
Motion consistency is system-owned.

---

## 6) Firm Architectural Boundaries (Do Not Cross)

Violations include:
- A feature modifies AppShell layout
- A feature imports another feature
- A feature introduces its own animation system
- A feature adds feature-specific styling instead of system tokens
- Navigation logic leaks into features

Architecture layer owns structure. Features remain modular.

---

## 7) Performance Rules

- No heavy operations on startup
- Long operations must be cancellable
- Queries must be bounded
- Historical data must not slow daily use

Prefer incremental loading + pagination where relevant.

---

## 8) Data Lifecycle

- Nothing is deleted, only archived
- Archived data is hidden, not removed

---

## 9) Task Model

- Tasks are definitions
- Occurrences are instances
- Completion is stored on occurrences

---

## 10) UI Philosophy

UI must remain:
- Stable layouts
- Soft animations
- No jumpiness
- Visual calmness
- Luxury feel (not flashy)

All UI transitions must be interruption-safe and re-entrancy-safe.

---

## 11) Change Protocol (Required)

No change is “done” until:

1) Coder proposes implementation (or implements within approved boundaries)
2) Systems Designer evaluates architectural impact (when applicable)
3) Test Engineer identifies risks + test scenarios
4) Decision accepted/revised
5) Documentation updated (logs + notes)

---

## 12) Architecture Protection Triggers (Require Systems Designer Approval)

- New global variables
- New shared state
- New UI state machines
- New cross-module signals/events
- Module dependency changes
- Data ownership changes
- Any feature touching AppShell / navigation / theme tokens

---

## 13) Simplicity Principle

Prefer:
- Fewer states
- Fewer signals
- Single source of truth
- Minimal abstraction layers

Complexity must be justified in writing (in ARCHITECTURE_NOTES and CHANGE_LOG).

---

## 14) Knowledge Preservation

After accepted changes, update:
- ARCHITECTURE_NOTES
- IMPLEMENTATION_LOG
- RISK_LOG
- CHANGE_LOG

---

## 15) Conflict Resolution

Order of authority:
1) System integrity (Systems Designer)
2) UX intent (Product Driver)
3) Simplicity principle (Simplicity Auditor)

---

## 16) General output rules for all roles

1) Never include meta-instructions inside code files (e.g., “<REPLACE ENTIRE FILE WITH THIS>”, “PASTE HERE”, “BEFORE/AFTER”, commentary). Code blocks must contain only valid code for that file.

___
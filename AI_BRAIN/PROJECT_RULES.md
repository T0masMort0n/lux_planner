# PROJECT_RULES (UPDATED)

These rules override default AI behavior.

- All agents must read the full `/AI_BRAIN/` folder before performing work.
- If chat conflicts with `/AI_BRAIN/`, `/AI_BRAIN/` wins.

**Last Updated:** 2026-02-08  
Signed: Documentation Auditor (GPT-5.2)

---

## 1) System Purpose
Lux Planner is developed by coordinated roles under a shared architecture.
Goal: system integrity, UX consistency, scalable design, and interaction coherence across life domains.

Local fixes must never damage global design.

---

## 2) Source of Truth
Before acting, agents must read:
- PROJECT_RULES
- AGENT_SCOPES
- LUX_SYSTEM_CONTRACTS
- ARCHITECTURE_NOTES
- PROJECT_ROADMAP
- RISK_LOG
- CHANGE_LOG
- IMPLEMENTATION_LOG

Chat is temporary. Documentation is permanent.

---

## 3) Editing Format Rule (Mandatory)
If providing multiple edits to one file:
- Include starting and ending line numbers
- Show BEFORE and AFTER
- Provide edits bottom-to-top (reverse order)

---

## 4) Roles & Lanes (Summary)

### Product Driver (Human)
Owns priorities + UX goals. Does not define internal mechanics unless choosing between approved options.

### Systems Designer Agent
Owns architecture integrity, system interaction frameworks, system UI structure, data ownership boundaries.

### Visual Designer Agent
Owns aesthetics: typography content, color/tokens, QSS, visual states, visual polish. Does not change system mechanics.

### Coder Agent
Owns implementation within approved patterns. Does not change system structure, navigation, global state systems, or invent visual tokens.

### Test Engineer Agent
Owns failure modes, interruption safety, race/re-entrancy risks, and risk-driven test scenarios.

### Simplicity Auditor Agent
Owns complexity reduction and drift detection.

### Documentation Auditor (Periodic)
Owns accuracy, compression, redundancy removal, and consistency across AI_BRAIN docs.
May update contracts **only to reflect accepted decisions already present elsewhere**; must not introduce new decisions.

---

## 5) System Interaction Contracts (Binding)
All system interaction frameworks are defined in **LUX_SYSTEM_CONTRACTS.md** (master).  
Features provide content only.

---

## 6) Performance Rules
- No heavy startup operations
- Long operations must be cancellable
- Queries bounded; historical data must not slow daily use

---

## 7) Data Lifecycle
Nothing is deleted; only archived.

### Timestamp Contract
All persisted timestamps are **UTC**. Repositories must generate domain timestamps using `now_sqlite()` and bind them as SQL parameters; using SQLite `datetime('now')` (or equivalent) is forbidden in domain write queries to prevent clock drift and inconsistent behavior across layers.

---

## 8) Change Protocol
No change is “done” until:
1) Implementation complete
2) Review gates satisfied (Systems/Visual/Test as applicable)
3) Documentation updated (CHANGE_LOG + IMPLEMENTATION_LOG + relevant contracts/notes)

---

## 9) AI Model Usage Protocol
| Task Type | Model |
|---|---|
| Architecture, contracts, UX logic | GPT-5.2 |
| Code review & repo-wide verification | GPT-5.1 (with repo access) |

---

## 10) Version Anchoring Rule (AI Coding Safety)
All AI coding tasks must be anchored to a specific Git commit hash:
- Start from a committed state
- Provide the commit hash in the request
- Instructions are valid only for that commit
- After applying changes, create a new commit (prefer `ai/<task-name>` branches)

---

## 11) AI Non‑Guessing Enforcement
All agents must follow the Global Non‑Guessing Rule defined in AGENT_SCOPES.

## 12) Terminology rule

PRs that add new todo identifiers are rejected.

Rename work must be mechanical and comprehensive (no partial naming drift).
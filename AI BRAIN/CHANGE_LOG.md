# CHANGE_LOG

Use this file as the project’s “institutional memory.”
It records WHY changes were made in user-facing terms, plus the rule implications for future work.

Owned by the Documentation Agent (with input from the Systems Designer).

---

## Template

## YYYY-MM-DD — <short title>
**User Problem / Goal:**  
**What Changed (high level):**  
**Why This Matters:**  
**Rules / Constraints Updated:**  
**Follow-ups / TODOs:**  

---

## Entries

(Empty by default — add entries as decisions are accepted and merged.)

## 2026-02-05 — Add starter UIs for Exercise, Goals, and refresh To Do
**User Problem / Goal:**  
Provide attractive, system-themed starter UIs for remaining feature modules (exercise/goals) and improve the basic To Do UI.

**What Changed (high level):**  
- Added richer, card-based sample layouts for Exercise and Goals (left panel + right view).  
- Refreshed To Do left/right UIs to better match the system look while keeping existing controller wiring.

**Why This Matters:**  
The team can now iterate on feature wiring and data flows without blocking on layout scaffolding, while keeping feature boundaries intact.

**Rules / Constraints Updated:**  
- None (all changes stay within feature UI content; no new system mechanisms).

**Follow-ups / TODOs:**  
- Wire buttons to feature controllers/services once UX flows are finalized.  
- Add selection + details flow for To Do (requires system-approved interaction model).  

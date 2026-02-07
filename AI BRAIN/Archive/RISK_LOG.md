
### Risk: Drag/Drop Framework Instability
**Date:** 2026-02-06  
**Triggered By Change:** System Interaction Contracts  
**Risk Description:** Drag operations may leave stuck overlays, un-cleared highlights, or partial state if interrupted (resize, ESC, rapid input).  
**Likely Causes:**
- Incomplete cancel handling
- State not reset on interruption
**Suggested Tests / Scenarios:**
1. Drag while resizing window
2. Rapid drag/cancel cycles
3. ESC mid-drag
**Mitigations / Guardrails:**
- Centralized drag state manager
- Strict cancel pathway tests

**Signed:** Product Driver & AI Admin


### Risk: Incorrect Deduplication on Pack Import
**Date:** 2026-02-06  
**Triggered By Change:** Template Pack System  
**Risk Description:** Items like ingredients may merge incorrectly or create excessive duplicates.  
**Likely Causes:**
- Poor canonical key logic
- Low-confidence merges misclassified
**Suggested Tests / Scenarios:**
1. Import same pack multiple times
2. Import conflicting metadata variants
3. Review merge workspace flow
**Mitigations / Guardrails:**
- Safe default import mode
- Merge review workspace

**Signed:** Product Driver & AI Admin

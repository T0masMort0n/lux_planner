
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

### Risk: Typography Scheme Drift / Substitution Regressions
**Date:** 2026-02-06  
**Triggered By Change:** System Typography Schemes (Fonts + Tokens + Settings)  
**Risk Description:** Typography schemes may silently fail to apply or drift over time (e.g., themes reintroduce hardcoded `font-family` stacks; token substitution stops matching; duplicate theme modules cause edits to land in the wrong file; packaged builds miss asset roots).  
**Likely Causes:**
- Theme QSS not consistently using `font-family: var(--font-*)`
- Token contract expanded without governance
- Unsafe/global string replacement reintroduced
- Duplicate / unused theme module copies
- Packaged asset root resolution issues
**Suggested Tests / Scenarios:**
1. Switch theme + switch font scheme repeatedly (confirm immediate application)
2. Verify no font re-registration on scheme/theme switch
3. Introduce an invalid/missing scheme file (confirm fail-soft)
4. Packaged build smoke test for font registration + scheme loading
**Mitigations / Guardrails:**
- System-owned token whitelist + bounded substitution limited to `font-family`
- Visual Designer rule: themes must not hardcode scheme-specific font stacks
- Keep a single authoritative `src/lux/ui/qt/theme.py` in repo
- Add a lightweight regression test/checklist for scheme application

**Signed:** Systems Designer Agent

### Risk: Model Context Mismatch During Reviews
**Date:** 2026-02-08  
**Description:** Reviews performed without repo visibility may miss integration issues.  
**Mitigation:** Use GPT-5.1 with repo access for code reviews.  
**Signed:** Systems Designer Agent

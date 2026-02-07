
### Decision: Establish System Interaction Contracts + Admin Governance
**Date:** 2026-02-06  
**Owner:** Systems Designer Agent (Admin Decision — Product Driver + AI Admin)  
**Context:** The project matured from feature scaffolding to a system-level life platform. Multiple cross-feature interaction models (drag/drop, sharing, packs, explore mode) were being defined without a single architectural consolidation point.  
**Decision:** Adopt **LUX_SYSTEM_CONTRACTS** as system law. Formalize Drag/Drop, Explore Mode, Sharing, Template Packs, and System Area Taxonomy as system-layer frameworks. Introduce Visual Designer Agent as separate aesthetic authority. Establish Product Driver + AI as admin governance layer.  
**Why:** Prevent architectural drift, feature silos, and visual inconsistency. Enable scalable system evolution while preserving simplicity and trust-first UX.  
**Rules Introduced / Updated:**
- System owns interaction frameworks
- Features provide content only
- Copy-first sharing model
- Packs behave like playlists
- Visual Designer owns cosmetics only
- Admin decisions must be signed
**System Implications:**
- New system directories/services expected
- Future features must integrate via system contracts
- Visual work separated from structural work
**Files / Areas Affected (high level):**
- LUX_SYSTEM_CONTRACTS
- PROJECT_RULES
- PROJECT_ARCHITECTURE
- AGENT_SCOPES

**Signed:** Product Driver & AI Admin

---

### Decision: Typography as a System-Owned Surface (Tokens + Font Schemes)
**Date:** 2026-02-06  
**Owner:** Systems Designer Agent (Reviewed implementation by Coder Agent)  
**Context:** Visual themes need to support multiple typography “schemes” (like Obsidian) without duplicating font-family stacks across every theme QSS. Qt/QSS also does not reliably support CSS custom properties at runtime, and bundled fonts are not automatically registered.  
**Decision:**  
- Typography is treated as a **system surface** (mechanism + storage + settings), not a theme-by-theme one-off.  
- The System defines a **Typography Token Contract** (system-owned names): `--font-ui`, `--font-body`, `--font-heading`, `--font-mono`, `--font-micro`.  
- The Visual Designer provides **Font Scheme content** as reusable mappings (token → `font-family` stack) in `assets/font_schemes/<id>.json`.  
- Theme QSS must reference tokens (e.g., `font-family: var(--font-body);`) and must not hardcode scheme-specific font stacks.  
- Because Qt/QSS support for `var(...)` is unreliable, the System applies schemes via **safe, bounded substitution** (only inside `font-family:` declarations).  
- The System performs **bundled font registration once per app lifecycle** (bounded to `assets/fonts/**`) before any QSS is applied.

**Why:**  
- Prevents theme coupling and reduces duplication/drift (any theme can pair with any scheme).  
- Keeps typography scalable and theme-agnostic while preserving clear ownership boundaries: mechanism/system vs content/visual.  
- Maintains fail-soft startup: invalid or missing scheme files never block app launch.

**Rules Introduced / Updated:**  
- Themes must use typography tokens; schemes define font stacks.  
- New typography tokens require Systems Designer approval (system contract change).  
- Font scheme IDs must be sanitized to prevent path traversal; scheme loading must fail-soft.

**Files / Areas Affected (high level):**  
- System UI bootstrap (`src/lux/ui/qt/theme.py`)  
- Assets (`assets/fonts/**`, `assets/font_schemes/**`)  
- System settings + Settings UI (font scheme selection)

**Signed:** Systems Designer Agent

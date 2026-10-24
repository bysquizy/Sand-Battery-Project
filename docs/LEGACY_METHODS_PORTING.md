# Legacy study archive → Sand Battery Studio feature mapping

**Comparison performed:** 24 October 2026.  
**Primary artifact:** user-provided `kum-bataryasi-proje-main.zip`, consisting of a 1,978-line `main.py` and a `requirements.txt`.  
**Reference web URL supplied by owner:** https://kum-bataryasi.streamlit.app/

The Streamlit site itself could not be fetched through the available web inspection tool. Therefore **this comparison is grounded in the uploaded source code**, not in a claim to have reviewed every rendered browser page. The original archive code was inspected for engineering workflows; the new implementation uses independently written calculations and the current project's existing numerical engine. No third-party copyright/license entitlement is assumed.

## Calculation and interface mapping

| Feature in original ZIP | Where it exists in Sand Battery Studio | Verification scope |
| --- | --- | --- |
| Temperature-dependent sensible enthalpy and charge/hold/discharge | `engine/materials.py`, `engine/physics.py` | Existing energy balance tests |
| Cylindrical silo geometry and insulation resistance | `engine/physics.py` | Formula tests and design summary |
| CSP source model | `engine/solar.py`, Dashboard | Constant DNI/efficiency scenario, not weather |
| Idealized composite materials | `engine/materials.py`, Material Atlas | Rule-based mixtures, not measured composites |
| Finite-volume 1-D thermal profile | `engine/thermocline.py`, Research Lab | Different numerical method; direct contact research topology |
| Multiple comparison diagrams and animated silo | `visuals.py`, Dashboard | Illustrations, not sensor/CFD data |
| Module count vs heat-leak analysis | **New:** `engine/design_lab.py`, Thermal Design Studio | Fixed total thermal capacity; geometry only |
| No-load cooling curves and cumulative thermal loss | **New:** `engine/design_lab.py`, Thermal Design Studio | 0-D cooling ODE with cp(T); Newton limit test |
| Required volume for target stored MWh | **New:** `engine/design_lab.py`, Thermal Design Studio | Theoretical MWh, not usable delivered energy |
| Insulation thickness and approximate shell volume | **New:** `engine/design_lab.py`, Thermal Design Studio | Sidewall conduction, cap volume approximation |
| Cooling-driven radial insulation study | **New:** Thermal Design Studio | Quasi-steady wall profile, not transient radial CFD |
| Constrained height/diameter geometry screening | **New:** Thermal Design Studio | Geometric feasibility only, not structural safety |
| Multi-configuration save/load via JSON | Current Dashboard exports inputs and results; rich multi-configuration import **not yet migrated** | Future release, guarded schema required |
| Original Finnish/Turkish app presentation | New pages are English, consistent with ESE101 project decision | Current original site not browser-audited |

## Why not copy the original 1,978-line `main.py` directly?

- The archived app mixes UI and scientific calculations, which makes numerical verification and maintenance harder.
- The current simulator already has distinct `engine/`, `visuals.py`, `pages/` and `tests/` modules.
- Neither author ownership nor a permissive license for republishing the old code is established in the supplied artifact.
- Models for direct-contact flow and closed-pipe sand batteries must not be silently presented as physically equivalent.

## Actual research documents reviewed

1. Bošnjaković & Santa (2026), *Sand Batteries for Thermal Energy Storage: A Review...* — source scope and system limitations. https://doi.org/10.3390/cleantechnol8050165
2. Team-supplied *Sand Battery Research Polar Night Energy* DOCX — company claims and technology narrative; not independent field validation.
3. Team-supplied *Sand Battery Source Check Enhanced Research Audit* DOCX — source confidence codes (P1, P2, S1, S2, U) and verdicts. Original claims must retain their attribution.
4. NREL report 84728 — characterized silica properties and phase-transition warning. https://www.nrel.gov/docs/fy23osti/84728.pdf
5. Vatajankoski operator vs Polar Night Energy developer specifications for Kankaanpää (100 vs 200 kW thermal, respectively). https://www.vatajankoski.fi/en/projects/sand-battery/ and https://polarnightenergy.com/reference/worlds-first-sand-battery/

**No experimental calibration, construction approval, verified LCOH value or electricity-to-electricity round-trip performance is claimed.**

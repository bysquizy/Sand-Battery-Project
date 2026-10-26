# v2.2 Beta — Design-System and Research UX Release

**Date:** 24 October 2026  
**Project:** Sand Battery Studio · IZTECH Department of Energy Systems Engineering · ESE101 Group 8  
**Lead developer:** Yağız Topaç (@bysquizy)

## What changed

- A common CSS-only styling module (`ui_theme.py`), based on the uploaded Claude UI proposal, unifies dashboard, research laboratory, material atlas and virtual experiments.
- Third-party font loading was removed; system fonts keep the hosted website independent of Google Fonts.
- Reduced-motion preferences, visible keyboard focus, responsive metric card sizing and consistent explanatory labels were added.
- Navigation is grouped into Simulation / Research & Comparison / Model Verification, with a short onboarding guide.
- Three **illustrative** presentation presets speed up the ESE101 live demonstration without pretending to reproduce measured field operation.
- New Light mode skips heavy animated 3D rendering on low-power devices.
- The Evidence Library presents a downloadable **model → equation → research source → verification status** register.
- CODE_OF_CONDUCT, CITATION.cff, issue and pull request templates, Dependabot configuration, focused Ruff checks and regression tests were added.
- Existing thermal equations, charging models, material parameter values and numerical solvers were **not changed** by this interface release.

## Scope limitations

| Feature | Evidence | Limitation |
|---|---|---|
| Linear `cp(T)` | Thermodynamic energy integral and illustrative parameters | Does **not** reconstruct NREL DSC curves or the ~573 °C quartz phase transition |
| 0-D thermal dynamics | Numerically closed sensible-heat energy ledger | No experimental calibration, exchanger pinch or thermal bridging |
| 1-D LTE / LTNE | Direct-contact packed-bed mathematical research approaches | Not a closed-pipe Polar Night Energy physical topology |
| Exergy | Second-law upper bound | Not actual electrical power output |
| Cost / uncertainty | User assumptions and synthetic distributions | Not measured cost or statistically calibrated confidence bounds |
| 3D animation / heatmap | Model-derived visualizations | Not sensor readings or CFD |

**Kankaanpää source conflict:** Vatajankoski (100 kW/8 MWh) and Polar Night Energy (200 kW/8 MWh) have differing public output ratings. Treat the numbers as separate source assertions, not as field validation.

## Decisions deferred pending evidence or approval

- Choosing MIT/GPL/Apache license: requires group agreement and source ownership review.
- Additional contributor and advisor names: requires exact, authorized details.
- Quantitative quartz inversion heat capacity model: requires valid measured cp/enthalpy data and specimen-specific assumptions.
- Hardware, watchdog, IoT and fail-safe claims: no prototype or control system exists.
- External vendor CAPEX assumptions: no verifiable plant quote or comparable scope.
- Two-language UI: project artifacts remain English according to the team's standing requirement.
- Fake measured-versus-predicted percentages using only manufacturer power/capacity specs: not meaningful validation.

## Testing

CI runs on Python 3.13: numerical checks, Streamlit AppTest launch, theme integrity and an interactive preset case. The site remains deployed to the user-confirmed Streamlit Community Cloud URL. CI success does **not** imply manual browser/device QA.

References and methods: [ADVANCED_RESEARCH_V2.md](ADVANCED_RESEARCH_V2.md), [MODEL_VALIDATION.md](MODEL_VALIDATION.md), [SOURCE_REGISTER.md](SOURCE_REGISTER.md), and [Model Evidence register](../project_info.py).

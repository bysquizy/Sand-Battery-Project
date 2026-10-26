# Sand Battery Studio — Five-Stage Development Roadmap

**Current target release:** 1.3.0, Stage 1 (Foundation & Security).
**Application:** independent Group 8 numerical research platform, not
an experimentally validated or construction-certified thermal battery.

## Stage 1 — Code Foundation, Security & Cleanup (v1.3)

- [x] Review Python 3.13, documentation and safety-related development settings.
- [x] Restore default Codespaces/Streamlit CORS and XSRF protections.
- [x] Add bounded CSV import validation and guard the Material Atlas heatmap.
- [x] Consolidate active software-version strings and archive obsolete release notes.
- [x] Expand numerical/upload/UI regression tests and focused import linting.
- [ ] Verify the merged `main` commit and the independently hosted browser UI.
- [ ] Confirm actual output on the user's deployed Streamlit Cloud app.

**Stage 1 boundary:** do not rewrite thermodynamics, change material-property
coefficients, add paid services or assert experimental calibration.

## Stage 2 — User Experience & Scenario System

Shared `Active Scenario` state; A/B/C save/load/compare, a calmer dashboard,
clearer sidebar controls, mobile UX, local caching and lightweight navigation.

## Stage 3 — Advanced Scientific Engineering

Explain 0-D vs 1-D outputs; evidence-labeled material properties, simplified
closed-pipe heat transfer, outlet temperature and insulation limits, solver
convergence and independent validation where real data are available.

## Stage 4 — Visualization, Animation & Reporting

Physically grounded 1-D temperature animations, coherent timeline controls,
uncertainty and Pareto plots, HTML/PDF-ready scenario reports and export audit.

## Stage 5 — Research, Publication & Final QA

Centralized APA-style source records, the existing concise Research Hub,
mobile/browser testing, GitHub release/version metadata and final QA evidence.

## Quality gate for every stage

1. Feature branch and reviewed pull request.
2. Tests on Python 3.13, no newly failing regressions.
3. Documented assumptions and a changelog entry.
4. Merge only after GitHub Actions passes.
5. Clearly distinguish headless CI from live Streamlit/browser acceptance.

## Open scientific limitations

- The current linear cp(T) scenarios do not model quartz phase-transition
  enthalpy near 573 °C.
- Direct-contact 1-D/LTNE bed physics is not Polar Night Energy's embedded-pipe
  commercial layout.
- No prototype or independently calibrated experimental data exists.
- Published operator/developer Kankaanpää power ratings differ and are
  source-specific, not calibration measurements.

Old beta milestones were preserved under `docs/archive/`, rather than
interleaved with future stage commitments.

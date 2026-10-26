# Sand Battery Studio — Five-Stage Development Roadmap

**Current software release:** 2.1.0 — numerical simulation, documentation and software checks. Real-browser acceptance and measured scientific validation remain open.
**Application:** independent Group 8 numerical research platform, not
an experimentally validated or construction-certified thermal battery.

## Stage 1 — Code Foundation, Security & Cleanup (v1.3)

- [x] Review Python 3.13, documentation and safety-related development settings.
- [x] Keep Streamlit CORS and XSRF protections enabled; remove optional desktop-oriented development container configuration.
- [x] Add bounded CSV import validation and guard the Material Atlas heatmap.
- [x] Consolidate active software-version strings and archive obsolete release notes.
- [x] Expand numerical/upload/UI regression tests and focused import linting.
- [ ] Verify the merged `main` commit and the independently hosted browser UI.
- [ ] Confirm actual output on the user's deployed Streamlit Cloud app.

**Stage 1 boundary:** do not rewrite thermodynamics, change material-property
coefficients, add paid services or assert experimental calibration.

## Stage 2 — User Experience & Scenario System (v1.4)

- [x] Shared validated Active Scenario for every simulation workspace.
- [x] One global sidebar editor; local research variations explicitly labelled.
- [x] A/B/C saved scenarios and model-computed numerical comparison table.
- [x] JSON v1 save/load with strict schema and resource limits; CSV comparison.
- [x] Remove redundant Dashboard input controls and lazy-render its four views.
- [x] Preserve historical release notes under `docs/archive` rather than deleting provenance.
- [ ] Independent visual browser/mobile verification and usability review.
- [ ] Shareable cloud-backed scenario links were deliberately **not** implemented
      because this academic app has no identity service or persistent database.

## Stage 3 — Advanced Scientific Engineering (v1.5)

- [x] Distinguish 0-D uniform-body physics from 1-D axial direct-contact LTE calculations.
- [x] Add adjustable charge/discharge cutoffs and 1-D phase energy ledger.
- [x] Implement an independent simplified closed-pipe fluid/solid resistance and sensible-enthalpy model with outlet-grade constraints.
- [x] Add source-labelled tabulated cp(T), strict measured-domain checking and numerical analytical tests.
- [x] Add an optional 2-layer insulation screen; the old thermal_ua equation is unchanged.
- [x] Revise Stage 1/2 input security, wasted inactive calculations and stale simulation plots.
- [ ] Full 2-D/3-D embedded-loop CFD and commercial piping calibration (unavailable geometry/measurements).
- [ ] Sourced measured cp(T) data for each material, quartz inversion enthalpy and experimental transient validation.
- [ ] Formal grid-and-time-step asymptotic convergence analysis (initial grid sensitivity only).

## Stage 4 — Visualization, Animation & Reporting (v2.0)

- [x] Physically grounded 1-D computed axial temperature snapshots.
- [x] Interactive 3-D cylindrical map and time/height heatmap from the same solver.
- [x] Light/mobile 2-D view and selected-workspace/on-demand computations.
- [x] Model-based 0-D energy Sankey, tornado sensitivity and bounded volume/insulation tradeoff.
- [x] Self-contained, illustrated HTML, compact dependency-free PDF, scenario JSON and numeric CSV exports.
- [x] Clearly label model-specific spatial constraints, no radial CFD/no sensors.
- [ ] Owner's live desktop/mobile acceptance and optional polished video walkthrough.
- [ ] Full screen-recorded animation, chart accessibility audit and advanced Pareto proof.

## Stage 5 — Research, Publication & Final QA (v2.0)

- [x] Extend equation-to-model/source/verification mapping and source register.
- [x] Replace made-up Sankey fractions in Research Hub with nonnumeric concept blocks.
- [x] Plot source-attributed Kankaanpää/Pornainen thermal power without merging conflicting numbers.
- [x] Align README, CITATION.cff, project version, security and model limitations.
- [x] Add original accessible static architecture SVG; no runtime font or image dependencies.
- [x] Retain Group 8 names and source links; keep previous docs archive for provenance.
- [x] Automate HTML/XSS, PDF-structure, Plotly, animation and full route tests in CI.
- [ ] Owner live-browser/mobile acceptance and verification of Cloud redeployment.
- [ ] GitHub About Website field and GitHub Release creation if authorized by maintainer/admin; connector permissions may limit these.
- [ ] AI usage statement and open-source license review subject to group/course agreement.
- [ ] Final all-stages post-release audit and user-requested edits (next revision cycle).

## Cross-stage revision — Interface and security (v2.1)

- [x] Consistent nine-page user interface using native Streamlit
      theme and trusted static CSS/HTML only, with no JavaScript.
- [x] Shared contextual ribbon and Group 8 source-credit footer.
- [x] Mobile and reduced-motion layout safeguards and improved contrast.
- [x] Formula-safe CSV download for user-controlled scenario names.
- [x] Preserve explicit Streamlit CORS and XSRF protections.
- [x] Cross-page smoke/regression coverage, source limitations preserved.
- [ ] True live Cloud browser screenshot, keyboard-only and physical-phone
      acceptance: unavailable via the repository connector and text-only web crawl.
- [ ] Full upstream dependency security audit and real-world calibration:
      tests and CodeQL do not replace either.

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

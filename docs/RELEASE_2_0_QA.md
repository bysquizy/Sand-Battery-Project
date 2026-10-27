# v2.0 — Stages 4 & 5 Release and Acceptance Record

**Release objective:** Research-grade Streamlit web demo with traceable simulation
visuals, lightweight reports, curated sources, and source-control review.
**Project:** Sand Battery Studio — Group 8.
**Status:** Historical v2.0 deliverables are present on main; current software version is 2.1.0. The 26 October main baseline `d0fbc8e68cca8db3932e14af0905c15bd945719c` passed 205 automated tests. Later revisions require their own CI and deployed-commit check. Physical-phone acceptance remains open. This is not an industrial certificate.

## Stage 4 deliverables

- 1-D LTE engine now stores bounded, actual finite-volume axial snapshots and
  phase/time metadata during charging, standby and decharging.
- Plotly cylinder maps those **axial results** onto an illustrative silo wall.
  Frames use real solved profiles, not arbitrary interpolated temperatures.
- Synchronized time-versus-height heatmap from the same computed profile list.
- Source-input energy Sankey, 0-D transient curves, ±10% input perturbation
  chart and small volume/insulation design tradeoff screen.
- Self-contained HTML scenario report with inline SVG temperature plot, readable
  assumptions, source links and **the three Group 8 members**.
- Compact standards-based PDF export generated without another runtime
  dependency. A printable HTML edition retains full Unicode styling and can
  be saved to PDF in the browser.
- JSON/CSV exported alongside reports for reproducible numerical inputs.

## Stage 5 deliverables

- [Equation-to-Code Traceability](EQUATION_TRACEABILITY.md) matrix, including
  assumptions, verification tests and missing evidence.
- Research Hub: replaced decorative 75/25/57/18 Sankey with nonnumeric phase
  descriptions; added developer/operator-attributed field-ratings chart.
- Official site, GitHub and download links, version/CITATION/README aligned.
- Original architecture SVG illustration with accessibility labels and no
  external assets, CDN, Google fonts or expensive frontend packages.
- Legacy historical reports and source-audit notes retained; no auto-generated
  LICENSE because three student authors have not agreed to reuse terms.
- GitHub CI includes Python 3.13, Ruff, pip dependency consistency, existing
  safety and numerical test suites, Stage 4/5 Plotly/PDF/HTML regression tests
  and CodeQL. No extra runtime dependency is needed.

## Acceptance checks for the team

1. Open <https://sand-battery-project-a5twmepge6cqbndgbz9jmj.streamlit.app/>.
2. In **Visual Story Studio**, run 1-D thermal playback, inspect the animation
   frame labels and 2-D temperature map. Change the scenario and ensure old
   simulation results are hidden until recalculated.
3. On mobile, enable the **2D-only** option; verify tables and charts do not
   overflow uncontrollably.
4. View **Energy & sensitivities**; run ±10% sensitivity and inspect input
   parameters, color legend and numeric table.
5. View **Design tradeoffs**; run bounded candidates and export the CSV.
6. Open **Engineering report** and download HTML, PDF and scenario JSON.
   Check Group 8 names, current temperature and energy inputs, and the cited
   model limits. Print HTML → Save as PDF for the illustrated Unicode edition.
7. In **Research Hub**, verify the live bibliography, equation mapping and
   real field reference chart. Kankaanpää 100 vs 200 kW disagreement must be
   visible and attributed to different sources.
8. Test all other app pages and A/B/C JSON import/export for regressions.
9. Check GitHub README links and source links; open new architecture illustration.
10. Confirm CI and CodeQL success on the **merged main SHA**, not only the PR.
11. If deployment error occurs, check Streamlit Cloud logs/redeploy configuration;
    GitHub CI headless AppTest cannot guarantee actual browser behavior.

## Release exclusions

- No hardware prototype, recorded measurements, calibrated real thermocouple
  data, 2-D/3-D CFD, certified design, live sensor panel, automatic hardware
  watchdog or industrial safety approval.
- The analytic cp(T) representation does not include experimentally sourced
  phase-transition enthalpy near 573 °C.
- Original experimental literature is referenced but not mirrored or
  represented as input measurements.
- No third-party account or persistent cloud user database.
- No fictitious cost quotation, carbon-savings guarantee or mechanical stress
  safety rating.
- The PDF export uses a built-in font and may transliterate some non-ASCII
  characters; HTML retains Unicode and the inline chart.

## CI and audit links

- Baseline CI: https://github.com/bysquizy/Sand-Battery-Project/actions/runs/40387317283
- Current prioritized browser/device acceptance: [WEB_ACCEPTANCE.md](WEB_ACCEPTANCE.md)
- GitHub Actions: https://github.com/bysquizy/Sand-Battery-Project/actions
- CodeQL/security: https://github.com/bysquizy/Sand-Battery-Project/security/code-scanning

**Owner sign-off** on live website/browser checks remains a manual acceptance
step. Do not call this record experimental validation.

# Changelog

## v1.2.0 — 25 October 2026 (Research Hub and team information)

- Added the Group 8 contributor names: Yağız Topaç, Semih Cenk and Fatma Ovacık.
- Rebuilt the Research Hub as eight concise review-grounded topics, method/evidence maps, manufacturer vs operator system context and searchable APA sources.
- Removed duplicated academic identity, timeline and bibliography tabs from the Engineering Dashboard; kept it focused on numerical results.
- Reorganized sidebar navigation, added a prominent canonical GitHub link and published the Streamlit native-repository-link limitation.
- Condensed README and created `docs/RESEARCH_GUIDE.md` and pure `research_notes.py` scientific summaries.
- No new runtime libraries and no modifications to existing physical equations; model limitations remain explicit.


## v1.1.0 — 24 October 2026 (research and layout update)

- Added a pure-physics `design_lab` module implementing temperature-dependent passive cooling, module-count tradeoffs, simplified insulation shell volume, radial sidewall thermal profile, reverse MWh sizing and bounded geometry studies.
- Added English Thermal Design Studio with cooling/loss curves, schematic 3D module arrangement, radial heat map, sizing and CSV/JSON exports.
- Added full IZTECH ESE101 Group 8 Project & Research Library with original source audit terms, operator/manufacturer discrepancy, APA citations and governing equation context.
- Reorganized six Streamlit pages into simulation, advanced research and project/evidence groups.
- Audited user-provided 1,978-line legacy ZIP and explained what was independently implemented vs deferred.
- Expanded numerical and multipage Streamlit tests. No runtime packages or equipment-validation claims added.


## v1.0.0 Stable — 24 October 2026

- Consolidated the previously released engineering research prototypes into a stable software baseline for ESE101.
- Fixed a cloud startup failure by making optional `MODEL_EVIDENCE` import backward-compatible with older project metadata during rolling deploys.
- Added full Streamlit router-level navigation regression tests across all four pages.
- Standardized the public release name and citation to `v1.0.0` while preserving historical beta entries.
- No numerical physics formulas or five runtime dependencies were changed. Scientific assumptions and lack of field validation remain explicit.
- See `docs/RELEASE_NOTES_V1_STABLE.md` for test evidence and limitations.


## v2.2.0-beta — 24 October 2026

- Adopted a unified responsive UI theme inspired by the team-supplied Claude CSS proposal, preserving reduced-motion support and no external font requests.
- Grouped navigation, added onboarding, three presentation scenarios, low-power visualization mode and method/source traceability export.
- Added GitHub Dependabot, behavioral policy, issue and PR templates, CITATION metadata and development-only Ruff static checks.
- Kept five runtime dependencies and the existing engineering mathematics unchanged; added web interaction tests.
- See `docs/RELEASE_NOTES_V22.md` for limitations and postponed model changes.


## v2.1 — 24 October 2026 (web-first research release)

- Linked the owner-supplied public Streamlit site throughout GitHub docs and the multi-page interface.
- Replaced stale version labels, added light, bounded simulation caching and removed a third-party web-font dependency.
- Rebuilt material-ranking visualization as a lighter single Plotly chart and added temperature/capacity heatmap.
- Added safeguards for nonphysical temperature bounds and a clear quartz inversion warning.
- Distinguished Kankaanpää operator's **100 kW / 8 MWh** from the manufacturer's **200 kW / 8 MWh**, without claiming resolution.
- Removed unused `start.bat`; unchanged five direct Python runtime dependencies for the web platform.
- Expanded web/source regression tests and CI coverage for the full Streamlit project.
- Recorded the distinction between numerical code checks, literature-backed model assumptions and absent experimental validation.

## v2.0.0-beta — 24 October 2026 (research platform)

- Added a modular advanced research engine and optional multipage laboratory.
- Added sensible exergy, hourly renewable dispatch and conservation residual, ideal ε–NTU exchangers, Ergun fan pressure, LCOH cost scenarios and deterministic input Monte Carlo experiments.
- Added 1-D local thermal nonequilibrium (gas and solid) scenario solver with numerical energy balance verification.
- Added 13 additional assumption-labeled granular media (18 total); unknown medium suitability is explicitly disclosed.
- Added optional model-grid, pressure-velocity and standby/insulation virtual experiments.
- Expanded numerical and Streamlit multipage smoke test coverage; 42 tests passed on Python 3.13 in GitHub Actions.
- Reconciled presentation of conflicting 100/200 kW Kankaanpää operator/manufacturer descriptions as **unresolved and source-specific**, not hidden.
- Preserved existing base thermal model for backward compatibility; no field or material-specific calibration is claimed.
- Release scope and remaining limitations documented in `docs/RELEASE_NOTES_V2.md`.


## v1.0 — 24 October 2026 (academic web release)

- Added official IZTECH and Department of Energy Systems Engineering identification, ESE101 Group 8 and the @bysquizy maintainer credit.
- Added a linked Evidence Library with source categories, APA references and reference plant specifications.
- Corrected Kankaanpää to 200 kW / 8 MWh based on Polar Night Energy's official plant page.
- Added separate project/team page and tentative course milestones.
- Added scenario Markdown export and bibliography TXT export.
- Simplified web-first GitHub/Streamlit setup instructions.
- Retained existing numerical models. This is a research release, not experimental or structural validation.

## 1.0.0-alpha — 24 October 2026

- Built a separate English Streamlit application with custom responsive dark theme and lightweight animation.
- Separated thermal physics, materials, thermal-source power, 1-D thermocline and design screening.
- Added an auditable 0-D phase energy ledger and terminal-event numerical integration.
- Added interactive 3D Plotly cylinder with phase animation, Sankey energy graph, material plots and thermal timeline.
- Added optional 1-D simulations and capacity screening without automatically blocking the main page.
- Added 23 numerical/unit/visual-construction tests, GitHub Actions Python 3.13 CI and academic source and model notes.
- Original unlicensed upstream code deliberately excluded from this new public repository bundle.
- Streamlit full-runtime visual QA remains outstanding owing to unavailable package-index access in build environment.

## Repository maintenance — 24 October 2026

- Rewrote README with the correct GitHub repository and a one-click Windows 3.13 setup.
- Added `start.bat`, `.python-version`, `.gitignore` and the Streamlit theme configuration.
- Added `.github/workflows/quality.yml` for Python 3.13 automated tests.
- Added `.github/SECURITY.md` and `CONTRIBUTING.md`.
- Removed a redundant ZIP archive from the repository root; future distributable archives belong in GitHub Releases.
- Kept the existing numerical engine and Streamlit UI code unchanged in this maintenance update.

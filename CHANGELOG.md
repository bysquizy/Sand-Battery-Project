# Changelog

## v2.0.0-beta — 24 October 2026

- Added a modular advanced research engine and optional multipage laboratory.
- Added sensible exergy, hourly renewable dispatch and conservation residual, ideal ε–NTU exchangers, Ergun fan pressure, LCOH cost scenarios and deterministic input Monte Carlo experiments.
- Added 1-D local thermal nonequilibrium (gas and solid) scenario solver with numerical energy balance verification.
- Added 13 additional assumption-labeled granular media (18 total); unknown medium suitability is explicitly disclosed.
- Added optional model-grid, pressure-velocity and standby/insulation virtual experiments.
- Expanded numerical and Streamlit multipage smoke test coverage.
- Reconciled presentation of conflicting 100/200 kW Kankaanpää operator/manufacturer descriptions as **unresolved and source-specific**, not hidden.
- Preserved existing base thermal model for backward compatibility; no field or material-specific calibration is claimed.


## v1.0 — 24 October 2026 (academic web release)

- Added official IZTECH and Department of Energy Systems Engineering identification, ESE101 Group 8 and the @bysquizy maintainer credit.
- Added a linked Evidence Library with source categories, APA references and reference plant specifications.
- Corrected Kankaanpää to 200 kW / 8 MWh based on Polar Night Energy's official plant page.
- Added separate project/team page and tentative course milestones.
- Added scenario Markdown export and bibliography TXT export.
- Simplified web-first GitHub/Streamlit setup instructions.
- Retained existing numerical models. This is a research release, not experimental or structural validation.

# Changelog

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

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

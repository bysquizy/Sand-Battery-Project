# Sand Battery Studio

**ESE101 · Group 8 · Industrial-scale thermal energy storage research**  
**Version: 1.0 alpha · English user interface · Python 3.13**

A fast, physics-first Streamlit engineering dashboard. Includes an interactive heat-cycle timeline, animated 3D silo, Sankey-style energy ledger, source-transparent materials and geometry-constrained capacity screening. The code uses **no external AI API**, neural network runtime or large media assets.

> **Research prototype, not a certified engineering tool.** No measured field dataset is included, so numerical tests do not establish experimental accuracy. Results depend on assumed material properties, idealized output quality and boundary conditions.

## Getting started (Windows / Python 3.13.17)

The app supports Python 3.13; the developer test machine used Python 3.13.5 and the CI workflow targets Python 3.13. Patch-level 3.13.17 testing should be repeated on the user's PC.

```powershell
py -3.13 --version
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m streamlit run streamlit_app.py
```

If PowerShell blocks activation, use the venv executable directly:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run streamlit_app.py
```

In macOS/Linux use `python3.13 -m venv .venv`, `source .venv/bin/activate`, and the same pip and Streamlit commands.

## Interface

- **Overview:** stored energy, useful heat, thermal loss, energy conservation ledger and charging history.
- **Thermal Dynamics:** energy-balance model and an optional exploratory 1-D local-thermal-equilibrium temperature profile.
- **3D Plant Explorer:** animated, idealized thermal-state visualization with a phase slider. The colors are not CFD predictions.
- **Materials & Optimization:** assumption-labeled inputs, thermophysical comparison and bounded grid screening of candidate designs.
- **Methods & Evidence:** governing equations, source links, limitations and energy boundaries.

Change the inputs in the sidebar; charts and metrics respond automatically. Capacity screening and the heavier 1-D solver run only when requested.

## Lightweight dependencies

`streamlit`, `numpy`, `scipy`, `plotly`, `pandas`. Python's standard library covers the rest. There is no GPU dependency, Docker requirement, model-download step or AI inference engine.

## Development and testing

```powershell
python -m pip install -r requirements-dev.txt
python -m pytest -q
python -m compileall -q streamlit_app.py engine visuals.py
```

### Source provenance and scientific quality

The mathematical approach was reimplemented after inspecting the user-supplied `kum-bataryasi-proje-main.zip`, the newer v0.5 preview and the associated academic papers. The original Turkish 116 kB monolithic script was **not included** in this clean repository. That avoids unnecessary bloat and avoids republishing unverified upstream licensing terms. Consult the original ZIP separately for feature migration and regression checking.

Read [`docs/MODEL_VALIDATION.md`](docs/MODEL_VALIDATION.md), [`docs/SOURCE_REGISTER.md`](docs/SOURCE_REGISTER.md) and [`docs/ROADMAP.md`](docs/ROADMAP.md) before citing any output as a design result.

## Create an entirely new public GitHub repository

The target repository does not exist until its owner creates it. Recommended name: `sand-battery-studio`.

1. Open [github.com/new](https://github.com/new) while logged into your GitHub account. Set owner to `bysquizy`, name to `sand-battery-studio`, visibility to **Public**. Do **not** initialize with a README, `.gitignore` or license, since this project already has a README and `.gitignore`.
2. From this folder in a terminal, run:

```powershell
git init -b main
git add .
git commit -m "Initial English physics-first Sand Battery Studio"
git remote add origin https://github.com/bysquizy/sand-battery-studio.git
git push -u origin main
```

If your remote requires login, use the Git credential manager/browser login rather than placing any token in the source code.

3. Configure GitHub Pages? **No:** this is a Python Streamlit application, not a static site. At [share.streamlit.io](https://share.streamlit.io), create an app from this GitHub repository, choose `main`, entrypoint `streamlit_app.py`, and in Advanced Settings select **Python 3.13**.

## Project integrity

A team member reported explicit **verbal instructor authorization** for AI-assisted programming. The course information sheet generally limits AI to idea generation; confirm the verbal exception's scope and disclose all approved AI-assisted work according to course requirements. Keep final academic reasoning, review, calculations and citations under the team's control.

## License

No software license is claimed for the original third-party repository. A license for this new original code should be agreed by the student team before public reuse is invited.

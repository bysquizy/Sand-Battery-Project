# Sand Battery Project

**Sand Battery Studio** · English-language engineering simulator · **ESE101 / Group 8**  
**Python 3.13 · Streamlit · Research preview (v1.0 alpha)**

A lightweight, physics-first workspace for studying industrial-scale sensible thermal energy storage. Explore charging and discharging, material assumptions, idealized temperature gradients, energy accounting, interactive charts, animated 3D silo and geometry-constrained capacity screening.

> **Research prototype, not a certified engineering tool.** No measured field data are included, so numerical tests do not establish experimental accuracy. **Electricity-to-useful-heat efficiency is not electricity-to-electricity round-trip efficiency.** Material data and operating boundaries are illustrative.

## Quick start — Windows (Python 3.13)

1. Download this repository using **Code → Download ZIP** and **extract** the folder.
2. Double-click **`start.bat`**. The first launch creates a local Python environment and installs dependencies automatically.
3. Open the local address in the terminal, usually <http://localhost:8501>.

Python **3.13.17** is the intended Windows version. The numerical tests were previously exercised with Python 3.13.5; full Streamlit browser testing on 3.13.17 is still required.

### Manual start — Windows PowerShell

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run streamlit_app.py
```

### macOS / Linux

```bash
python3.13 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m streamlit run streamlit_app.py
```

## Features

| Workspace | Description |
| --- | --- |
| **Overview** | Stored energy, deliverable thermal energy, heat losses and cycle energy balance. |
| **Thermal Dynamics** | 0-D energy-balance calculations and optional exploratory 1-D LTE model. |
| **3D Plant Explorer** | Animated, idealized silo and thermal-state presentation; **not** a CFD prediction. |
| **Materials & Optimization** | Assumption-labeled media, idealized blends and bounded design screening. |
| **Methods & Evidence** | Model equations, scientific limitations and references. |

Charging input scenarios cover electric resistance heating, constant-irradiance CSP (Fresnel/heliostat), and average-power PV and wind. They are **not live weather forecasts**.

## Technical structure

- `streamlit_app.py` — English interface and main entry point
- `engine/` — thermophysical materials, 0-D and 1-D models, renewable scenarios and optimization
- `visuals.py` — plots, 3D silo and energy-flow diagrams
- `tests/` — numerical and visualization construction tests
- `docs/` — source register, limitations and roadmap
- `.github/workflows/quality.yml` — automatic Python 3.13 tests

To run the tests:

```powershell
py -3.13 -m pip install -r requirements-dev.txt
py -3.13 -m pytest -q
```

Read the [model-validation notes](docs/MODEL_VALIDATION.md), [source register](docs/SOURCE_REGISTER.md), and [roadmap](docs/ROADMAP.md) before reporting simulated values as engineering findings. Numerical consistency tests **do not** establish full experimental validation.

## Online deployment

Use [Streamlit Community Cloud](https://share.streamlit.io/) with:

- **Repository:** `bysquizy/Sand-Battery-Project`
- **Branch:** `main`
- **Main file path:** `streamlit_app.py`
- **Python version:** `3.13`

This app cannot be hosted as a static GitHub Pages site. A public GitHub repository is not itself a deployed live application.

## Research provenance and integrity

Developed for a three-person ESE101 Group 8 project. A team member reports verbal instructor permission for AI-assisted coding; the course's written AI policy is more restrictive, so scope and disclosure should be confirmed before academic submission. The team remains responsible for reviewing the mathematics, documentation and results.

The current solver was reimplemented after reviewing an earlier project archive and academic references. The older unlicensed monolithic project was not copied into this repository. Relevant literature is catalogued in [SOURCE_REGISTER.md](docs/SOURCE_REGISTER.md).

## Security, contributions and license

Please read the [security policy](.github/SECURITY.md) and [contribution guide](CONTRIBUTING.md). There is no general open-source reuse license at this stage; the three-person team should agree on licensing before inviting redistribution.

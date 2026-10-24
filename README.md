# Sand Battery Project — Sand Battery Studio v2.0 Beta

**İzmir Institute of Technology (IZTECH) · Department of Energy Systems Engineering**  
**ESE 101 · Group 8 (three students) · Fall 2026/27 · Maintainer: Yağız Topaç ([@bysquizy](https://github.com/bysquizy))**

A lightweight English-language **browser-based v2 research platform** for thermal-energy-storage simulation. Explore industrial-scale sensible-heat storage, transient losses and heat delivery, 0-D and exploratory 1-D simulations, interactive 3D silo visualization, idealized material comparisons, capacity screening and scientific evidence.

> **Academic research release, not experimentally validated.** This repository is an independent student project, not an official IZTECH website or an engineering design certification. Input material properties are illustrative. Electricity-to-useful-heat is not electricity-to-electricity round-trip efficiency.

## Open as a website — preferred

The team reports that this project is already hosted on Streamlit Community Cloud. The public application's **exact** address has not been supplied, so it is not linked here yet. Once confirmed, add the Streamlit URL to this README and to GitHub **About → Website**. Do not guess a deployed URL.

If deployment must be configured or refreshed, use [Streamlit Community Cloud](https://share.streamlit.io/) with:

| Setting | Value |
| --- | --- |
| Repository | `bysquizy/Sand-Battery-Project` |
| Branch | `main` |
| Main file | `streamlit_app.py` |
| Python | **3.13** (select in Advanced settings) |

Select **Deploy** or **Reboot** as appropriate. Verify that the hosted app is pulling the latest `main` commit. A GitHub repository link is **not** itself the web application. Streamlit hosts the Python calculation engine and browser interface; GitHub Pages alone cannot run this backend.

## Windows installation (Python 3.13.17)

Download the repository ZIP, extract the folder and double-click **`start.bat`**. First run installs dependencies. Manual alternative:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run streamlit_app.py
```

## Navigation

**New v2 pages** are available through Streamlit's built-in navigation:

- **Engineering Research Lab:** exergy, hypothetical hourly renewable dispatch with optional CSV inputs, direct-contact LTNE solver, Ergun flow loss, ε–NTU heat exchanger, uncertainty distributions and scenario LCOH.
- **Material Atlas:** 18 material scenarios, including **13 additional illustration-only media** with source/provenance flags, cp(T) curves and ideal mixtures.
- **Virtual Experiments:** pressure drop, grid sensitivity and insulation–standby heat loss.

The original interface remains available:

- **Dashboard** (`home_app.py`, routed by `streamlit_app.py`): stored thermal energy, delivered heat, energy balance and interactive Sankey.
- **Thermal Dynamics:** transient charge/hold/discharge and optional 1-D LTE research surrogate.
- **3D Plant Explorer:** animated idealized silo—not CFD or a construction drawing.
- **Materials & Optimization:** illustrative solid-media properties and bounded design screening.
- **Evidence Library:** manufacturer reference plants, methods, APA-style citations and original links.
- **Project & Team:** IZTECH affiliation, Group 8 credit, milestones and academic-integrity notice.

Export the simulation as JSON, an engineering summary as Markdown or the bibliography as TXT.

## Technical validity

Theoretical storage capacity differs from **usable thermal delivery**. The 0-D model approximates mean temperature, heat losses and fixed-output operation; the 1-D finite-volume LTE model is a **different, direct-contact topology**, not a calibrated commercial pipe-in-sand exchanger. CSP irradiance and PV/wind capacity factors are scenario inputs, not hourly weather or guaranteed electricity generation. No validated construction, capital-cost or electricity-reconversion claim is made.

For governing equations, explicit scope limits and source conflicts, see [Advanced Research v2](docs/ADVANCED_RESEARCH_V2.md). For the original thermal core see [Source Register](docs/SOURCE_REGISTER.md), [Model Validation](docs/MODEL_VALIDATION.md), [Roadmap](docs/ROADMAP.md), and [Changelog](CHANGELOG.md). Primary sources include [Bošnjaković & Santa (2026)](https://doi.org/10.3390/cleantechnol8050165), [Polar Night Energy — Kankaanpää (200 kW, 8 MWh)](https://polarnightenergy.com/reference/worlds-first-sand-battery/), [Pornainen (1 MW, 100 MWh)](https://polarnightenergy.com/reference/solution-for-clean-energys-big-problem/), and [NREL (2024)](https://www.nrel.gov/news/features/2024/solution-to-energy-storage-may-be-beneath-your-feet.html). The app includes an expanded bibliography and claim boundaries.

## Quality checks (Python 3.13)

```powershell
py -3.13 -m pip install -r requirements-dev.txt
py -3.13 -m pytest -q
py -3.13 -m compileall -q streamlit_app.py project_info.py visuals.py engine
```

The v2 GitHub Actions pipeline passed **42 automated tests** on Python 3.13, including Streamlit page smoke tests. Tests verify code execution and numerical consistency, not physical experimental accuracy. GitHub Actions runs on pushes and pull requests.

## Team and disclosure

The project team contains three ESE101 Group 8 students. Lead developer: **Yağız Topaç** ([@bysquizy](https://github.com/bysquizy)). Other contributor names will be added when explicitly provided. The team reports verbal faculty approval for AI-assisted coding; the general written course handout restricts AI to brainstorming. Confirm the exception's scope and disclose authorized use in any assessed submission. No general open-source license is currently granted. See [Security Policy](.github/SECURITY.md) and [Contributing](CONTRIBUTING.md).

## Release status

**v2.0 Beta**: feature-complete for the current research demonstrations, with source-aware warnings and CI checks. Not production- or experiment-certified; user-side visual QA and independent field data validation remain open. See [Release Notes](docs/RELEASE_NOTES_V2.md) and [Roadmap](docs/ROADMAP.md).

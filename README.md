# Sand Battery Project — Sand Battery Studio v1.1 Research Update

**İzmir Institute of Technology (IZTECH)** · Department of Energy Systems Engineering · **ESE101 / Group 8** · Fall 2026/27  
Project developer: **Yağız Topaç** ([@bysquizy](https://github.com/bysquizy)) · Team of three

[**Open the live web application ↗**](https://sand-battery-project-a5twmepge6cqbndgbz9jmj.streamlit.app/) · [Browse source](https://github.com/bysquizy/Sand-Battery-Project) · [Evidence and formulas](docs/ADVANCED_RESEARCH_V2.md)

A **browser-first** Python/Streamlit engineering research platform for industrial sensible-heat storage. **No installation is required to use the live app.** The repository contains the numerical models and reproducible tests.

> **Research demonstration, not a field-validated engineering design.** Results are derived from simplified physics and illustrative material properties. The 1-D direct-contact LTE/LTNE research models are not calibrated representations of commercial closed-pipe sand batteries. Sensible heat, usable thermal heat and thermodynamic exergy are different quantities.

## v1.0 stable research features

- **Shared visual language:** responsive copper/teal engineering theme adapted from a team-submitted UI proposal; no third-party font downloads; reduced-motion and keyboard-focus support.
- **Guided navigation:** grouped Simulation, Research & Comparison, and Model Verification workspaces plus a quick-start guide.
- **Faculty demo presets:** three illustrative one-click input configurations; explicitly **not** measured commercial-plant profiles.
- **Light mode:** skip expensive 3D figures when using a mobile device or slower connection.
- **Traceable equations:** a downloadable table maps each implemented model to its governing equation, relevant reference, assumption boundary and verification status.
- **Repository hygiene:** scoped Ruff checks, Dependabot, issue/PR templates, contributor conduct policy and formal software citation.
- The existing 0-D, 1-D, LTNE and related numerical research models are preserved. **Software stability is not experimental validation.** Do not infer new experimental accuracy from a new visual theme.

## v1.1 — Thermal Design Studio and source-linked academic portal

This update is grounded in the **user-supplied legacy sand-battery ZIP**, the team-provided Polar Night Energy research DOCX, the complete Bošnjaković & Santa (2026) review and the enhanced source verification audit. The old public website was **not directly browser-renderable** by the inspection tool; its uploaded source code was reviewed instead. See the [source-to-feature mapping](docs/LEGACY_METHODS_PORTING.md).

Two additional pages are included without new Python runtime packages:

- **Thermal Design Studio:** temperature-dependent passive cooling, cumulative ambient loss, module-count tradeoffs, interactive schematic 3D modular layouts, radial insulation temperatures, time–radius heatmap, theoretical target-MWh volume sizing, constrained silo dimensions, and CSV/JSON scenario exports.
- **Project & Research Library:** dedicated IZTECH Energy Systems Engineering / ESE101 Group 8 identity; course timeline and contributor credits; governing equations with explicit applicability; manufacturer vs operator specifications; NREL material data caveats; reference categories, source audit principles and downloadable APA-style bibliography.

The new computations are numerical scenarios: no physical prototype, temperature sensor data, certified design, verified field efficiency or experimental material fitting is implied.

## What's inside

| Web workspace | Calculations and visuals |
| --- | --- |
| **Dashboard** | Interactive 0-D charging/standby/discharge, energy ledger, Plotly timeline, thermal metrics, animated 3D silo and bounded geometry screening |
| **Engineering Research Lab** | Exergy, hourly synthetic PV/wind heat dispatch with optional CSV, two-temperature LTNE, ε–NTU exchanger, Ergun flow loss, hypothetical Monte Carlo inputs and LCOH |
| **Material Atlas** | 18 comparison scenarios, provenance labels, cp(T) curves, capacity charts, temperature-sweep heatmap and ideal two-material blending |
| **Virtual Experiments** | Velocity-pressure comparison, axial mesh sensitivity, insulation and standby heat-loss screening |
| **Thermal Design Studio** | 0-D passive cooling, radial wall heat profile, module layouts, energy-target sizing, dimension screening and explanatory Plotly visuals |\n| **Project & Research Library** | Student/team profile, source evidence classifications, governing equations, published field references and APA bibliography |\n| **Evidence Library** | APA references, manufacturer/utility claims, model equations, assumptions and uncertainty boundaries |
| **Project & Team** | IZTECH, department, ESE101 Group 8 and named lead-developer credit |

**No external AI service, GPU, large ML model, paid weather API or browser plug-in.** The five direct Python dependencies are Streamlit, NumPy, SciPy, Pandas and Plotly. They support the current UI, solvers, tabular data and figures. Test-only Pytest lives in `requirements-dev.txt` and is not required by the hosted app.

## Use on the web

Open **https://sand-battery-project-a5twmepge6cqbndgbz9jmj.streamlit.app/**. From the left-hand navigation, choose the desired engineering workspace. Parameter changes update the calculations; heavier numerical experiments run only when requested. Outputs can be exported as JSON, Markdown or CSV where available.

The website is configured from **GitHub `main` → `streamlit_app.py`**. Streamlit Community Cloud automatically deploys updates from the repository. No local installation or separate backend server is necessary for visitors. If a new version seems stale, reload the browser or use **Manage app → Reboot app** as its owner.

## Engineering evidence: what is and isn't confirmed

- **Kankaanpää, 2022:** utility operator Vatajankoski describes **100 kW thermal** / **8 MWh**, while system developer Polar Night Energy describes **200 kW thermal** / **8 MWh**. These are **source-attributed inconsistent power figures**, potentially reflecting different definitions; neither is a calibration measurement for this simulator. [Operator](https://www.vatajankoski.fi/en/projects/sand-battery/) · [Developer](https://polarnightenergy.com/reference/worlds-first-sand-battery/).
- **Pornainen, 2025:** Polar Night Energy's published description states **1 MW thermal** / **100 MWh**. [Manufacturer report](https://polarnightenergy.com/news/worlds-largest-sand-battery-now-in-operation/).
- **NREL specific silica-sand sample:** report 84728 gives **1,543 kg/m³ bulk density**, describes measured cp(T) and the quartz transition around **573 °C**. Our *illustrative linear cp(T)* is **not** that experimental curve. [NREL report 84728](https://www.nrel.gov/docs/fy23osti/84728.pdf).
- **Thermal-model literature:** [Bošnjaković & Santa (2026)](https://doi.org/10.3390/cleantechnol8050165) surveys technical systems and research gaps; [Liu et al. (2024)](https://doi.org/10.1016/j.est.2023.109957) concerns experimentally studied packed-bed LTNE physics with a different apparatus. Neither independently certifies this app's chosen parameters.

Details: [Source register](docs/SOURCE_REGISTER.md) · [Advanced equations and limits](docs/ADVANCED_RESEARCH_V2.md) · [Model verification](docs/MODEL_VALIDATION.md) · [Roadmap](docs/ROADMAP.md).

## Developers and academic integrity

The source runs on Python **3.13**. GitHub Actions automatically installs the five runtime dependencies plus Pytest and runs syntax, numerical and Streamlit page-startup checks. To repeat locally *only if you're developing the source*, install `requirements-dev.txt` and run `python -m pytest -q`.

The team reports verbal instructor permission for AI-assisted coding, although the general ESE101 information sheet restricts AI to brainstorming. The team must confirm and disclose the authorized exception for assessed submissions. This is an **independent student project**; it does not claim official university endorsement, experimental performance certification, validated construction safety or third-party intellectual property rights. No general source reuse license has yet been granted.

See [Security policy](.github/SECURITY.md), [Contributing](CONTRIBUTING.md), [Code of Conduct](CODE_OF_CONDUCT.md), [software citation](CITATION.cff), [Changelog](CHANGELOG.md) and [v1.0 stable release notes](docs/RELEASE_NOTES_V1_STABLE.md). MIT/GPL licensing is **not** asserted without agreement of all student contributors.

### Interpretation of the supplied older project

The older project archive contains additional engineering explorations; not all original features can be safely copied or assumed scientifically equivalent. The new capabilities are independently implemented with current model definitions. See [Legacy source mapping](docs/LEGACY_METHODS_PORTING.md) for a precise delivered/deferred comparison.

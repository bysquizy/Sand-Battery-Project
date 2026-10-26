# Sand Battery Studio

A browser-based engineering project for exploring **sensible thermal energy storage** using sand and other granular materials. The application models charging, heat retention, thermal discharge and design trade-offs through transparent numerical assumptions.

**[Open the simulation](https://sand-battery-project-a5twmepge6cqbndgbz9jmj.streamlit.app/)** · **[Research methods](docs/EQUATION_TRACEABILITY.md)** · **[Model limitations](docs/MODEL_VALIDATION.md)**

**Group 8:** Yağız Topaç · Semih Cenk · Fatma Ovacık

![Sand Battery Studio simulation workflow](assets/architecture.svg)

## About the project

Sand Battery Studio is a software-only thermal storage study. It helps users investigate how storage volume, material properties, operating temperatures, insulation and heat transfer affect modeled thermal performance. All calculations run in a browser-based Streamlit application; no hardware or local installation is required to use the website.

The project uses numerical models of different complexity. They provide ways to explore engineering behavior, not direct predictions of commercial equipment.

## Application

| Page | Main functions |
| --- | --- |
| Engineering Dashboard | Charging, holding and discharging cycles; energy and heat-loss summaries |
| Thermal Design Studio | Insulation, geometry and thermal capacity screening |
| Scenario Manager | Save and compare three designs; JSON/CSV exchange |
| Model Verification | Compare 0-D and 1-D assumptions, energy balances and simplified closed-pipe transfer |
| Visual Story Studio | Computed axial thermal animation, heatmaps, design comparisons and HTML/PDF reports |
| Advanced Research Lab | Exergy, renewable dispatch, thermal flow, uncertainty and cost assumptions |
| Material Atlas | Compare granular storage materials and temperature-dependent heat capacities |
| Virtual Experiments | Mesh sensitivity, flow and thermal-loss investigations |
| Research Hub | Literature summaries, field references, equations and source attribution |

The same **Active Scenario** provides core design parameters across the application. Some research tools intentionally allow local exploratory variations without changing the saved design.

## Scientific basis and limitations

Thermal energy is calculated from material mass and temperature-dependent specific heat. Transient energy balances include charging, thermal output and modeled losses. The 1-D thermocline and simplified embedded-pipe approaches represent **different physical configurations**; their outputs are not interchangeable.

**This is an educational simulation, not an experimentally validated sand battery.** Material properties and economic inputs may be illustrative. Charts and animated temperatures are computed visualizations, not measurements, and no real prototype, sensor data or industrial certification is claimed.

Source details and limitations are documented in:

- [Equation and source traceability](docs/EQUATION_TRACEABILITY.md)
- [Research guide](docs/RESEARCH_GUIDE.md)
- [Source register](docs/SOURCE_REGISTER.md)
- [Model verification and limitations](docs/MODEL_VALIDATION.md)

Reference installations mentioned in the Research Hub are attributed to their publishers. In particular, the **Kankaanpää** thermal-power figures reported by Polar Night Energy (200 kW) and Vatajankoski (100 kW) differ; this unresolved discrepancy is not used to calibrate the simulation.

## Running locally

Python 3.13 is recommended.

```bash
python -m pip install -r requirements.txt
streamlit run streamlit_app.py
```

The runtime uses **Streamlit, NumPy, SciPy, Plotly and Pandas**.

To run the software tests:

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

## Project structure

- `streamlit_app.py` — multipage navigation
- `home_app.py` and `pages/` — application workspaces
- `engine/` — physical models and input validation
- `scenario_state.py` — active design state
- `visuals.py` and `visuals_advanced.py` — numerical visualization
- `project_info.py` and `research_notes.py` — project metadata and research context
- `docs/` — scientific methods, source registers, verification and historical records
- `tests/` — automated software regression tests

See [Contributing](CONTRIBUTING.md), [Security](.github/SECURITY.md), [Changelog](CHANGELOG.md) and [Citation](CITATION.cff) for repository details.

**Reuse:** No general open-source license has been selected by the three contributors.

# Sand Battery Project

**Sand-based thermal energy storage — numerical simulation and research project**

**Group 8:** Yağız Topaç · Semih Cenk · Fatma Ovacık

[Run the simulation](https://sand-battery-project-a5twmepge6cqbndgbz9jmj.streamlit.app/) · [Source code](https://github.com/bysquizy/Sand-Battery-Project)

## Project overview

This is a student engineering project investigating how sand and other granular materials can store energy as heat. The Streamlit application explores charging, heat retention, thermal discharge, insulation, storage geometry and material-property assumptions through numerical models.

The project is **software-only**. Results are simulations, not measured performance from a physical prototype or commercial battery. Energy capacity is reported as **thermal energy** (MWh), not electricity generated.

## What the application does

- **Engineering Dashboard:** explores charging, stored heat, useful thermal output and heat losses.
- **Thermal Design Studio:** compares insulation and tank-design choices.
- **Scenario Manager:** saves and compares design configurations.
- **Model Verification:** inspects calculation and energy-balance assumptions.
- **Visual Story Studio:** visualizes modeled temperatures and exports reports.
- **Advanced Research Lab, Material Atlas and Virtual Experiments:** explores materials, sensitivities and additional simplified engineering models.
- **Research Hub:** documents the project background, sources and limitations.

All pages use a shared active scenario. Adjustable waiting periods, including a two-day example value, are **simulation inputs**, not project deadlines.

## How it works

Electrical or solar energy is represented as thermal input. A model estimates sensible heat stored in a granular medium and tracks heat losses during storage and discharge. The idealized energy relationship is:

```text
Q = m × cp × ΔT
```

Actual predictions depend on the chosen heat capacity, temperature range, geometry, insulation, power inputs and model assumptions. The application includes simplified 0-D and 1-D approaches, which do not describe identical physics.

## Installation

Python 3.13 is recommended.

```bash
python -m pip install -r requirements.txt
streamlit run streamlit_app.py
```

Tests:

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

## Sources and limitations

The project documentation records equations, citations, evidence quality and model limitations:

- [Equations and assumptions](docs/EQUATION_TRACEABILITY.md)
- [Research guide](docs/RESEARCH_GUIDE.md)
- [Source register](docs/SOURCE_REGISTER.md)
- [Model verification](docs/MODEL_VALIDATION.md)

Reference systems described in the research are **not** calibration or validation data for this simulator. Commercial performance, electricity-to-electricity efficiency and planned emissions reductions must not be confused with the results of this educational model.

## Repository structure

- `streamlit_app.py`, `home_app.py`, `pages/`: application screens.
- `engine/`: numerical models and input validation.
- `scenario_state.py`: shared scenario state.
- `project_info.py`, `research_notes.py`: project information and references.
- `docs/`: methodology and documentation.
- `tests/`: automated regression tests.

**License:** No general open-source license has been selected by the contributors.

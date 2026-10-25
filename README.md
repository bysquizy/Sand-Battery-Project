# Sand Battery Studio — v1.2 Research Hub

[**Open the live web application**](https://sand-battery-project-a5twmepge6cqbndgbz9jmj.streamlit.app/) · [**GitHub repository**](https://github.com/bysquizy/Sand-Battery-Project) · [**Scientific methods**](docs/ADVANCED_RESEARCH_V2.md)

A lightweight, English-language, browser-based engineering simulation of **sensible thermal energy storage**. Visitors need no local installation. The five Python runtime dependencies remain Streamlit, NumPy, SciPy, Pandas and Plotly.

**Group 8:** Yağız Topaç · Semih Cenk · Fatma Ovacık.

> **Software research tool, not an experimentally validated industrial sand battery.** All energy, economic and material scenario results must be interpreted within their stated assumptions. A validated energy balance does not certify actual operating performance.

## Explore the site

| Workspace | What you can explore |
| --- | --- |
| **Engineering Dashboard** | 0-D charge/hold/discharge, useful heat, energy losses, Sankey balance, annotated temperature timelines, illustrative animated 3D silo and bounded material screening |
| **Thermal Design Studio** | Passive cooling, modular geometry, radial insulation temperature, geometric limits, target theoretical MWh volume sizing and scenario exports |
| **Advanced Research Lab** | Exergy, synthetic PV/wind dispatch, direct-contact LTNE, Ergun pressure loss, ideal ε–NTU exchanger, illustrative uncertainty and LCOH |
| **Material Atlas** | 18 sourced-or-assumption-labeled materials, cp(T) curves, temperature/capacity comparison, theoretical ideal mixtures |
| **Virtual Experiments** | Mesh-sensitivity comparison, air-flow/pressure resistance and insulation/standby case studies |
| **Research Hub** | Eight concise technical summaries, operating modes, equations, model boundaries, Finnish reference systems, the source-audit method, APA bibliography and a minimal Group 8 member section |

The **Research Hub is the single primary place for references and team information**. Duplicate academic project tabs were removed from the Dashboard to improve navigation. All three contributors are credited by the names supplied to the project.

### GitHub icon in Streamlit's upper toolbar

The built-in GitHub icon belongs to Streamlit Community Cloud and may use the repository connected to the deployment. Its destination **cannot be redirected by a Streamlit Python link**. To ensure a visible working link, the application includes an explicit **GitHub Repository** button pointing to [this repository](https://github.com/bysquizy/Sand-Battery-Project). If Streamlit's native GitHub button points elsewhere, the app owner must correct the connected GitHub deployment source in Streamlit Community Cloud.

## Research foundation

The primary literature review is **Bošnjaković and Santa (2026)**, [*Sand Batteries for Thermal Energy Storage: A Review of Operating Principles, Technologies, Challenges and Future Perspectives*](https://doi.org/10.3390/cleantechnol8050165), *Clean Technologies, 8*(5), 165. Its main themes are charging/storage/discharging, fixed and thermocline beds, fluidized/moving beds, hybrid materials, modelling and AI, environmental/economic tradeoffs, safety, reliability and commercialization limitations. The project has **not** reproduced that copyrighted article; concise study notes in `research_notes.py` and `docs/RESEARCH_GUIDE.md` are derived interpretations with section references.

The submitted team sources include the *Polar Night Energy research summary* (manufacturer-sourced context), the *Enhanced Source Check Research Audit* (source reliability grades P1, P2, S1, S2, U and claim verdicts) and the original legacy Streamlit ZIP (calculation ideas, not field observations). Commercial claims are attributed rather than treated as calibration data.

- **Kankaanpää, Finland:** the Vatajankoski operator [reports 100 kW](https://www.vatajankoski.fi/en/projects/sand-battery/), while the Polar Night Energy developer [lists 200 kW](https://polarnightenergy.com/reference/worlds-first-sand-battery/); both mention 8 MWh. The discrepancy remains unresolved.
- **Pornainen, Finland:** [Polar Night Energy reports 1 MW and 100 MWh](https://polarnightenergy.com/reference/solution-for-clean-energys-big-problem/), with crushed soapstone.
- **NREL's particle storage work:** [report 84728](https://www.nrel.gov/docs/fy23osti/84728.pdf) discusses a specific high-purity silica sample. Our illustrative linear cp(T) is **not** the measured phase-transition curve around 573 °C.

[**Research summaries**](docs/RESEARCH_GUIDE.md) · [Equation and evidence mapping](docs/ADVANCED_RESEARCH_V2.md) · [Source register](docs/SOURCE_REGISTER.md) · [Legacy feature migration](docs/LEGACY_METHODS_PORTING.md) · [Limitations](docs/MODEL_VALIDATION.md)

## Calculation boundaries and reproducibility

- **Stored energy:** \(Q=m\int c_p(T)dT\), based on specified bulk material density and assumed property curves.
- **0-D thermal losses:** \(Q_{loss}=UA(T-T_{ambient})\), approximate cylindrical insulation geometry.
- **1-D LTE/LTNE:** direct-contact bed equations; **not** the same as the commercial embedded-pipe technology.
- **Exergy:** a thermodynamic upper bound, not electricity generated.
- **Costs:** hypothetical scenario inputs, not verified installed quotes.
- **Animated temperatures:** numerical illustration, not measured thermocouple points or CFD.

Python 3.13 GitHub Actions checks numerical results, imports, page navigation and static analysis. Runtime dependencies are in `requirements.txt`; test-only tools are in `requirements-dev.txt`. Tests do **not** substitute for measurements. Team members should disclose permitted AI assistance according to their actual course/institution rules.

There is **no general open-source license** pending contributor agreement. See [security](.github/SECURITY.md), [contributing](CONTRIBUTING.md), [changelog](CHANGELOG.md) and [software citation](CITATION.cff).

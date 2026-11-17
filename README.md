# Sand Battery Project

**Sand-based thermal energy storage — web simulation and engineering research**

[Open the web application](https://sand-battery-project-a5twmepge6cqbndgbz9jmj.streamlit.app/) · [Research and model assumptions](docs/EQUATION_TRACEABILITY.md)

**Group 8:** Yağız Topaç · Semih Cenk · Fatma Ovacık  
**Web application:** Yağız Topaç ([@bysquizy](https://github.com/bysquizy))

## Project overview

This student project investigates the storage of thermal energy in sand and other granular media. Its Python/Streamlit web application simulates charging, sensible-heat retention, standby heat loss, thermal discharge, material selection, insulation and tank geometry.

It is a **numerical research tool, not a physical prototype or a commercial battery**. Results are illustrative model calculations, not measured plant performance. Reported MWh values represent **thermal energy**, not electricity generated.

## Explore the application

| Page | What you can do |
| --- | --- |
| Engineering Dashboard | Review energy capacity, heat losses, temperatures, energy accounting and an interactive silo view |
| How It Works / Nasıl Çalışır? | Learn the three operating stages and try a material-dependent energy calculation |
| Thermal Design Studio | Compare insulation, geometry, storage volume and passive cooling |
| Scenario Manager | Save A/B/C designs, compare calculated results and export/import versioned JSON |
| Model Verification | Inspect equations, model boundaries, energy conservation and numerical comparisons |
| Visual Story Studio | Play computed 1-D temperature profiles, explore sensitivity and export reports |
| Research Lab, Material Atlas, Virtual Experiments | Study additional simplified physical models and material assumptions |
| Research Hub | Read scientific explanations, source attributions and limitations |

## Getting started / İlk kullanım

1. **Open the web application.** No desktop download or local Python installation is required.
2. **Choose English or Türkçe** from the sidebar.
3. Open **Edit shared design / Ortak tasarımı düzenle**, change the inputs and select **Apply to all pages / Tüm sayfalara uygula**. Unsaved form changes do not affect calculations.
4. Review the Dashboard; run optional higher-cost simulations only when needed. In Scenario Manager, compare designs or download a JSON backup.

**Important:** A/B/C saved designs exist only in the current session. Refreshing, disconnecting or starting a new browser session can lose them. Download **active + A/B/C scenario JSON** to preserve them. Importing a bundle replaces the active design and the saved slots; make a backup first. Numerical-results JSON is a report, **not** a restorable scenario file.

For phones, Dashboard **Light mode** avoids its 3-D renderer. Visual Story Studio also offers a separate 2-D mode.

## Mathematical basis and limitations

Theoretical sensible heat between two temperatures is

\[
Q=m\int_{T_{\min}}^{T_{\max}}c_p(T)\,\mathrm{d}T.
\]

The 0-D simulation estimates heat input, heat losses and useful thermal output from a lumped temperature. Separate 1-D direct-contact models illustrate axial heat transfer; these do **not** represent a validated commercial closed-pipe sand battery. Temperature-dependent material properties and the ~573 °C quartz transition require independent experimental characterization.

Numerical energy-balance checks establish internal consistency, **not physical validation**. The current project does not claim calibrated sensor data, structural certification, electrical round-trip efficiency or verified plant emissions reductions.

The published Kankaanpää heating-power figures differ between the [operator](https://www.vatajankoski.fi/en/projects/sand-battery/) and [technology developer](https://polarnightenergy.com/reference/worlds-first-sand-battery/). They are preserved with attribution, not averaged.

## Sources and project files

- [Equation-to-code and evidence map](docs/EQUATION_TRACEABILITY.md)
- [Scientific source register](docs/SOURCE_REGISTER.md)
- [Research guide](docs/RESEARCH_GUIDE.md)
- [Model verification and limitations](docs/MODEL_VALIDATION.md)
- [Browser/mobile acceptance checklist](docs/WEB_ACCEPTANCE.md)

Source layout: `engine/` contains the numerical models, `pages/` and `streamlit_app.py` contain the web interface, `scenario_state.py` manages the active design, `ui_theme.py` styles the interface and `tests/` contains automated verification.

GitHub Actions runs Python compilation, linting, dependency checks and numerical/UI regression tests. Those checks do not replace independent physical-model validation or real-device browser testing.

**License:** The student team has not selected a general open-source license.

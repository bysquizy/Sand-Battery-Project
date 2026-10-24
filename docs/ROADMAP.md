# Phased Development Roadmap

| Phase | Scope | Gate |
|---|---|---|
| Alpha 1 (this ZIP) | New modular source, English responsive Streamlit, animated charts, conservation ledger, source labels | Numerical tests pass; UI requires user-side smoke test |
| Alpha 2 | End-to-end Python 3.13.17 verification, GitHub Actions, issue triage and screenshots | All app navigation and download paths pass; PR review |
| Beta 1 | Measured/sourced material-property catalogue and uncertainty bounds | Per-material temperature range and traceable primary source |
| Beta 2 | Improved 1-D advection model and a 2-temperature LTNE/piping conceptual solver | Mass + energy conservation, mesh and time-step convergence |
| Beta 3 | Time-series CSP/PV/wind irradiance/weather and dispatch behavior | Weather provenance, consistent kW↔kWh, time-zone treatment |
| Beta 4 | Multi-objective design screening with heat-grade pinch, losses, CAPEX and carbon sensitivity | Stated bounds/units/cost year and Pareto trade-off audit |
| Release | Field-aligned validation report, deployment and presentation | Measured data or honest explicit unvalidated status |

## Team workflow

- One developer owns code integration and architecture.
- Two colleagues independently review literature, units, citations and numerical outputs.
- Commit through GitHub branches. Keep `main` deployable; use pull requests for engineering changes.
- Record permission/disclosure of any instructor-approved AI usage in academic deliverables. ESE101 standard written instruction allows only brainstorming unless a clear instructor exception is provided.

## ESE101 milestones (tentative)

- 17 November 2026 — Interim project report
- 5 January 2027 — English project poster/presentation
- 12 January 2027 — Final report (max 10 content pages excluding cover/references; APA, Times New Roman 11 pt, section headings per information sheet)

Keep the minimum academically necessary literature review and presentation separate from the optional software demonstration.

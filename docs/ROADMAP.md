# Sand Battery Project — Release and Research Roadmap

**Current release: v1.0 academic web research simulator (24 October 2026).**

## v1.0 — Delivered software

- English Python 3.13 / Streamlit interface, responsive dark theme, Plotly graphics and animated silo.
- 0-D sensible-heat charge/standby/discharge solver with an audited energy ledger.
- Optional exploratory direct-contact 1-D LTE model (**not** a pipe-in-sand model calibration).
- Ideal material blends, source scenarios, constrained capacity screening and deterministic scenario export.
- ESE101 Group 8 identity, source-linked research, manufacturer reference installations and APA bibliography.
- GitHub Actions engineering tests plus headless Streamlit AppTest.

**Status:** Research release; not experimentally validated, physically certified or university-endorsed.

## v1.1 — Model verification

1. Collect traceable temperature-dependent medium properties and uncertainty bands.
2. Run independent 1-D conservation, time-step and mesh-convergence audits.
3. Add realistic exchanger outlet-temperature and pinch limitations.
4. Expand parametric sensitivity and uncertainty presentation.

## v1.2 — Better physical architecture

1. Add separate fluid/solid temperatures (LTNE) with defensible correlations.
2. Clearly separate pipe-in-sand closed-loop technology from direct-contact packed-bed concepts.
3. Use sourced time-series CSP/PV/wind data with correct kW, kWh and time-zone conventions.
4. Explore operational scheduling rather than assuming average renewable power is firm capacity.

## v1.3 — Industrial techno-economics

1. Add transparent cost-year and price-range scenarios.
2. Compare heat grade, capacity, power, insulation losses, land/geometry constraints and cost.
3. Document tradeoffs and multi-objective design screening.
4. Seek measured dataset for experimental comparison; label any absence honestly.

## ESE101 tentative milestones

- 17 November 2026 — Interim project report.
- 5 January 2027 — Project poster presentation in English.
- 12 January 2027 — Final project report, APA references, max ten pages excluding cover and references.

**Academic integrity:** The standard course sheet limits AI to brainstorming; the team reports verbal permission to use AI for code. Clarify the instructor exception in writing and disclose permitted AI usage for assessed deliverables.

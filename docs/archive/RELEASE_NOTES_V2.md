# Sand Battery Studio — v2.1 Web Research Preview (v2 foundation)

**Release date:** 24 October 2026  
**Institutional context:** İzmir Institute of Technology (IZTECH), Department of Energy Systems Engineering; ESE101 Group 8.  
**Lead:** Yağız Topaç ([@bysquizy](https://github.com/bysquizy)). Other group-member names not yet provided.

## Included features

### Baseline thermal platform
- English-language Streamlit dashboard and 3D geometry with animated thermal visualization.
- 0-D energy balance during charging, standby and discharging; 1-D LTE research surrogate.
- Basic material/blend comparisons, renewable input scenarios and bounded capacity screening.
- JSON, Markdown and bibliography TXT downloads.

### v2 advanced research modules
- Heat exergy as a reversible thermodynamic upper bound—not actual electricity output.
- Temperature-dependent enthalpy inversion and synthetic, hourly charging/demand dispatch with CSV scenario upload.
- 1-D LTNE separate gas/solid thermal fields in **direct-contact packed beds only**.
- Pressure drop via the Ergun equation and indicative fan power.
- Standalone steady ε–NTU heat exchanger model.
- Assumption-based Monte Carlo parameter sensitivity and hypothetical levelized cost of heat.
- 18 material scenarios with explicit provenance, not certified properties.
- Grid-refinement, insulation-loss and flow-resistance virtual experiments.
- Linked academic sources, technical assumptions, and course-team credits.

## Test evidence

- 42/42 Python 3.13 CI tests passed for the v2 merged main commit, including multipage Streamlit AppTest startup.
- Source browsing and formal unit tests are not a substitute for rendered-browser testing or physical validation.
- No measured field dataset was used to calibrate heat-transfer correlations or material properties.
- The Streamlit live website URL has not yet been provided in chat and has not been independently reviewed.

## Critical model limitations

- Stored MWh(th), useful delivered MWh(th) and exergy MWh(ex) are different quantities; no electricity-to-electricity efficiency claim.
- The packed-bed LTNE / Ergun examples are **not** calibrated models of Polar Night Energy's closed-pipe sand battery.
- Quartz thermal transition around 573 °C is not correctly modeled by current linear cp illustrations.
- Source claims for the Kankaanpää plant heating rating conflict in supplied material (100 kW operator description versus current manufacturer 200 kW listing); preserve context rather than equating these.
- Cost inputs and statistical spreads are hypothetical, not validated project prices or measurement confidence bounds.
- Industrial construction requires additional thermal/mechanical safety work and independent validation.

## Research references

- Bošnjaković, M., & Santa, R. (2026). *Sand batteries for thermal energy storage: A review of operating principles, technologies, challenges and future perspectives*. Clean Technologies, 8(5), Article 165. https://doi.org/10.3390/cleantechnol8050165
- Liu, S., Ahmadi-Senichault, A., Levet, C., & Lachaud, J. (2024). *Development and validation of a local thermal non-equilibrium model for high-temperature thermal energy storage in packed beds*. Journal of Energy Storage, 78, Article 109957. https://doi.org/10.1016/j.est.2023.109957
- Polar Night Energy. *World's first Sand Battery*. https://polarnightenergy.com/reference/worlds-first-sand-battery/
- National Renewable Energy Laboratory. *Economic long-duration electricity storage by using low-cost thermal energy storage and high-efficiency power cycles* (NREL/TP-5700-84728). https://www.nrel.gov/docs/fy23osti/84728.pdf

See [ADVANCED_RESEARCH_V2.md](ADVANCED_RESEARCH_V2.md), [MODEL_VALIDATION.md](MODEL_VALIDATION.md), and [SOURCE_REGISTER.md](SOURCE_REGISTER.md) for modeling boundaries and provenance.

## Team review before academic submission

1. Check all authorship, advisor credit, cited measurements and source access dates.
2. Run realistic lab-scale input cases and independently verify unit conversions.
3. Inspect hosted Streamlit app on desktop and mobile; test sliders, visual animations, CSV upload and export.
4. Disclose all faculty-authorized AI use under the ESE101 course rules.

## v2.1 — Web-first refinement, 24 October 2026

- Added user-supplied live Streamlit link to README, metadata and page navigation.
- Removed the unused local Windows launcher; no new runtime dependencies.
- Corrected v1.0 footer and export metadata to v2.1.
- Updated material chart to a single lighter Plotly bar trace and added interactive maximum-temperature/capacity heatmap.
- Added validation for equal temperature bounds and clearer quartz transition warnings.
- Bounded 0-D scenario caching to reduce repeated simulation on Cloud reruns.
- Correctly attributed the separate Vatajankoski operator (100 kW) and Polar Night Energy developer (200 kW) Kankaanpää thermal-power statements.
- Modernized GitHub Actions and added web/source-integrity tests. CI evidence is available under the repository Actions tab.

**Caution:** the published website URL comes from the project owner; automated CI can test Streamlit page execution, not guarantee the externally hosted browser rendering or production performance.

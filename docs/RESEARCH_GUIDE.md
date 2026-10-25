# Research Guide — Sand Battery Studio

This document provides *short original summaries*, not reproduced pages, from the user-supplied scientific material. All numerical parameters in the website are independently identified as assumptions or sourced values. Review material: **M. Bošnjaković & R. Santa (2026)**, *Clean Technologies, 8*(5), Article 165 ([DOI](https://doi.org/10.3390/cleantechnol8050165)).

| Research topic | Relevant section | Practical interpretation | Application boundary |
| --- | --- | --- | --- |
| Charging, storage and thermal discharge | §3.1 | Separate input conversion, passive cooling and useful heat output | 0-D model assumes mean medium temperature and idealized steady heat delivery |
| Packed beds, thermocline, fluidized/moving-bed and hybrid designs | §3.2 | Architecture determines flow, stratification and contact heat transfer | Direct-contact LTE/LTNE is not a validated closed-pipe design |
| Material properties, conductivity and cycling | §3.1–3.2, §6.2–6.3 | Capacity depends on bulk density and enthalpy; power depends on heat-transfer geometry | Atlas uses 18 examples, many with hypothetical packed-density/cp |
| Thermocline and heat loss | §3.2.2, §4.1, §6.3–6.4 | Hot–cold interfaces spread, reducing useful delivery temperature | 3D animation is an illustration, not measured spatial gradients |
| Renewables integration and operating limits | §1, §3.1, §6.6 | Electrical availability, charging schedules and heat demand differ | Built-in generation traces are synthetic, not site weather data |
| CFD, ML and digital twins | §4 | Numerically plausible solutions still need validation measurements | This application is not a live digital twin or trained AI model |
| Lifecycle costs and sustainability | §5.1–5.2 | LCOH needs annual delivered heat and all relevant energy/capital costs | CAPEX, price and uncertainty inputs are user scenarios |
| Safety, reliability and deployment barriers | §5.3–5.4, §6 | High temperature, electrical, dust, materials and mechanical issues require study | The web models are not building/fire/pressure safety calculations |

## Governing relationship map

Theoretical sensible heat:

\[
Q = \rho_{\mathrm{bulk}} V \int_{T_{\min}}^{T_{\max}} c_p(T)\,dT
\]

Simplified 0-D energy balance:

\[
mc_p(T)\frac{dT}{dt}=P_{\mathrm{charge}}-P_{\mathrm{discharge}}-UA(T-T_a)
\]

Exergy (Kelvin temperatures):

\[
X=m\int c_p(T)\left(1-\frac{T_0}{T}\right)dT
\]

These expressions describe different quantities. A heat store's first-law heat retention is not electricity-to-electricity round-trip efficiency. Additional equations and method boundaries are listed in [ADVANCED_RESEARCH_V2.md](ADVANCED_RESEARCH_V2.md).

## Primary-source discipline

The submitted *Enhanced Source Check and Research Audit* uses **P1/P2/S1/S2/U** to describe evidence provenance; use **MATCH / QUALIFY / MISATTRIBUTED / CONTRADICTED / NOT LOCATED / UNRESOLVED** to describe how a particular claim relates to a particular source. A manufacturer statement graded P2 is still a company statement, not an independently measured validation.

**Source-disagreement example:** The Kankaanpää utility-operator description presents **100 kW / 8 MWh** while Polar Night Energy presents **200 kW / 8 MWh**. The mismatch must be retained with both original links until definitions are reconciled:
- https://www.vatajankoski.fi/en/projects/sand-battery/
- https://polarnightenergy.com/reference/worlds-first-sand-battery/

The Polar Night Energy material describes **closed-loop heat transfer**, with heating applications involving water, air or steam; it also refers to possible future heat-to-electricity conversion. The website does **not** assume that such future conversion exists as a validated round-trip electricity process.

For material comparisons, [NREL report 84728](https://www.nrel.gov/docs/fy23osti/84728.pdf) describes a particular characterized silica sample, including temperature-varying cp and a quartz transition. Illustrative software coefficients are not the same as the original DSC data; therefore no made-up transition enthalpy is added to the model.

## What the website does not claim

No installed prototype, instrumented sensor network, independently validated industrial closed-pipe heat exchanger, structural/safety certification, measured thermal efficiency or investor-ready plant cost is included. Numerical regression tests assess software behavior; publication of a review paper does not certify our chosen model inputs.

Full citations and original links are searchable in the web **Research Hub**. All three Group 8 member names appear in its last tab; university/course calendars are not displayed in the application.

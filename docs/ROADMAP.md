# Sand Battery Project — Engineering Development Roadmap

**Current release:** Sand Battery Studio **v2.1 Web Research Preview**, 24 October 2026.  
**Project:** IZTECH, Department of Energy Systems Engineering · ESE101 Group 8 · Maintainer: Yağız Topaç (@bysquizy).

## Delivered in v1.0

- Responsive, English-language Python 3.13 / Streamlit web application.
- Transient 0-D sensible-heat charge/hold/discharge; auditable input, loss and useful-output ledger.
- Exploratory direct-contact 1-D LTE, animated 3D silo, materials comparison and constrained geometry screening.
- University identification, source links, APA-style evidence catalogue and technical exports.

## Delivered in v2.0 Beta

- Exergy upper bound, temperature-dependent enthalpy inversion and hypothetical source/heat-demand dispatch.
- Exploratory 1-D **LTNE** separated gas/solid temperature model, not calibrated for the closed-loop pipe architecture.
- Packed-bed Ergun pressure loss, ideal ε–NTU exchanger, input uncertainty and scenario LCOH tools.
- Material Atlas: 18 total medium scenarios, including 13 clearly hypothetical comparison entries.
- Virtual experiments: mesh sensitivity, velocity/pressure analysis, standby/insulation thermal-loss screening.
- Three new multipage Streamlit workspaces and **42/42 successful Python 3.13 GitHub automated tests**, including page-start smoke tests.

**Scientific status:** models are numerically exercised but not experimentally validated, a structural safety evaluation, a guaranteed performance prediction, or investment guidance.

## v2.1 — Scientific strengthening (not yet implemented)

1. Add experimentally measured, source-cited temperature-dependent cp, effective conductivity and sample packing densities (with operating ranges).
2. Include enthalpy changes across the α–β quartz inversion when modeling quartz near 573 °C.
3. Expand conservation, mesh/time-step refinement and uncertainty analysis for 0-D, LTE and LTNE models.
4. Add realistic useful-outlet temperature, pressure-flow coupling and heat-exchanger pinch constraints.
5. Add measurement comparison from accessible, compatible laboratory datasets; report fit error and validation limitations.

## v2.2 — Industrial system model (not yet implemented)

1. Differentiate *closed pipe heat transfer in static sand* and *direct-contact packed-bed flow* in both physics and the interface.
2. Evaluate time-stamped real CSP/PV/wind resource data and representative thermal load profiles.
3. Add realistic charge scheduling, parasitic electric consumption, mechanical/insulation safety and material compatibility checks.
4. Extend multi-objective Pareto analyses for thermal delivery, cost, heat loss and industrial footprints.

## Academic deadlines (tentative course calendar)

- **17 November 2026:** Interim Project Report.
- **5 January 2027:** English project poster presentation.
- **12 January 2027:** Final Project Report, APA references and ten-page body limit, excluding cover/references.

The ESE101 course information sheet generally permits AI only for brainstorming. The team reports verbal faculty approval for coding assistance; confirm the exact exception and disclose approved use in assessed submissions.

## Release checklist

- [x] GitHub v2 code merged into main.
- [x] Python 3.13 GitHub automated tests and multipage startup tests passing.
- [x] Source-specific claims and model assumptions documented.
- [x] User supplied the Streamlit public URL, now documented in the website and README.
- [ ] Independent rendered-browser and mobile UX review (site cannot be fetched from this testing environment).
- [ ] Experimental calibration and independently verified input-property datasets.
- [ ] Remaining two team-member names and faculty advisor details confirmed.

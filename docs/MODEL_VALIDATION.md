# Model Specification, Numerical Verification and Validation Gaps

**Status: v1.3 Stage 1 software quality review · 26 October 2026; NOT experimentally validated**

## Model domains

### Storage material and sensible heat

A material is represented as a bulk-density medium with illustrative `cp(T) = cp25 + beta*(T-25°C)` in J/(kg K). Reference enthalpy is `h(T) = cp25*(T-25°C) + beta/2*(T-25°C)^2` in J/kg. Total theoretical storage between Tmin and Tmax is `m*[h(Tmax)-h(Tmin)]`.

**Excluded:** quartz near-573°C phase transition, property hysteresis, sintering, degradation, thermal expansion, compaction, moisture/steam, corrosion and temperature-dependent granular conductivity. This is a simplified *assumption*, not derived from thermophysical measurements for all materials.

### Equivalent heat-transfer coefficient

A cylinder with equal cap and wall insulation: radial cylindrical conduction resistance in series with ambient film resistance. Two caps each use approximate plane-wall conduction plus convection. Thermal bridges, roof details, ground losses, pipe penetrations and fire standards are not included.

### 0-D energy balance

`m*cp(T)*dT/dt = P_thermal_charge - P_useful - UA*(T-Tambient)`.

Charging stops when Tmax is reached; standby is zero-charge and zero-useful-output; discharge stops at Tmin. The solver is `scipy.integrate.solve_ivp` with temperature event triggers and strict relative/absolute tolerances. Assumes constant charging and thermal delivery power.

Ledger identity, referenced to the beginning at Tmin:

`E_model_source_input = E_heater_loss + E_charge_ambient_loss + E_standby_ambient_loss + E_discharge_ambient_loss + E_useful_output + E_final_relative_to_Tmin`.

An analytically reconstructed residual checks internal numerical consistency. **A small residual only tests mathematical accounting, not physical realism.** If the standby period cools below Tmin, remaining *relative* energy is negative; the Sankey is suppressed to avoid negative flow lines.

### 1-D thermocline surrogate

Finite-volume, direct-contact, local-thermal-equilibrium axial transport with effective conduction. **Not calibrated or structurally representative of an electrically heated closed-loop pipe-in-sand silo.** An additional **exploratory 1-D LTNE direct-contact gas/solid** solver and a standalone Ergun packed-bed flow calculator are now available; neither represents a validated embedded-pipe commercial silo. Closed-loop pipe physics remains future work.

### Charging power

- Electric resistance: fixed named MW input and charging efficiency.
- CSP: `Pth = aperture * DNI * assumed efficiency`, constant DNI, not hourly tracking/weather. The simulated input energy is post-optics solar thermal energy, **not electricity** and not gross incident solar irradiance.
- PV/wind: scenario-average power from rated power and capacity factors; not dispatchable continuous power. This is used as a deliberately optimistic constant charging source, and should not be treated as a firm charging guarantee.

### Capacity screening

A discrete grid of volumes, ratios and insulation thicknesses is filtered against max module diameter/height and ranked by calculated useful heat; **not** structural/cost/safety certification or a continuous global optimizer.

## Current software verification scope

GitHub Actions installs the runtime packages on **Python 3.13**, compiles the Streamlit entry point and all page/model modules, runs focused Ruff name/import checks and executes the full Pytest suite. See the latest [CI runs](https://github.com/bysquizy/Sand-Battery-Project/actions) for the **actual run-specific pass count**; do not treat an old snapshot as the current test count.

Current checks include 0-D energy conservation, thermodynamic limits, simplified thermocline/LTNE test cases, design-lab analytical bounds, material scenario provenance, reproducible synthetic dispatch, Streamlit page startup and router navigation. The Stage 1 safety tests reject malformed CSVs, oversize rows, NaN/Inf, negative/out-of-range power values and user-selected heatmap temperatures outside the interval.

**Numerical consistency is not experimental validation.** The new CSV boundaries and corrected heatmap sampling do not alter heat-capacity properties, solver dynamics or manufacturer-performance claims.

Performance, mesh/time-step convergence, full device-temperature validation, mobile-browser QA, pressure-boundary safety and a physical rig comparison remain incomplete.

## External validation requirements

1. Acquire experimental curves for a known system matching geometry, medium, heater, outlet and sensor boundaries.
2. Publish material-specific density, temperature-dependent cp(T) and thermal conductivity data with uncertainty.
3. Compare discharge cutoff, actual usable MWh, measured skin/ground loss, fan/heater losses and transient temperature profiles.
4. Perform grid convergence (n=20,40,80,160), solver step/tolerance sensitivity and net input/output enthalpy audit on the 1-D model.
5. Calibrate the existing exploratory fluid/solid LTNE solver using experimentally suitable heat-transfer coefficients and geometry before claiming a validated predictive model.
6. Confirm structural integrity and code compliance with a qualified engineering analysis before physical fabrication.

## Original v4 regression context

The supplied original code's geometry and `UA` expressions were inspected and preserved in physical meaning. Charge/discharge time formulations align with integral solutions of the same 0-D boundary assumptions; the alpha version instead uses time-domain ODE integration plus a phase-by-phase ledger. A formal full-feature v4 regression is still outstanding.

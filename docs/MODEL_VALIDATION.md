# Model Specification, Numerical Verification and Validation Gaps

**Status: v1.0 academic web research release · 24 October 2026; NOT experimentally validated**

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

Finite-volume, direct-contact, local-thermal-equilibrium axial transport with effective conduction. **Not calibrated or structurally representative of an electrically heated closed-loop pipe-in-sand silo.** Air/solid thermal non-equilibrium, separate heater piping and airflow pressure losses are future-work topics.

### Charging power

- Electric resistance: fixed named MW input and charging efficiency.
- CSP: `Pth = aperture * DNI * assumed efficiency`, constant DNI, not hourly tracking/weather. The simulated input energy is post-optics solar thermal energy, **not electricity** and not gross incident solar irradiance.
- PV/wind: scenario-average power from rated power and capacity factors; not dispatchable continuous power. This is used as a deliberately optimistic constant charging source, and should not be treated as a firm charging guarantee.

### Capacity screening

A discrete grid of volumes, ratios and insulation thicknesses is filtered against max module diameter/height and ranked by calculated useful heat; **not** structural/cost/safety certification or a continuous global optimizer.

## Test coverage

The test suite verifies geometry volumes, temperature enthalpy differentiation, ideal mixing heat conservation, module/insulation monotonicity, temperature and source validation, zero-loss limit, energy-balance identity, charging failure, standby behavior, 1-D sanity, screening constraints and Plotly chart frame construction.

Local test run: Python 3.13.5 with numpy 2.3.5, scipy 1.17.0, pandas 2.2.3, plotly 6.5.2, pytest 9.0.2. **23 tests passed**. Streamlit was unavailable in this isolated build container and pip installation could not reach a package index: the full web UI has not yet been visually smoke-tested. CI and the user's Python 3.13.17 environment should perform this additional test.

## External validation requirements

1. Acquire experimental curves for a known system matching geometry, medium, heater, outlet and sensor boundaries.
2. Publish material-specific density, temperature-dependent cp(T) and thermal conductivity data with uncertainty.
3. Compare discharge cutoff, actual usable MWh, measured skin/ground loss, fan/heater losses and transient temperature profiles.
4. Perform grid convergence (n=20,40,80,160), solver step/tolerance sensitivity and net input/output enthalpy audit on the 1-D model.
5. Add separate fluid-solid LTNE physics after validated heat-transfer coefficients and geometric details are available.
6. Confirm structural integrity and code compliance with a qualified engineering analysis before physical fabrication.

## Original v4 regression context

The supplied original code's geometry and `UA` expressions were inspected and preserved in physical meaning. Charge/discharge time formulations align with integral solutions of the same 0-D boundary assumptions; the alpha version instead uses time-domain ODE integration plus a phase-by-phase ledger. A formal full-feature v4 regression is still outstanding.

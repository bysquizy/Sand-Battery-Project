# Stage 3 — Scientific Model Specification and Verification

**Software:** Sand Battery Studio v1.5 (Stage 3), 26 October 2026.
**Basis:** user-supplied Bošnjaković & Santa 2026 review, Polar Night Energy
technical summary and Enhanced Research Audit, with NREL report 84728 and
engineering literature cross-checks. All results are numerical educational
scenarios; **no industrial thermal battery is experimentally validated**.

## 1. Three architectures, not one interchangeable result

| Calculation | Storage assumption | Heat transfer | Useful-heat limit | Interpretation |
| --- | --- | --- | --- | --- |
| 0-D | One bulk temperature | Prescribed thermal power and uniform ambient UA | Stops at Tmin | Lumped idealized benchmark |
| 1-D LTE | Direct-contact axial packed bed | Finite-volume upwind advection plus effective axial conduction | Configurable 10% charge and 70% discharge defaults relative to Tmin–Tmax | Exploratory through-bed thermocline, **not closed pipes** |
| Closed pipe (v1.5) | One uniform solid temperature | Fluid convection + pipe-wall conduction + effective radial solid resistance | Exchanger outlet grade and power-limited heat delivery | Different, more relevant topology but still **not 2-D CFD or manufacturer calibration** |

**Do not conclude that 1-D outputs should equal 0-D outputs**. The geometries,
flow paths, boundary conditions and discharge cutoffs differ. A relative
difference table is provided to *diagnose* the discrepancy, not declare one
model more accurate without matching experimental evidence.

## 2. Closed-pipe research model

Let `L = tube_count × length_each`, `ri = Di/2`,
`ro = ri + wall_thickness`, and `rc = pitch/2`.
The following series resistances (K/W) are used:

- Inside fluid convection: `Rf = 1/(h_i × 2π ri L)`
- Cylindrical pipe wall conduction: `Rw = ln(ro/ri)/(2π k_pipe L)`
- Illustrative surrounding-medium resistance:
  `Rs = ln(rc/ro)/(2π k_eff L)`
- `UA_pipe = 1/(Rf + Rw + Rs)`
- `Cfluid = mdot × cp_fluid`
- `NTU = UA_pipe/Cfluid`, `epsilon = 1−exp(−NTU)`
- `T_out = T_solid + (T_in−T_solid)×exp(−NTU)`
- `Q_hot = epsilon Cfluid(T_hot_in−Tsolid)`
- `Q_cold = epsilon Cfluid(Tsolid−T_return)`

This is the textbook single-stream exchanger limit against an idealized
uniform-temperature solid reservoir. No axial temperature variation,
mass-transfer mixing, contact resistance, distributor manifold, stress,
two-phase flow or pressure-dependent property variation is solved.

Transient energy conservation uses:

`m cp_s(T) dT/dt = Q_hot − Q_out − UA_ambient(T−Tamb)`

with `Q_out <= requested useful MW` and a **temperature-grade cutoff**
at which the ideal hot outlet cannot reach the specified minimum useful
outlet temperature. In the real plant, meeting this rating depends on HX
layout, bypass/control strategy and application return temperatures.

The returned ledger is:

`E_pipe_heat_in = E_useful_out + E_ambient_loss + ΔE_solid`.

No electrical round-trip efficiency can be derived from the above thermal
ledger because heaters, renewables conversion, pumps/fans and generator
hardware are outside the model. The geometry influence-cell volume constraint
is a numerical screening bound, **not** a physical packing/foundation check.

## 3. Tabulated material cp(T)

`engine/property_curves.py` accepts strictly increasing temperature knots
with finite positive cp. cp is linearly interpolated between knots; specific
enthalpy is integrated *exactly* piecewise. Outside the source temperature
range evaluation raises an error (no unsupported extrapolation).

Displayed example knots are **hypothetical user inputs**. They are NOT
digitized calorimetry and should not be copied into a material catalogue as
measured. NREL report 84728 gives sample-specific high-purity silica results,
including a reported bulk density of 1,543 kg/m³, measured heat-capacity curve
and α–β quartz inversion near 573 °C. Its study does **not** justify an
arbitrary latent-enthalpy spike in the existing application's linear material
models. Source https://www.nrel.gov/docs/fy23osti/84728.pdf

## 4. One-dimensional LTE energy accounting

The direct-contact upwind solver now accumulates:

- Source energy into charge-stage bed;
- Charge-phase ambient losses;
- Hold-phase ambient losses;
- Discharge-stage ambient losses;
- Useful outlet heat and remaining stored energy relative to Tmin.

The residual equals input thermal energy less all losses, outlet heat and
final relative enthalpy. Because its explicit update advances temperature
using cp at the *old* timestep, numerical closure is **not algebraically
exact** when cp(T) varies; report residuals and perform grid/time refinement
rather than claiming physical validation.

## 5. Stage 1/2 maintenance revisions

- Imported schema-v1 JSON now rejects duplicate key names (ambiguous last-key
  wins behavior is not permitted) in addition to previous size/range checks.
- Advanced Research Lab's inactive calculation tabs are no longer eagerly
  executed on each Streamlit rerun. Only the selected research workspace
  computes/plots, reducing unnecessary cloud CPU and refresh work.
- Virtual Experiments stores its active scenario beside each computed grid or
  insulation plot; stale results do not silently display for another design.

## 6. Literature attribution

1. Bošnjaković, M., & Santa, R. (2026). Sand batteries for thermal energy
   storage: A review of operating principles, technologies, challenges and
   future perspectives. *Clean Technologies, 8*(5), 165.
   https://doi.org/10.3390/cleantechnol8050165
2. National Renewable Energy Laboratory. (2023). *Economic long-duration
   electricity storage by using low-cost thermal energy storage and high-efficiency
   power cycles* (NREL/TP-5700-84728).
   https://www.nrel.gov/docs/fy23osti/84728.pdf
3. Wakao, N., Kaguei, S., & Funazkri, T. (1979). Effect of fluid dispersion
   coefficients on particle-to-fluid heat transfer coefficients in packed beds:
   Correlation of Nusselt numbers. *Chemical Engineering Science, 34*(3), 325–336.
   https://doi.org/10.1016/0009-2509(79)85064-2

The Wakao correlation's direct-contact particle-bed applicability is **not**
substituted for a closed-pipe convection coefficient here. Manufacturer
and utility claims retain their own source classes in the Research Hub.

## 7. Explicit out-of-scope evidence

No prototype, measured charge/discharge curves, comprehensive mesh convergence,
2-D/3-D CFD, material-specific oxidation/sintering/phase-change testing,
pressure-vessel mechanical design, qualified thermal-expansion calculation,
fan/pump consumption, construction permit, plant CAPEX quote or operational
dataset. The public site must not describe theoretical simulation heat
efficiencies as measurements.

## 8. Automated and manual verification

See [Stage 3 verification checklist](STAGE3_VERIFICATION.md) for recorded
Python 3.13 CI evidence and required manual Streamlit Cloud acceptance.
These tests cannot establish actual plant performance.

# Equation-to-Code Traceability — Sand Battery Studio v2.0

**Source hierarchy:** mathematical identities and textbook relations support equations;
peer-reviewed literature supports architecture and known limitations; laboratory material
measurements support only the actual tested sample; operator/manufacturer project pages
support attributed plant statements. **Neither numerical verification nor a source link
constitutes physical calibration or independent experimental validation.**

| Model/output | Implemented equation/method | Code | Evidence & source class | Numerical test | Important missing evidence |
| --- | --- | --- | --- | --- | --- |
| Material sensible heat | `E = V ρbulk [h(Tmax) − h(Tmin)]` | `engine/materials.py`, `engine/physics.py` | First law; 2026 <https://doi.org/10.3390/cleantechnol8050165> review | Capacity/enthalpy and conservation tests | Measured cp(T), density for every app medium |
| Charge, hold, discharge | `m cp(T) dT/dt = Pheat − Pout − UA(T−Tamb)` | `engine/physics.py` | Lumped first law; geometry assumptions | 0-D energy balance, zero-loss/bounds | Field time series, heat bridges and installation geometry |
| 1-D LTE direct-contact | Upwind axial advection, effective conduction and loss | `engine/thermocline.py` | Review + related packed-bed methods | Energy ledger, multi-module, cutoff tests | Direct-contact apparatus measurement; not PNE closed tubes |
| 1-D LTNE | Separate solid and air temperatures coupled with assumed hv | `engine/research_v2.py` | Liu et al. (2024), <https://doi.org/10.1016/j.est.2023.109957>, related glass-bead bed | Model test and fixed grid numerical checks | Calibration of hv, void fraction and actual geometry |
| Idealized embedded pipe | `R=Rf+Rpipe+Rsolid`; `ε=1−exp(−UA/(m_dot cp))` | `engine/closed_pipe.py` | Convection, Fourier cylindrical resistance and single-reservoir ε–NTU | Energy closure, transfer monotonicity, cutoff | Pipe routing, axial field, fluid-specific measured properties, pump work |
| Insulation envelope | Cylinder wall + two simplified caps | `engine/physics.py` | Radial Fourier and Newton convection | Analytical UA identity | Thermal bridging and roof/ground detail |
| Multi-layer screen | `Rside=∑ln(ro/ri)/(2πkL)+1/(hA)` | `engine/insulation_layers.py` | Series steady conductive resistance | Single-layer equivalence, monotonicity | Measured k(T), contact/radiant losses |
| Tabulated cp(T) | Piecewise-linear cp with exactly integrated enthalpy | `engine/property_curves.py` | Generic calorimetry mathematics; NREL 84728 specific silica research | Constant/linear analytic integrals, interpolation domain | Digitized valid measurement table, 573 °C quartz transition |
| Solar thermal input | `Pth=aperture×DNI×η` | `engine/solar.py` | Scenario assumption | Deterministic source bounds | Local hourly DNI and optical control |
| Fan flow (direct contact) | Ergun packed-bed pressure gradient | `engine/research_v2.py` | Packed-bed correlation, not embedded pipes | Boundary cases and pressure behavior | Fluid properties / measured pressure losses |
| Energy dispatch | Hourly capped charge/discharge/heat ledger | `engine/research_v2.py` | First-law simplified dispatch | Energy residual, CSV validation | Real load and weather time series |
| Cost estimate | Annualized assumed CAPEX/OPEX ÷ modeled delivered MWh | `engine/research_v2.py` | Assumption-based transparent LCOH | Sensitivity/range tests | Supplier quotations and electricity tariffs |
| 3D axial playback | `T_visual(r,θ,z,t) := T_LTE(z,t)` azimuthally mapped | `engine/thermocline.py`, `visuals_advanced.py` | Visualization of the actual 1-D numerical outputs | Frame/shape/finite/time tests | **No radial model, CFD, or temperature sensors** |
| Design tradeoff & tornado | Repeated 0-D solver calls under disclosed input changes | `pages/8_Visual_Story_Studio.py` | Sensitivity analysis, not an optimizer certificate | Basic figure tests and existing solver checks | Statistical parameter distributions and physical constraints |
| Report HTML and PDF | Data copied from validated scenario and 0-D energy ledger | `engine/report_exports.py` | Reproducible software output + selected citations | HTML escaping, finite-result rejects and PDF syntax tests | No legal/engineering certification; no separate sign-off |

## Attributed real-world reference cases

- **Kankaanpää (2022): 8 MWhth.** Technology developer [Polar Night Energy](https://polarnightenergy.com/reference/worlds-first-sand-battery/) lists **200 kWth**; utility operator [Vatajankoski](https://www.vatajankoski.fi/en/projects/sand-battery/) lists **100 kWth**. Keep each assertion separate. This difference is unresolved; **do not average it**.
- **Pornainen (2025): 1 MWth / 100 MWhth.** [Polar Night Energy](https://polarnightenergy.com/reference/solution-for-clean-energys-big-problem/) describes the installation; crushed soapstone is described as the storage medium. These are manufacturer statements, not this simulator's measured/calibration outputs.
- **Bošnjaković & Santa, 9 October 2026:** peer-reviewed [technology review](https://doi.org/10.3390/cleantechnol8050165). Architecture taxonomy and research gaps, *not a dataset of plant measurements*.
- **NREL 84728:** source-specific thermophysical evidence; not a universal cp(T) curve for quartz and other industrial media. The current UI does **not** import digitized NREL calorimetry and does **not** model the quartz inversion enthalpy.

## What the graphical results mean

The original 0-D animated silo uses uniform colors corresponding to bulk-average
temperature. The new axial playback samples **computed** 1-D states during charging,
standby and discharge. Both styles are educational visual mappings: surface color
is not a sensor reading, and the 1-D front cannot establish temperature across the
radius or structural hot spots. Numeric charts and downloads carry this qualifier.

## Verification vs validation

**Verification:** test that discretization, limiting cases and conservation are
internally consistent with *chosen* equations.

**Validation:** compare predictions against measurements from the same or sufficiently
matched physical configuration. There is **no physical prototype or qualifying data**
provided for this project. Passing GitHub Actions, CodeQL, unit tests or numerical
conservation does not substitute for validation.

See [Model Specification](MODEL_VALIDATION.md), [Stage 3 Methods](STAGE3_METHODS.md)
and [Source Register](SOURCE_REGISTER.md). Recheck all original papers before using
results in a published academic report or equipment-sizing decision.

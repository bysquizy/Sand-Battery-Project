# Sand Battery Studio v2 — Research Methods & Limitations

**Independent student software; IZTECH / ESE101 Group 8.** These features are numerical scenarios, NOT experimental validation or industrial certification.

## Core formulae

1. **Sensible heat:** Q = m × integral[Tmin,Tmax] cp(T) dT. Material parameters are illustrative linear cp(T) inputs. Real phase transitions are not modeled.
2. **Exergy upper bound:** X = m × integral[Tmin,Tmax] cp(T) × (1 - T0/T) dT. Temperatures in the Carnot factor are in kelvin. This is NOT actual recoverable electricity.
3. **Hourly dispatch:** Accepted source × charging efficiency, minus ambient UA heat losses and requested thermal delivery, with capacity/rated-power constraints. Synthetic PV/wind output is seeded and not recorded meteorology.
4. **1-D LTNE:** rho_bulk × cp_s × dTs/dt = k_s × d²Ts/dz² + hv(Tg-Ts) − (UA/V)(Ts-Ta). Gas: eps×rho_g×cp_g×dTg/dt + rho_g×cp_g×u×dTg/dz = k_g×d²Tg/dz² − hv(Tg-Ts). Upwind advection, fixed gas properties. DIRECT-contact bed, NOT Polar Night Energy's closed-loop embedded-pipe configuration.
5. **Ergun:** dP/L = 150 mu (1-eps)² u / (eps³ dp²) + 1.75 rho (1-eps)u²/(eps³ dp); fan power = pressure drop × volume flow / efficiency. Not a closed-pipe pressure-flow model.
6. **Heat exchanger:** Q = effectiveness × Cmin × (Th,in − Tc,in), NTU = UA / Cmin. Steady counterflow/parallel idealization only.
7. **Uncertainty:** Synthetic independent input perturbations for cp, bulk density and UA, not experimentally derived confidence intervals.
8. **LCOH:** (CAPEX × capital recovery factor + fixed O&M + annual energy cost) / annual useful heat. All cost inputs are hypothetical and user-provided.

## Evidence and conflicts

- User-supplied Bošnjaković & Santa (2026), *Clean Technologies*, 8(5), 165: https://doi.org/10.3390/cleantechnol8050165 — review supports research questions but NOT this solver's parameters or field results.
- Liu et al. (2024), *Journal of Energy Storage*, 78, 109957: https://doi.org/10.1016/j.est.2023.109957 — experimental LTNE correlations studied for 16-mm GLASS BEADS, Re 58–252, not our arbitrary sand/media.
- Manufacturer Kankaanpää page https://polarnightenergy.com/reference/worlds-first-sand-battery/ reports 200 kW/8 MWh; user-uploaded Enhanced Source Audit cites operator Vatajankoski for 100 kW/8 MWh. State the disagreement with attribution, not an invented consensus.
- Manufacturer Pornainen reference https://polarnightenergy.com/news/worlds-largest-sand-battery-now-in-operation/ reports 1 MW/100 MWh. Neither commercial plant is an app calibration dataset.
- NREL report 84728 https://www.nrel.gov/docs/fy23osti/84728.pdf reports sample-specific sand bulk density and a measured quartz cp transition peak around 573°C. The app's linear cp is NOT that experimental cp curve.

## Engineering verification still needed

- Measured material DSC properties, packing density, cycling durability, and quartz transition enthalpy.
- Actual exchanger outlet pinch, fan/piping hydraulics, thermal stress and insulation safety.
- Experimental rig data, mesh AND time-step convergence, proper measurement uncertainty.
- Time-stamped weather, process load, tariffs and engineering cost ranges.
- Documented disclosure for ESE101 instructor-authorized AI-assisted development.

**Deployment:** existing main entry point is streamlit_app.py. New optional research pages are auto-discovered by Streamlit in the pages directory. A public GitHub repository is not itself a live hosted app.

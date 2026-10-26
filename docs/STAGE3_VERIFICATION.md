# Stage 3 — Scientific Engineering & Stage 1/2 Revision: Verification

**Software:** Sand Battery Studio v1.5.0
**Date:** 26 October 2026
**Pull Request:** https://github.com/bysquizy/Sand-Battery-Project/pull/18
**Status:** Python 3.13 test gate required before merge; use GitHub Actions
for the final run count and exact passing commit.

## Implementation log

| Scope | Delivered | Scientific limitation |
| --- | --- | --- |
| Closed pipe | Effective resistance of hot-fluid convection, pipe wall and surrounding solid; NTU and outlet-temperature grade; transient energy ledger | Lumped solid, not multidimensional CFD, calibrated heat exchanger, real routing or pump load |
| Model comparison | On-demand 0-D / 1-D LTE numerical comparison with adjustable 1-D cutoffs and result explanation | Different physical configurations and operating boundaries, so outputs are not expected to match |
| 1-D LTE | Charge/hold/discharge ambient losses, remaining enthalpy and numerical residual, including multi-module output scaling | Explicit time integration of temperature-dependent cp gives a discretization error |
| cp(T) | User-assumed tabulated knots with exact piecewise-linear integral and source-domain enforcement | No digitized NREL DSC measurements; quartz transformation unmodeled |
| Multilayer insulation | Concentric sidewall resistance, outside convection, approximate two end caps, layer-interface temperatures | No thermal bridges, ground loss, fire engineering or temperature-dependent k |
| Stage 1 security | JSON import rejects duplicate object keys as well as unexpected fields, NaN/Inf and oversize files | No penetration test or account/authentication system |
| Stage 2 performance | Research Lab selects a single computational workspace; hidden Monte Carlo/cost calculations are not rerun | Not a cloud benchmark or measured page-load time |
| Stage 2 stale results | Experimental result buffers tied to active scenario | Full browser-persistence and all manual change/refresh patterns are not yet tested |

## Verification methods

The new tests in `tests/test_stage3_physics.py` cover:

- Heat-transfer resistance components, UA monotonicity and NTU bounds;
- Closed-pipe source/heat-delivery/ambient/stored-energy conservation;
- Temperature-grade and invalid geometrical/transport input boundaries;
- cp(T) exact constant/linear analytical integration and no extrapolation;
- Direct-contact LTE energy ledger, user cutoff documentation and multi-module scaling;
- Single-layer insulation equivalence to the existing `thermal_ua` function;
- Layered insulation conductivity-versus-loss monotonicity and invalid cases;
- Route opening via Streamlit AppTest, JSON duplicate rejection and lazy Research Lab layout.

CI's Python 3.13, Ruff F401/F821/F823, `pip check`, headless Streamlit
opening and CodeQL workflows do **not** prove independent physical calibration.

## Requested manual web acceptance

- [ ] Open the deployed site and verify the new **Model Verification** page.
- [ ] Run the 0-D/1-D comparison at 10% charge / 70% discharge defaults;
      inspect useful heat, charge/discharge durations and energy residual.
- [ ] Change each cutoff and confirm results recalculate with different bounds.
- [ ] Run the closed-pipe loop with baseline inputs; inspect `UA`, `NTU`,
      threshold outlet, thermal MWh in/out and energy-balance residual.
- [ ] Enter invalid pipe count/pitch or impossible temperature grade and
      confirm clear error feedback without a server exception.
- [ ] Compare one-layer/dual-layer assumed insulation at the same geometry;
      confirm higher insulation resistance reduces modeled heat leak.
- [ ] Edit the hypothetical cp(T) curve and confirm capacity changes;
      check the NREL sample-specific provenance warning.
- [ ] In Advanced Research Lab, switch Exergy / Uncertainty / Cost;
      confirm each remains functional and hidden calculations are not eager.
- [ ] In Scenario Manager, save/load A/B/C and verify numeric baselines still match.
- [ ] Test navigation on a narrow mobile screen and check formula/plot overflow.
- [ ] Read `docs/STAGE3_METHODS.md`, `docs/MODEL_VALIDATION.md`, README,
      `docs/ROADMAP.md` and CHANGELOG for source attribution and consistency.

## Open issues for later stages

Material-specific experimentally digitized cp(T), closed-pipe spatial field,
temperature-variable conductivity, formal asymptotic grid/time convergence,
pressure stress, lifetime fatigue, electric parasitic demand, sensor validation,
plant costing, and fully interactive 3D thermal playback remain future research.

**This report is software verification evidence, not a physical sand-battery
certificate or industrial performance acceptance test.**

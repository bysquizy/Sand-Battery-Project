# Stage 2 — Shared Scenarios & UX: Verification Report

**Release:** Sand Battery Studio v1.4.0
**Date:** 26 October 2026
**Pull request:** https://github.com/bysquizy/Sand-Battery-Project/pull/16
**Status:** Passed GitHub Python 3.13 automated tests prior to main merge.
**Scientific boundary:** Existing thermal equations and assumed properties were
not changed. Model tests verify software behavior, not physical calibration.

## Delivered changes

| Component | Stage 2 result |
| --- | --- |
| Active Scenario | One frozen, validated `Scenario` object shared between all model pages via browser-session state |
| Global design editor | Sidebar form with explicit Apply; material, storage geometry, operating temperatures, charging mode and demand |
| Presets | Three original illustrative presets maintained in one module; no duplicated numerical defaults |
| Dashboard | Duplicate base controls removed; preset application and low-power mode retained; only selected workspace calculates/renders heavy graphics |
| Research Lab & Material Atlas | Initialize from Active Scenario; label temporary local exploratory variations; Research Lab power control accommodates the maximum valid configured PV/wind source |
| Thermal Design | Base medium/geometry sourced directly from the Active Scenario rather than duplicate form |
| Virtual Experiments | Inherit material and operating assumptions for numerical studies; deliberate 400 m³ mesh benchmark documented |
| Scenario Manager | Save/load/clear A/B/C slots; calculate thermal KPI comparison; export comparison CSV; import/export versioned scenario JSON |
| Security | Strict non-executable 40 kB JSON format, named-schema validation, explicit numerical ranges and finite values; previously hardened hourly CSV importer retained |
| Cleanup | Historical release notes for v1 stable and v2/v2.2 beta moved into `docs/archive/`. Original file contents retained. |
| Source code | All existing physics, materials, research and plotting Python modules remain in use, so none was removed merely for its name or original version. |
| Documentation | Version set to 1.4.0, main README, security/model docs, roadmap and changelog updated |

## Automated verification

- Pull-request QA workflow: https://github.com/bysquizy/Sand-Battery-Project/actions/runs/40321403507
- Runtime: Python 3.13.
- **134 tests passed**, including existing engine/physics conservation,
  page-start and navigation, CSV security, new A/B/C JSON boundaries and
  manager slot-save/navigation smoke tests.
- Ruff F401/F821/F823 checks passed.
- Pip dependency consistency checks passed.
- No additional Python runtime packages.

## Manual acceptance checklist

1. Open the [live app](https://sand-battery-project-a5twmepge6cqbndgbz9jmj.streamlit.app/) after main deploy.
2. Expand **Edit shared design** in the sidebar; change total volume from
   1,000 m³ to 1,500 m³; press **Apply to all pages**.
3. Confirm that **Engineering Dashboard**, **Thermal Design Studio**, the
   initial **Material Atlas** screening and **Advanced Research Lab** use the
   1,500 m³ baseline. Local Atlas/Research overrides are intentionally
   separate and must not silently alter the global baseline.
4. Use Dashboard's **Use selected preset** and confirm it changes active
   temperature/volume/source values only after the button click.
5. In **Scenario Manager**, save to A, change the active design, save to B,
   verify both scenarios differ and that their reported MWh were recomputed.
6. Download the **active + A/B/C JSON** bundle, clear a slot, re-upload,
   confirm the loaded names and click **Replace active design and saved slots**.
7. Upload malformed JSON or an unsupported schema and confirm a friendly
   error rather than code execution or an application crash.
8. Verify on mobile that the sidebar and selected Dashboard workspace remain
   navigable; heavy 3D can be disabled via Light mode.
9. Inspect GitHub `docs/archive/`, `README.md`, `CHANGELOG.md` and the
   independent Research Hub: no academic-source records have been discarded.

## Known limitations

- Saved scenarios reside in the user's Streamlit session only; no cross-device
  cloud persistence, private account storage or shareable link is promised.
- Data import is intentionally restricted to schema v1 JSON; numerical output
  files from the older Dashboard results exporter are a different format.
- The Research Lab and Material Atlas retain **local exploratory overrides**.
  Applying a new global scenario resets their baseline inputs. Their local
  changes are not automatically promoted to the active design.
- The 1-D direct-contact LTNE research model still does not represent a
  validated embedded closed-pipe storage plant.
- No measured cp(T) transition enthalpy, real-world physical calibration,
  cross-browser screenshot comparison or comprehensive performance benchmark
  has been completed.
- **CI headless smoke tests are not a substitute for actual hosted-browser
  acceptance testing.**

## Cleanup decision log

- Archived `docs/RELEASE_NOTES_V1_STABLE.md`, `docs/RELEASE_NOTES_V2.md` and
  `docs/RELEASE_NOTES_V22.md` under `docs/archive/`. No scientific source
  or historical milestone was erased.
- Kept `engine/research_v2.py`, `engine/material_scenarios_v2.py`,
  `visuals.py`, `engine/thermocline.py`, and every actively imported
  application module. Renaming/deleting these simply to remove old version
  suffixes could break references without improving runtime behavior.
- Did not delete automated tests merely because their filenames mention older
  releases; they remain useful regression evidence.

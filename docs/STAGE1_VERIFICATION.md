# Stage 1 — Foundation & Security: Verification Report

**Release:** Sand Battery Studio v1.3.0
**Date:** 26 October 2026
**Scope:** Stage 1 of the five-stage plan; **no new physical equations or major UI redesign**.
**PR:** https://github.com/bysquizy/Sand-Battery-Project/pull/15

## Completed work

| Area | Change | How to review |
| --- | --- | --- |
| Python environment | Codespaces upgraded from Python 3.11 to 3.13; unsafe CORS/XSRF disabling and unnecessary apt upgrade removed | `.devcontainer/devcontainer.json` |
| Uploaded user CSV | Strict 1 MB and 8,760 hourly-row caps, UTF-8, column width/schema, finite numeric values, nonnegative values and 1,000 MW server-input ceiling | `engine/input_validation.py`, `tests/test_input_validation.py` |
| Research Lab | Validated inputs and friendly error messages before solving; optional CSV now uses the shared parser | `pages/1_Engineering_Research_Lab.py` |
| Material Atlas | Temperature sweep is bounded by the user-selected Tmin/Tmax rather than silently using values above Tmax | `pages/2_Material_Atlas.py` |
| Code cleanup | Removed audited unused imports (no solver formula rewrite) | Pull request diff; Ruff |
| Release identity | Added `project_version.py` and aligned UI/export, README, CFF, security and tests to v1.3 | `project_version.py`, `pyproject.toml` |
| Release documents | Streamlined the current changelog and roadmap; archived the contradictory original beta chronology | `CHANGELOG.md`, `docs/archive/CHANGELOG_PRE_V1_3.md`, `docs/ROADMAP.md` |
| Model transparency | Removed obsolete v1.0/23-test claims and clearly separated numerical verification from experimental validation | `docs/MODEL_VALIDATION.md` |
| CI | Focused Ruff F401/F821/F823 checks, `pip check`, full model/page compilation and Pytest | `.github/workflows/quality.yml` |

## Automated verification evidence

- **Pull-request CI**: https://github.com/bysquizy/Sand-Battery-Project/actions/runs/40311260031
- **Python:** 3.13 (GitHub Actions runner).
- **Results:** **105 tests passed**, including previous physical model regression checks, Streamlit page startup, malicious CSV boundary cases, below-300°C Material Atlas guard, release metadata, safe development settings and version consistency.
- Ruff unused-import/undefined-name checks passed.
- `python -m pip check` passed.
- Runtime dependencies are still **Streamlit, NumPy, SciPy, Pandas and Plotly**; no runtime dependency added.

Passing numerical energy-ledger tests does **not** establish that a field thermodynamic system is accurate.

## Deliberately deferred from Stage 1

1. Shared cross-page scenario state and A/B/C comparison — Stage 2.
2. More advanced 0-D/1-D heat-transfer physics, real measured cp(T) and validation — Stage 3.
3. New 3D animations, charts and automated reporting — Stage 4.
4. Full browser/mobile visual acceptance, long-term release packaging and GitHub metadata — Stage 5.
5. Locking a resolved *transitive* dependency tree was not done: the 5 primary version ranges remain unchanged. A reproducible lock can be generated only after choosing and testing the intended deployment environment.

## Items for the student reviewer

- [ ] Open the deployed Streamlit application after the merge/redeploy; visit all six pages.
- [ ] In Material Atlas, set **Tmax = 250 °C**, select several materials and confirm the heatmap never exceeds 250 °C.
- [ ] In Advanced Research Lab, upload a valid `available_mw,demand_mw` CSV and observe the graph.
- [ ] Upload a CSV containing negative input, NaN, missing column or malformed row and confirm a friendly error appears.
- [ ] Verify that Dashboard temperature/energy values match your previous saved baseline inputs (mathematical equations have not been modified).
- [ ] Inspect the new GitHub README, security policy, roadmap and changelog.
- [ ] Test phone/tablet layout separately; CI does not render a real browser.

**Unverified:** Real Streamlit Cloud/browser release behavior, real-world material-property calibration, field-device performance, independent penetration testing and a structural/electrical/thermal safety assessment.

This report is a software verification log, not a thermal storage equipment certificate.

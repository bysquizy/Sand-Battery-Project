# Sand Battery Studio — v1.0 Stable Software Release

**Date:** 24 October 2026  
**Live application:** https://sand-battery-project-a5twmepge6cqbndgbz9jmj.streamlit.app/  
**Repository:** https://github.com/bysquizy/Sand-Battery-Project  
**Academic context:** IZTECH, Department of Energy Systems Engineering, ESE101 Group 8.

## Why a v1.0 release after research betas?

Version 1.0 establishes a **stable software presentation baseline** for academic demonstrations, consolidating the earlier research-preview experiments and design updates. It does **not** represent physical validation, a complete industrial plant model or a finalized graduation thesis.

## Stability fixes

1. Removed the hard requirement to import `MODEL_EVIDENCE` by name in `home_app.py`. During a Streamlit Cloud rolling update, an older cached `project_info` may not expose that optional register; the dashboard now remains available and the source-register section explains any temporary omission.
2. Tested the real `streamlit_app.py` multipage entry point and navigation to all three research pages, not only separately launched page scripts.
3. Added a regression simulating an older `project_info` module without the optional evidence mapping.
4. Preserved 0-D thermal-cycle models, optional direct-contact LTE/LTNE, exergy, materials, plots and exports without new Python dependencies.
5. Consolidated version labels and documentation, retaining past beta milestones in CHANGELOG as historical development records.

## Accepted software features

- Dark responsive engineering dashboard; optional 3D thermal illustration and lightweight mobile mode.
- 0-D thermal charge/standby/discharge with energy accounting; 1-D exploratory thermal models.
- Three demonstrative presets and grouped navigation.
- Material Atlas, source-labeled engineering equation register and APA-style Evidence Library.
- Hourly synthetic renewable dispatch, isolated exchanger/flow calculators and numerical virtual experiments.
- Browser-first hosted operation; Python 3.13 GitHub automated test workflow.

## Explicit scientific limitations

- The solid-media data currently include **illustrative** density and linear cp coefficients. Quartz phase transition near 573 °C is not modeled by the legacy cp approximation.
- A direct-contact packed-bed LTNE solution is not a validated model of Polar Night Energy's sealed air-pipe system.
- The Kankaanpää thermal-rating discrepancy remains attributed to its sources (100 kW operator; 200 kW system developer).
- Economic figures and uncertainty distributions are scenarios, not measured plant results.
- Python testing and numerical energy closure do not substitute for field measurements or structural/thermal certification.

## Test evidence and independent review

GitHub Actions Python 3.13 runs syntax, Ruff checks, numerical/unit tests, app startup and **router-level page navigation**. The actual deployed Streamlit Cloud instance is outside GitHub Actions: check the live page and, if necessary, reboot its app session after merge. The code release is considered software-stable when its CI passes; no assertion of fully verified browser rendering is made until tested on the hosted site.

## Next academic steps

Submit the course's assessed documents in English with APA references; confirm contributor names and authorized AI use with your group and instructor. Before adding engineering claims, obtain reliable material test data and independently check model applicability.

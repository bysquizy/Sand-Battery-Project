# Changelog

Software release history for Sand Battery Studio. All physical modelling results
remain research examples, not certified industrial-system predictions.

## Unreleased — Layered 3D storage view
- Replace the five-stage illustrative cylinder with steel cladding, insulation, granular core cut faces, lid and footing; provide exterior/cutaway selection.
- Drive at most 36 playback frames directly from solver samples, with synchronized mean temperature, elapsed time and material-enthalpy-based heat above Tmin.
- Keep all steel neutral; explicitly distinguish illustrative construction details from physical model outputs and show one representative module with total-module heat.
- Place compact horizontal playback controls and an unlabeled scrubber below the 3D scene to prevent long mobile phase labels from clipping; keep the numeric phase/time readout visible.
- Preserve native camera interaction, stable language-independent view selection and Light mode that bypasses the 3D renderer.

## Unreleased — Web release consistency
- Explain Apply semantics, local research overrides, ephemeral sessions and JSON backup/restore in the browser-first README.
- Distinguish restorable scenario JSON from numerical output JSON; warn that importing an active-only bundle clears saved A/B/C slots.
- Translate critical Dashboard, shared-editor, Scenario Manager and report-download controls into Turkish; document remaining English scientific content.
- Preserve Dashboard and Visual Story workspace selection across language changes using stable internal values.
- Reduce the scenario file picker's transport ceiling to 1 MB, explain the separate strict 40,000-byte scenario validation limit, and require Streamlit 1.66.1 or newer for the upload API used here.
- Update ten-screen documentation and add prioritized browser/mobile acceptance criteria without claiming unfinished checks passed.

## [2.1.0] — 2026-10-26 (Premium Interface & Security Revision)
- Unified all nine Streamlit workspaces with source-only, dependency-free
  native theming and safe static HTML/CSS: accessible headers, product identity,
  consistent KPI cards, navigation, context ribbon and project footer.
- Designed mobile spacing, more readable technical annotations, keyboard
  focus, high-contrast source labels and reduced-motion behavior.
- Replaced legacy continuously animated decoration with bounded entrance
  motion and preserved existing calculated Plotly animations.
- Escaped user-supplied scenario names before rendering the context ribbon.
- Neutralized spreadsheet formula prefixes in imported scenario-name
  cells when exporting A/B/C comparison CSV; original numeric data stays intact.
- Enabled CORS/XSRF protections explicitly; retained five lightweight
  dependencies and all physics engines.
- Added cross-page QA for premium layout, security, native configuration,
  user metadata and CSV export; real browser acceptance remains manual.

## [2.0.0] — 2026-10-26 (Stages 4/5: Visual Engineering & Publication)
- Added independent Visual Story Studio: computed 1-D axial temperature
  snapshots mapped onto an interactive Plotly 3D cylinder and synchronized
  temporal heatmap, both clearly labeled as axial model representations.
- Added bounded volume/insulation tradeoff and deterministic ±10%
  input-sensitivity plots, computed only when requested.
- Added self-contained illustrated HTML and compact native PDF reports,
  plus CSV and reproducible JSON exports with no additional dependencies.
- Extended Research Hub source matrix and published true source-attributed
  Kankaanpää/Pornainen rating comparison; removed arbitrary flow percentages
  used for the decorative conceptual Sankey.
- Added accessible repository architecture illustration, equation/source/code
  traceability register, release QA checklist, standardized version and links.
- Preserved unvalidated simulation disclosures; no measured sensor feeds,
  arbitrary quartz phase enthalpy or manufacturer calibration inferred.

## [1.5.0] — 2026-10-26 (Stage 3: Scientific Verification)
- Added a separate lumped-solid closed-pipe heat-transfer research model with fluid, pipe-wall and surrounding-solid thermal resistances, outlet-grade constraints and a phase-integrated energy ledger.
- Added a 0-D/1-D comparison interface with explicit divergent physical assumptions and user-adjustable direct-contact model cutoffs.
- Added a source-labelled multilayer cylinder insulation screen, including interface temperatures and comparison to the old one-layer thermal UA.
- Added cp(T) knot interpolation, exactly integrated piecewise sensible enthalpy and strict source-domain handling; no invented quartz phase-transition enthalpy.
- Extended 1-D LTE with phase ambient-loss tracking, stored enthalpy and numerical energy closure.
- Revised Stage 1/2: duplicate imported JSON keys are rejected; hidden Research Lab sections no longer calculate; stale experiments are hidden after active-design changes.
- No new runtime dependencies. No claim of calibrated industrial physical performance.

## [1.4.0] — 2026-10-26 (Stage 2: Shared scenarios & user experience)
- Aligned Research Lab charging-power control with the full valid shared PV/wind source range.
- Added one validated `Active Scenario` for the dashboard, Material Atlas,
  Research Lab, Virtual Experiments, and Thermal Design Studio.
- Added a compact shared sidebar editor; page-specific exploratory controls
  are labelled as local overrides and reset on applying a new active design.
- Added Scenario Manager: independent A/B/C saved designs, calculated comparison
  results, CSV output and strict 40 kB / schema v1 JSON import/export.
- Changed Dashboard from eagerly evaluated tabs to selected-workspace rendering,
  reducing unnecessary Plotly/3D and screening calculations.
- Archived superseded alpha/beta release-note files under `docs/archive`; kept
  all physics and materials Python modules because they remain used.
- Preserved Stage 1 security validation, numerical equations and the original
  five runtime dependencies.

## [1.3.0] — 2026-10-26 (Stage 1: Foundation & Security)
- Hardened hourly CSV uploads: UTF-8, 1 MB maximum, 8,760 row limit, expected
  numeric columns, finite nonnegative values and bounded power inputs.
- Fixed Material Atlas heatmap temperatures to honor the user-selected maximum.
- Made invalid Research Lab thermal designs show an explanatory error instead
  of throwing a page exception.
- Matched Codespaces/devcontainer to Python 3.13; removed commands that disabled
  Streamlit CORS and XSRF protections.
- Added the software-version module, Python and tooling metadata, targeted
  regression tests, expanded static analysis and dependency-consistency checks.
- Updated security, model-verification and roadmap docs; preserved historical
  changes in [the archive](docs/archive/CHANGELOG_PRE_V1_3.md).
- No new runtime packages or thermodynamic solver equations.

## [1.2.0] — 2026-10-26
- Added the Group 8 research hub, scientific summaries, source attribution and
  credits for Yağız Topaç, Semih Cenk and Fatma Ovacık.
- Removed duplicate academic information from the main dashboard.

## [1.1.0] — 2026-10-26
- Added Thermal Design Studio: cooling, modular geometry, radial insulation
  and reverse theoretical thermal-capacity sizing.

## [1.0.0] — 2026-10-26
- Established a stable software release baseline with Streamlit multipage
  navigation and compatibility checks for optional research metadata.

## Historical beta iterations
Earlier exploratory v2.0–v2.2 beta commits preceded the deliberate v1.0
software rebaseline. Their original notes remain available in
[the archived change log](docs/archive/CHANGELOG_PRE_V1_3.md).
These older labels are **not** currently supported release versions.

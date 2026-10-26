# Changelog

Software release history for Sand Battery Studio. All physical modelling results
remain research examples, not certified industrial-system predictions.

## [1.4.0] — 2026-10-26 (Stage 2: Shared scenarios & user experience)
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

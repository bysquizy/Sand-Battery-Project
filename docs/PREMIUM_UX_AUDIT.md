# Premium UX, Source Integrity & Security Audit — v2.1

**Release scope:** Streamlit user interface, repository storefront, documentation consistency, export trust boundaries, and non-breaking regression checks. All nine pages were revised without changing the physical equations or adding runtime dependencies.

## Decisions and evidence

| Topic | Action completed | Remaining limit |
|---|---|---|
| Brand consistency | Native dark-teal/copper Streamlit theme, global CSS tokens, uniform header + footer for nine pages | Real rendered mobile screenshot comparison not available in the repository API |
| Dashboard | One clear leading hero with meaningful model disclaimers and canonical GitHub link | Data plots remain interactive, but chart layout needs live-phone acceptance |
| Sidebar | Unified branded header, grouped page navigation, controlled scenario editor | Some advanced Streamlit widgets remain lengthy on narrow screens |
| Scenario identity | Escaped dynamic label; material, volume, Tmin/Tmax, charging source/power chips | Browser-session-only storage, not an account sync feature |
| Animation | Previous model-driven Plotly animation retained; decorative continuous CSS motion replaced with one short intro | Static CSS visual is not a measured temperature gradient |
| Accessibility | Improved contrast and annotation sizes, keyboard focus, reduced-motion preference and legible charts | Formal WCAG audit with screen reader/device testing not conducted |
| HTML safety | Static source-defined HTML/CSS only; all dynamic text in custom HTML helpers escaped | Streamlit's sanitizer remains a platform boundary; native widgets used for interaction |
| Cross-site protections | Explicit Streamlit server CORS/XSRF enabled | Security headers/CSP are set by Streamlit Cloud and cannot be independently controlled in this repository |
| CSV exports | A/B/C comparison names are formula-neutralized against =, +, -, @ and leading whitespace | Spreadsheet-specific importing may require further downstream consumer precautions |
| User input | Existing size/type/schema bounds for JSON and hourly CSV preserved | No authenticated user accounts or data persistence |
| Python stack | Still only Streamlit, NumPy, SciPy, Plotly and Pandas | Vulnerability landscape changes; monitor Dependabot alerts |
| Research sources | Source attribution and unresolved Kankaanpää 100/200kW differences retained | Manufacturer specs do not validate simulator output |
| Repository | Release v2.1, README badge/architecture image, transparent roadmap and security docs | GitHub About Website field and formal Release may require direct maintainer UI action |

## Accessibility and reduced-motion rationale

Native `st.metric`, `st.button`, `st.radio`, `st.tabs`, charts and form fields remain Streamlit controls with built-in semantics. HTML is used only for passive banners, context chips and credits. The hero animation is a single entrance motion, not an infinite autoplay effect. The CSS respects `prefers-reduced-motion: reduce`.

## Research integrity boundaries

- 0-D models have uniform bulk temperature and numerical heat loss, not 3D CFD.
- 1-D visualization maps *calculated* axial data around a silo but does not resolve radial gradients.
- Closed-pipe, packed-bed LTE and LTNE are separate topologies; no false one-to-one commercial calibration.
- Quartz inversion near 573°C is still a warning, not a validated latent/transition enthalpy.
- Theoretical energy balance closure is not experimental accuracy.
- Kankaanpää thermal power from developer (200kW) and operator (100kW) must both be separately attributed; capacity 8MWh. Pornainen 1MW/100MWh is manufacturer-sourced.

## QA procedure

1. CI Python 3.13 compiles all pages and engine modules, then runs Pytest page startup, numerical conservation, data import, CSV injection and accessibility checks.
2. Ruff flags undefined names and unused imports. Pip consistency checks dependency compatibility. CodeQL scans Python and GitHub Actions.
3. Real browser acceptance remains separate: desktop and mobile widths, sidebar, dark mode contrast, keyboard traversal, low-motion setting, PDF downloads and long 3D playback.
4. The user-supplied DOCX research notes are retained as source provenance only; original external papers must be read and cited individually before any scholarly submission.

## Links

- [Live application](https://sand-battery-project-a5twmepge6cqbndgbz9jmj.streamlit.app/)
- [GitHub](https://github.com/bysquizy/Sand-Battery-Project)
- [Equation/source/code mapping](EQUATION_TRACEABILITY.md)
- [Stage 1 review](STAGE1_VERIFICATION.md)
- [Stage 2 review](STAGE2_VERIFICATION.md)
- [Stage 3 methods](STAGE3_METHODS.md)
- [Stage 4/5 release QA](RELEASE_2_0_QA.md)

**No claim of experimental calibration, industrial safety certification, or independent live web-browser inspection is made.**

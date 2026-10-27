# Sand Battery Project

**Sand-based thermal energy storage — numerical simulation and research project**

**Group 8:** Yağız Topaç · Semih Cenk · Fatma Ovacık

**Web application development:** Yağız Topaç ([@bysquizy](https://github.com/bysquizy))

[Run the simulation](https://sand-battery-project-a5twmepge6cqbndgbz9jmj.streamlit.app/) · [Source code](https://github.com/bysquizy/Sand-Battery-Project)

## Project overview

This is a student engineering project investigating how sand and other granular materials can store energy as heat. The Streamlit application explores charging, heat retention, thermal discharge, insulation, storage geometry and material-property assumptions through numerical models.

The project is **software-only**. Charts are illustrative numerical results. Results are simulations, not measured performance from a physical prototype or commercial battery. Energy capacity is reported as **thermal energy** (MWh), not electricity generated.

## What the application does

- **Engineering Dashboard:** explores charging, stored heat, useful thermal output and heat losses.
- **How It Works / Nasıl Çalışır?:** explains the simulation and its assumptions.
- **Thermal Design Studio:** compares insulation and tank-design choices.
- **Scenario Manager:** keeps up to three designs in the current session, compares them and exports portable JSON backups.
- **Model Verification:** inspects calculation and energy-balance assumptions.
- **Visual Story Studio:** visualizes modeled temperatures and exports reports.
- **Advanced Research Lab, Material Atlas and Virtual Experiments:** explores materials, sensitivities and additional simplified engineering models.
- **Research Hub:** documents the project background, sources and limitations.

Engineering pages start from a shared active scenario. Research Lab and Material Atlas allow explicitly labelled local overrides; some virtual experiments use reference inputs (for example, the grid study fixes volume at 400 m³). These do not update the active scenario. Storage time is an adjustable model input, not a project deadline.

## How it works

Electrical or solar energy is represented as thermal input. A model estimates sensible heat stored in a granular medium and tracks heat losses during storage and discharge. The idealized energy relationship is:

```text
Q = m × cp × ΔT
```

Actual predictions depend on the chosen heat capacity, temperature range, geometry, insulation, power inputs and model assumptions. The application includes simplified 0-D and 1-D approaches, which do not describe identical physics.

## Access

Use the [live web application](https://sand-battery-project-a5twmepge6cqbndgbz9jmj.streamlit.app/) directly in your browser. No desktop application or local installation is required.

## First use / İlk kullanım

1. Open the live application. Choose **English** or **Türkçe** in the sidebar; English is the default. On mobile, open the sidebar first.
2. Open **Edit shared design / Ortak tasarımı düzenle**, change the model inputs and press **Apply to all pages / Tüm sayfalara uygula**. Unsubmitted edits do not change the model.
3. Review the Dashboard. Run optional 1-D models and design screens explicitly; after changing their inputs, recalculate before interpreting results.
4. In **Scenario Manager / Senaryo Yöneticisi**, save the active design to A, B or C and compare the saved designs.
5. Download a scenario JSON backup before leaving or refreshing the application. **Session storage is temporary**, can be lost on reload/disconnection and does not sync across devices.

**Türkçe:** Yan menüden dili seçin → ortak tasarımı düzenleyin → **Tüm sayfalara uygula** düğmesine basın → sonuçları inceleyin. A/B/C kayıtları geçicidir; çalışmanızı korumak için senaryo JSON dosyasını indirin.

Core navigation and key controls support Turkish and English. Some advanced research text, tables, model errors and exported reports remain in English; this is not a complete translation of every scientific resource.

### Save, restore and reports

| Download | Purpose | Import into Scenario Manager? |
|---|---|---|
| Dashboard: **Save active scenario · JSON** | Active design only; A/B/C slots in this bundle are empty | Yes; importing replaces the active design **and clears existing slots** when applied |
| Scenario Manager: **Download active + A/B/C · JSON** | Backup of the active design and all three saved slots | Yes; applying replaces the active design **and all saved slots** |
| Visual Story Studio: **Download editable scenario JSON** | Active design only, with empty A/B/C slots | Yes; the same replacement rule applies |
| Dashboard: **Export numerical results · JSON** | Snapshot of calculated outputs | No |
| HTML / PDF / Markdown / CSV | Reports or numerical tables | No; these are not scenario backups |

Scenario import accepts schema-v1 JSON up to **40,000 bytes**, regardless of the file picker's separate 1 MB transfer ceiling. Review the imported design before applying, and back up your current bundle first. Invalid files leave the current design and saved slots unchanged.

For phones, enable Dashboard **Light mode** to skip its 3D view. Visual Story Studio has a separate **2D-only / mobile-friendly view** switch. These settings apply to their respective workspaces.

Compact PDF reports may transliterate non-ASCII characters. The illustrated HTML report retains Unicode and can be printed to PDF in your browser.

If the app fails to load, reload once; if the issue persists, report the page, browser and error through the repository issues. Reloading can reset session data. Browser and physical-phone acceptance is tracked separately from automated tests in [the release checklist](docs/WEB_ACCEPTANCE.md).

## Sources and limitations

The project documentation records equations, citations, evidence quality and model limitations:

- [Equations and assumptions](docs/EQUATION_TRACEABILITY.md)
- [Research guide](docs/RESEARCH_GUIDE.md)
- [Source register](docs/SOURCE_REGISTER.md)
- [Model verification](docs/MODEL_VALIDATION.md)

Reference systems described in the research are **not** calibration or validation data for this simulator. Commercial performance, electricity-to-electricity efficiency and planned emissions reductions must not be confused with the results of this educational model.

## Repository structure

- `streamlit_app.py`, `home_app.py`, `pages/`: application screens.
- `engine/`: numerical models and input validation.
- `scenario_state.py`: shared scenario state.
- `project_info.py`, `research_notes.py`: project information and references.
- `docs/`: methodology and documentation.
- `tests/`: automated regression tests.

**License:** No general open-source license has been selected by the contributors.

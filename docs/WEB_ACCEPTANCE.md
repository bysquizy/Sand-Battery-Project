# Web release acceptance

Status: **pending for the revised build**. Automated tests do not complete this checklist.

The previous main baseline `d0fbc8e68cca8db3932e14af0905c15bd945719c` passed 205 tests in [CI](https://github.com/bysquizy/Sand-Battery-Project/actions/runs/40387317283). On 27 October 2026 a cloud desktop browser opened the live Dashboard, switched English to Turkish, and navigated to Scenario Manager with Turkish retained. That was limited smoke testing, not physical-phone acceptance or proof of the deployed SHA.

Record for each case: deployed SHA, date, device, OS/browser version, language, steps, expected/actual result and pass/fail evidence. Resolve P0 failures before accepting a release. P1 failures need a fix or an explicit documented release limitation.

## P0 — release gates

- [ ] Confirm the deployed SHA matches the tested commit and its CI passes. From a clean session, open all ten screens, direct page URLs, refresh and back/forward without exceptions.
- [ ] Change shared volume without Apply: calculations stay unchanged. Apply: Dashboard, Design, Verification and reports show the committed inputs. Local research overrides remain explicitly identified.
- [ ] Run 1-D playback, sensitivity and design screening. Change the active design: stale results must disappear until recomputed for the new inputs.
- [ ] Save distinct A/B/C designs, download the complete JSON bundle, start a new session, import and apply. Every field and slot must round-trip. An active-only bundle must warn before replacing and clearing slots.
- [ ] Upload malformed, wrong-schema, oversized and numerical-results JSON. Show an understandable rejection; preserve existing active design and saved slots. The file picker uses a 1 MB transport ceiling; the application enforces at most 40,000 bytes for a scenario.
- [ ] Download/open HTML, PDF, CSV, output JSON and scenario JSON. Values match the current active design. HTML preserves Unicode; compact PDF transliteration is disclosed. Downloads do not unexpectedly reset the model.
- [ ] On a physical Android phone (Chrome) and iPhone (Safari), test portrait/landscape, sidebar open/close, all inputs, Apply, A/B/C and downloads. No essential control may be clipped or unreachable; chart touch gestures must not trap page scrolling.

## P1 — interaction, performance and accessibility

- [ ] Use the actual language selector EN → TR → EN on all ten screens, before and after calculations. It never becomes empty; active scenario, saved slots and selected workspace remain stable. Evaluate pending form edits and explain any reset.
- [ ] Check 360/390/768/1366 px widths, long Turkish labels, wide tables and 200% zoom. Page controls remain usable; table-local horizontal scrolling is acceptable.
- [ ] Verify Plotly play/pause/reset, zoom, tooltips and figure exports. Dashboard Light mode and Visual Story 2D-only mode are separate; neither should build its skipped 3D chart.
- [ ] Exercise representative high-cost calculations and repeated navigation. No frozen UI or unbounded reruns; old results are not mislabeled as current while recomputing.
- [ ] Keyboard-only: visible focus, logical order, operable language picker/sidebar/form, no focus traps. Screen reader: labels, validation errors and important results are understandable.
- [ ] Reduced-motion setting and dark-theme contrast: test actual rendered controls and plots; static CSS assertions alone are insufficient.
- [ ] Check README live-app/source links and in-app method/reference links. Broken scientific links should retain citation details and be recorded.

Suggested desktop matrix: Chrome or Edge plus Firefox. Mobile emulation helps layout checks but does not replace physical Android/iOS behavior. No device/browser result should be marked passed without running it.

## Layered Dashboard 3D revision

For the revised build, also verify: cutaway/exterior switching, camera drag, play/pause/reset and scrubber behavior at 360 px width. The phase, temperature, time and heat-above-Tmin readouts must change together. Steel must remain neutral; only the inner core changes thermal color. Geometry uses the active design; one module is shown while heat is for all modules. Switch material and module count, and confirm no old model result survives. Activate Light mode and confirm the 3D canvas is absent. Physical-phone interaction remains a manual gate.

"""Stage 2: versioned scenario persistence, input boundaries and multipage UI."""
from dataclasses import asdict, replace
import json
from pathlib import Path

import pytest

from engine.materials import MATERIALS
from engine.physics import summarize
from engine.scenarios import (
    MAX_IMPORT_BYTES, PRESETS, SCHEMA_VERSION, SLOTS, Scenario,
    from_json, from_mapping, to_json,
)

ROOT = Path(__file__).resolve().parents[1]


def test_presets_are_valid_distinct_scenarios():
    for name, scenario in PRESETS.items():
        assert scenario.name == name
        scenario.validate()
        assert scenario.charge_power_mw() > 0


def test_shared_scenario_maps_to_same_engine_result():
    s = Scenario()
    s.validate()
    d = s.make_design()
    out = summarize(d, MATERIALS[s.material_name])
    assert d.volume_m3 == s.volume_m3
    assert d.maximum_c == s.maximum_c
    assert out["capacity_mwh"] > 0


def test_all_charge_sources_preserve_source_kind():
    baseline = Scenario()
    assert baseline.make_design().source_kind == "electricity"
    csp = replace(baseline, source="CSP thermal")
    csp.validate()
    assert csp.make_design().source_kind == "solar_thermal"
    hybrid = replace(baseline, source="PV + wind")
    hybrid.validate()
    assert hybrid.charge_power_mw() > 0


@pytest.mark.parametrize(
    "change",
    [
        {"maximum_c": 10},
        {"minimum_c": 200, "maximum_c": 180},
        {"volume_m3": float("nan")},
        {"electric_mw": float("inf")},
        {"material_name": "unverified exotic"},
        {"modules": True},
        {"source": "Unknown energy"},
        {"source": "PV + wind", "pv_mwp": 0, "wind_mw": 0},
        {"name": "x" * 49},
        {"ambient_c": 45, "minimum_c": 20},
        {"insulation_m": -1},
    ],
)
def test_scenarios_reject_unphysical_or_unbounded_data(change):
    with pytest.raises(ValueError):
        replace(Scenario(), **change).validate()


def test_versioned_json_round_trip_with_all_three_slots():
    active = PRESETS["Compact research study"]
    saved = {"A": PRESETS["Industrial thermal store"],
             "B": PRESETS["CSP-assisted thermal storage"], "C": None}
    blob = to_json(active, saved).encode("utf-8")
    restored, slots = from_json(blob)
    assert restored == active
    assert slots == saved
    assert json.loads(blob)["schema_version"] == SCHEMA_VERSION


@pytest.mark.parametrize("bad", [
    b"",
    b"{",
    b"\xff",
    b"x" * (MAX_IMPORT_BYTES+1),
    b'{"schema_version":2,"active":{},"saved":{}}',
    b'{"schema_version":1,"active":{},"saved":{}}',
    b'[]',
])
def test_untrusted_bundle_rejected(bad):
    with pytest.raises(ValueError):
        from_json(bad)


def test_nested_unknown_fields_and_nonfinite_json_rejected():
    data = json.loads(to_json(Scenario(), {slot: None for slot in SLOTS}))
    data["active"]["hacker_setting"] = "bad"
    with pytest.raises(ValueError):
        from_json(json.dumps(data).encode())
    data["active"].pop("hacker_setting")
    data["active"]["volume_m3"] = float("nan")
    with pytest.raises(ValueError):
        from_json(json.dumps(data).encode())


def test_schema_refuses_partial_or_boolean_modules():
    source = asdict(Scenario())
    source["modules"] = False
    with pytest.raises(ValueError):
        from_mapping(source)
    source.pop("modules")
    with pytest.raises(ValueError):
        from_mapping(source)


def test_manager_and_router_start_with_six_other_pages():
    from streamlit.testing.v1 import AppTest
    app = AppTest.from_file(str(ROOT/"streamlit_app.py"),
                             default_timeout=75).run(timeout=75)
    assert not app.exception, [str(x.message) for x in app.exception]
    app.switch_page("pages/6_Scenario_Manager.py").run(timeout=75)
    assert not app.exception, [str(x.message) for x in app.exception]


def test_stage2_resource_cleanup_does_not_delete_essential_python():
    assert (ROOT/"engine/physics.py").exists()
    assert (ROOT/"engine/thermocline.py").exists()
    assert (ROOT/"engine/research_v2.py").exists()
    for name in ("RELEASE_NOTES_V1_STABLE.md",
                 "RELEASE_NOTES_V2.md", "RELEASE_NOTES_V22.md"):
        assert not (ROOT/"docs"/name).exists()
        assert (ROOT/"docs/archive"/name).exists()

def test_manager_slot_save_then_cross_page_navigation():
    from streamlit.testing.v1 import AppTest
    app = AppTest.from_file(str(ROOT/"streamlit_app.py"),
                             default_timeout=75).run(timeout=75)
    app.switch_page("pages/6_Scenario_Manager.py").run(timeout=75)
    assert not app.exception, [str(x.message) for x in app.exception]
    app.button(key="slot_save_A").click().run(timeout=75)
    assert not app.exception, [str(x.message) for x in app.exception]
    assert app.session_state["saved_scenarios"]["A"] == Scenario()
    app.switch_page("pages/4_Thermal_Design_Studio.py").run(timeout=75)
    assert not app.exception, [str(x.message) for x in app.exception]


def test_dashboard_outputs_portable_scenario_bundle_not_untrusted_results():
    home = (ROOT/"home_app.py").read_text(encoding="utf-8")
    assert "home_scenario_export" in home
    assert "to_json(current_scenario" in home
    assert "Export numerical results" in home


def test_research_lab_accepts_maximum_valid_renewable_source_power():
    high = Scenario(
        source="PV + wind", pv_mwp=200.0, pv_capacity_factor=0.6,
        wind_mw=200.0, wind_capacity_factor=0.75
    )
    high.validate()
    assert high.charge_power_mw() == pytest.approx(270.0)
    source = (ROOT/"pages/1_Engineering_Research_Lab.py").read_text(encoding="utf-8")
    assert 'st.number_input("Charging power (MW)",.2,300.' in source

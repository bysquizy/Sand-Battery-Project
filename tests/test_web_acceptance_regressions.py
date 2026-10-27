"""Interactive headless regressions; physical-browser acceptance remains separate."""
from dataclasses import replace
from pathlib import Path
from types import SimpleNamespace

import pytest
from streamlit.testing.v1 import AppTest

from engine.scenarios import MAX_IMPORT_BYTES, SLOTS, Scenario, to_json

ROOT = Path(__file__).resolve().parents[1]


def app():
    result = AppTest.from_file(str(ROOT / "streamlit_app.py"), default_timeout=75)
    result.run(timeout=75)
    assert not result.exception
    return result


def test_real_language_selector_preserves_workspace_and_saved_design():
    ui = app()
    ui.selectbox(key="demo_preset").set_value("Compact research study").run()
    ui.button(key="home_apply_preset").click().run()
    selected = ui.session_state["active_scenario"]
    ui.session_state["saved_scenarios"] = {"A": selected, "B": None, "C": None}
    ui.radio(key="home_workspace").set_value("Thermal Dynamics").run()
    for language in ("Türkçe", "English"):
        ui.selectbox(key="sb_language_select").set_value(language).run()
        assert not ui.exception
        assert ui.radio(key="home_workspace").value == "Thermal Dynamics"
        assert ui.session_state["active_scenario"] == selected
        assert ui.session_state["saved_scenarios"]["A"] == selected
    # AppTest reruns a switched page alone; exercise its stored-language input
    # separately from the actual router selector tested above.
    ui = AppTest.from_file(str(ROOT / "pages/8_Visual_Story_Studio.py"), default_timeout=75).run()
    ui.radio(key="visual_workspace").set_value("Engineering report").run()
    ui.session_state["sb_language"] = "tr"
    ui.run()
    assert not ui.exception
    assert ui.radio(key="visual_workspace").value == "Engineering report"
    assert any(button.label == "Görselli HTML raporunu indir" for button in ui.get("download_button"))


def test_all_ten_pages_start_via_turkish_router():
    for page in ["home_app.py", *sorted(str(p.relative_to(ROOT)) for p in (ROOT / "pages").glob("*.py"))]:
        ui = app()
        ui.selectbox(key="sb_language_select").set_value("Türkçe").run()
        if page != "home_app.py":
            ui.switch_page(page).run(timeout=75)
        assert not ui.exception, page
        assert ui.session_state["sb_language"] == "tr"


def test_uploader_uses_small_transport_ceiling_and_explains_validation():
    ui = app()
    ui.switch_page("pages/6_Scenario_Manager.py").run()
    assert ui.get("file_uploader")[0].proto.max_upload_size_mb == 1
    assert any("40,000 bytes" in item.value for item in ui.caption)


@pytest.mark.parametrize("payload", [b"invalid", b"x" * (MAX_IMPORT_BYTES + 1)])
def test_rejected_ui_import_preserves_current_work(monkeypatch, payload):
    import streamlit as st
    ui = app()
    original = ui.session_state["active_scenario"]
    ui.switch_page("pages/6_Scenario_Manager.py").run()
    ui.button(key="slot_save_A").click().run()
    monkeypatch.setattr(st, "file_uploader", lambda *args, **kwargs:
                        SimpleNamespace(size=len(payload), getvalue=lambda: payload))
    ui.run()
    assert not ui.exception
    assert ui.error
    assert ui.session_state["active_scenario"] == original
    assert ui.session_state["saved_scenarios"]["A"] == original


def test_active_only_import_warns_and_replaces_only_after_apply(monkeypatch):
    import streamlit as st
    ui = app()
    original = ui.session_state["active_scenario"]
    imported = replace(Scenario(), name="Restored study", volume_m3=500)
    payload = to_json(imported, {slot: None for slot in SLOTS}).encode()
    ui.switch_page("pages/6_Scenario_Manager.py").run()
    ui.button(key="slot_save_A").click().run()
    monkeypatch.setattr(st, "file_uploader", lambda *args, **kwargs:
                        SimpleNamespace(size=len(payload), getvalue=lambda: payload))
    ui.run()
    assert not ui.exception
    assert any("all A/B/C slots" in item.value for item in ui.warning)
    assert ui.session_state["active_scenario"] == original
    assert ui.session_state["saved_scenarios"]["A"] == original
    ui.button(key="manager_import_apply").click().run()
    assert not ui.exception
    assert ui.session_state["active_scenario"] == imported
    assert all(value is None for value in ui.session_state["saved_scenarios"].values())

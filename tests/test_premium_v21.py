"""v2.1 security, cross-page design and safe web presentation regressions."""
from __future__ import annotations

from dataclasses import replace
from pathlib import Path
import tomllib

import pandas as pd
import pytest

from engine.export_safety import csv_cell, safe_csv
from engine.scenarios import Scenario

ROOT=Path(__file__).resolve().parents[1]
PAGES=[
    "home_app.py",
    "pages/1_Engineering_Research_Lab.py",
    "pages/2_Material_Atlas.py",
    "pages/3_Virtual_Experiments.py",
    "pages/4_Thermal_Design_Studio.py",
    "pages/5_Project_Research_Library.py",
    "pages/6_Scenario_Manager.py",
    "pages/7_Model_Verification.py",
    "pages/8_Visual_Story_Studio.py",
]


@pytest.mark.parametrize("name", [
    "=HYPERLINK(\"https://example.test\",\"click\")",
    "+SUM(1,1)",
    "-2+3",
    "@SUM(1,1)",
    "   =cmd",
    "\t=1+1",
    "\ufeff@IMPORT",
])
def test_spreadsheet_injection_is_neutralized(name):
    assert csv_cell(name).startswith("'")
    text=safe_csv(pd.DataFrame({"Name":[name],"Energy":[42.5]}))
    assert name not in text.splitlines()[1][0:len(name)]


def test_csv_preserves_numeric_model_data_and_safe_strings():
    output=safe_csv(pd.DataFrame({
        "Scenario":["A", "=IMPORTXML('x','y')", "Thermal store"],
        "MWh":[1.0,2.5,4.0],
    }))
    assert "'=IMPORTXML" in output
    assert "2.5" in output
    assert "Thermal store" in output


def test_ribbon_html_escapes_scenario_names():
    from html import escape
    name="<img src=x onerror=alert(1)>"
    text=(ROOT/"scenario_state.py").read_text(encoding="utf-8")
    assert "escape(s.name)" in text
    assert escape(name) != name
    # Scenario names remain valid as model metadata; rendered output escapes.
    replace(Scenario(),name=name).validate()


def test_brand_system_is_static_no_js_and_reduced_motion():
    text=(ROOT/"ui_theme.py").read_text(encoding="utf-8")
    assert "prefers-reduced-motion" in text
    assert ":focus-visible" in text
    assert "escape(kicker)" in text and "escape(description)" in text
    assert "st.html(CSS)" in text
    assert "unsafe_allow_javascript" not in text
    assert "fonts.googleapis" not in text
    assert "<script" not in text


def test_streamlit_config_preserves_security_and_theme():
    config=tomllib.loads((ROOT/".streamlit/config.toml").read_text(encoding="utf-8"))
    assert config["theme"]["base"]=="dark"
    assert config["theme"]["sidebar"]["primaryColor"]
    assert config["server"]["enableCORS"] is True
    assert config["server"]["enableXsrfProtection"] is True


@pytest.mark.parametrize("path",PAGES)
def test_every_page_uses_premium_theme_and_provenance_footer(path):
    page=(ROOT/path).read_text(encoding="utf-8")
    assert "from ui_theme import inject" in page
    assert "hero(" in page
    assert "footer()" in page


def test_navigational_entry_still_registers_all_pages():
    source=(ROOT/"streamlit_app.py").read_text(encoding="utf-8")
    for page in PAGES:
        assert page in source
    assert "GitHub Repository" in source
    assert "Getting started" in source


def test_scenario_comparison_csv_does_not_trust_imported_text():
    source=(ROOT/"pages/6_Scenario_Manager.py").read_text(encoding="utf-8")
    assert "safe_csv(df)" in source


def test_full_multipage_startup_with_current_theme():
    from streamlit.testing.v1 import AppTest
    app=AppTest.from_file(str(ROOT/"streamlit_app.py"),default_timeout=75).run(timeout=75)
    assert not app.exception,[str(x.message) for x in app.exception]
    for page in PAGES[1:]:
        app.switch_page(page).run(timeout=75)
        assert not app.exception, f"{page}: {[str(x.message) for x in app.exception]}"

def test_offline_html_report_matches_brand_and_respects_accessibility():
    from engine.materials import MATERIALS
    from engine.physics import simulate_cycle
    from engine.report_exports import html_report
    scenario=Scenario()
    output=simulate_cycle(scenario.make_design(), MATERIALS[scenario.material_name])
    html=html_report(scenario,output).decode("utf-8")
    assert "prefers-reduced-motion" in html
    assert "@media print" in html
    assert "sb-chart-reveal" in html
    assert "sb-trace" in html
    assert "<script" not in html
    assert "fonts.googleapis.com" not in html
    assert "Group 8" in html

"""Regression checks for the bilingual interface and visual output.

Keep display translations separate from stable numerical data keys.
"""
from pathlib import Path
from types import SimpleNamespace

import pandas as pd

import localization
from visuals import timeline, material_comparison

ROOT = Path(__file__).resolve().parents[1]


def test_temperature_graph_works_in_both_languages(monkeypatch):
    sample = {
        "charge_trace_h": [0.0, 1.0, 2.0],
        "charge_trace_c": [50.0, 100.0, 150.0],
        "hold_trace_h": [2.0, 3.0, 4.0],
        "hold_trace_c": [150.0, 148.0, 146.0],
        "discharge_trace_h": [4.0, 5.0, 6.0],
        "discharge_trace_c": [146.0, 100.0, 50.0],
    }
    for lang, expected in [("tr", "Şarj"), ("en", "Charging")]:
        monkeypatch.setattr(
            localization, "st", SimpleNamespace(session_state={"sb_language": lang})
        )
        fig = timeline(sample)
        assert fig.data[0].name == expected
        assert len(fig.frames) == 25
        assert fig.layout.updatemenus[0].buttons[0].method == "animate"


def test_material_graph_preserves_data_schema(monkeypatch):
    monkeypatch.setattr(
        localization, "st", SimpleNamespace(session_state={"sb_language": "tr"})
    )
    data = pd.DataFrame([{"Material": "Silica sand", "Theoretical MWh": 2.5}])
    chart = material_comparison(data)
    assert chart.data[0].y[0] == "Silica sand"


def test_translation_calls_not_nested_and_formula_escapes_valid():
    checked = [ROOT / "home_app.py", ROOT / "visuals.py"]
    checked += list((ROOT / "pages").glob("*.py"))
    for path in checked:
        assert "tr(tr(" not in path.read_text(encoding="utf-8"), path.name
    guide = (ROOT / "pages/9_How_It_Works.py").read_text(encoding="utf-8")
    assert r"Q=m\int_{T_{\mathrm{low}}}^{T_{\mathrm{high}}}c_p(T)\,\mathrm{d}T" in guide
    assert "material.enthalpy(temp)-material.enthalpy(low)" in guide
    assert "mass*830*" not in guide


def test_turkish_pages_start_without_runtime_errors():
    from streamlit.testing.v1 import AppTest

    for page in ("home_app.py", "pages/5_Project_Research_Library.py",
                 "pages/8_Visual_Story_Studio.py", "pages/9_How_It_Works.py"):
        app = AppTest.from_file(str(ROOT / page), default_timeout=75)
        app.session_state["sb_language"] = "tr"
        app.run(timeout=75)
        assert not app.exception, f"{page}: {[str(e.message) for e in app.exception]}"


def test_display_translation_keeps_stable_source_keys(monkeypatch):
    """Turkish labels must never mutate saved JSON scenario source identifiers."""
    from engine.scenarios import Scenario, to_json

    monkeypatch.setattr(
        localization, "st", SimpleNamespace(session_state={"sb_language": "tr"})
    )
    assert localization.material_label("Silica sand") == "Silis kumu"
    assert localization.source_label("Electric heater") == "Elektrikli ısıtıcı"
    assert localization.preset_label("Compact research study") == "Kompakt araştırma örneği"
    saved = to_json(Scenario(), {"A": None, "B": None, "C": None})
    assert '"source": "Electric heater"' in saved
    assert '"material_name": "Silica sand"' in saved
    monkeypatch.setattr(
        localization, "st", SimpleNamespace(session_state={"sb_language": "en"})
    )
    assert localization.material_label("Silica sand") == "Silica sand"
    assert localization.source_label("Electric heater") == "Electric heater"
    # Selectbox option labels stay identical across language changes, avoiding
    # the widget-state mismatch seen when a form is open during EN/TR toggling.
    assert localization.material_option_label("Silica sand") == "Silica sand / Silis kumu"
    assert localization.source_option_label("Electric heater") == "Electric heater / Elektrikli ısıtıcı"
    assert "CSP" in localization.preset_option_label("CSP-assisted thermal storage")


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
    assert r"Q=m\,c_p\,\Delta T" in guide

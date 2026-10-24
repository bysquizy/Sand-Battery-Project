"""Research release identity, bibliography and reproducible export checks."""
import pytest
from project_info import PROJECT,REFERENCES,FIELD_REFERENCES,bibliography_text
from engine.materials import MATERIALS
from engine.physics import Design,simulate_cycle
from engine.reporting import scenario_markdown

def test_verified_claim_register():
    assert PROJECT["group"]=="Group 8"
    assert "İzmir Institute of Technology" in PROJECT["institution"]
    assert len(REFERENCES)>=6
    assert len({r["id"] for r in REFERENCES})==len(REFERENCES)
    assert all(r["url"].startswith("https://") for r in REFERENCES)
    assert FIELD_REFERENCES[0]["thermal_power_mw"]==pytest.approx(.2)
    assert FIELD_REFERENCES[0]["thermal_capacity_mwh"]==pytest.approx(8.)
    assert FIELD_REFERENCES[1]["thermal_power_mw"]==pytest.approx(1.)
    assert "Bošnjaković" in bibliography_text()

def test_scenario_markdown_report():
    d=Design(volume_m3=120.,charge_mw=1.,thermal_output_mw=.5)
    m=MATERIALS["Silica sand"]
    r=simulate_cycle(d,m)
    result=scenario_markdown(d,m,r)
    assert "120.0" in result
    assert "MWh" in result
    assert "@bysquizy" in result
    assert "unvalidated" in result

def test_web_entrypoint_with_streamlit_apptest():
    # Run inside GitHub Actions; exercises the full Streamlit script without browser rendering.
    from streamlit.testing.v1 import AppTest
    from pathlib import Path
    path=Path(__file__).resolve().parents[1]/"streamlit_app.py"
    app=AppTest.from_file(str(path),default_timeout=60).run(timeout=60)
    assert not app.exception, [str(e.message) for e in app.exception]

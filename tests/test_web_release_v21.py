"""Web-first release, source attribution and packaging regression tests."""
from pathlib import Path
from project_info import PROJECT, FIELD_REFERENCES, REFERENCES

ROOT=Path(__file__).resolve().parents[1]
PUBLIC="https://sand-battery-project-a5twmepge6cqbndgbz9jmj.streamlit.app/"

def test_public_url_is_real_user_supplied_site():
    assert PROJECT["public_app"] == PUBLIC
    assert PUBLIC in (ROOT/"README.md").read_text(encoding="utf-8")
    assert PUBLIC not in (ROOT/"streamlit_app.py").read_text(encoding="utf-8")

def test_operator_and_manufacturer_specs_are_separate():
    k=FIELD_REFERENCES[0]
    assert k["site"].startswith("Kankaanpää")
    assert k["thermal_power_mw"]==0.2
    assert k["operator_power_mw"]==0.1
    assert k["thermal_capacity_mwh"]==8.
    ref={r["id"]:r for r in REFERENCES}
    assert "vatajankoski" in ref and "kankaanpaa" in ref
    assert ref["vatajankoski"]["url"].startswith("https://www.vatajankoski.fi/")

def test_browser_only_app_has_no_local_launcher():
    assert not (ROOT/"start.bat").exists()
    requirements=(ROOT/"requirements.txt").read_text().strip().splitlines()
    assert len(requirements)==5
    assert all(not x.startswith(("torch","tensorflow","openai","transformers")) for x in requirements)

def test_model_source_docs_present():
    assert (ROOT/"docs/ADVANCED_RESEARCH_V2.md").exists()
    assert (ROOT/"docs/archive/RELEASE_NOTES_V2.md").exists()
    assert "illustrative" in (ROOT/"README.md").read_text().lower()
    assert "operator" in (ROOT/"pages/5_Project_Research_Library.py").read_text().lower()

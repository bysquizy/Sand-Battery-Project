"""v2.2 UI, attribution, packaging and web-navigation regression checks."""
from pathlib import Path
from project_info import MODEL_EVIDENCE, PROJECT

ROOT = Path(__file__).resolve().parents[1]


def test_shared_theme_across_all_pages():
    for name in (
        "home_app.py",
        "pages/1_Engineering_Research_Lab.py",
        "pages/2_Material_Atlas.py",
        "pages/3_Virtual_Experiments.py",
    ):
        content = (ROOT / name).read_text(encoding="utf-8")
        assert "from ui_theme import inject" in content, name
        assert "inject()" in content, name


def test_no_font_service_dependency_and_reduced_motion():
    theme = (ROOT / "ui_theme.py").read_text(encoding="utf-8")
    assert "prefers-reduced-motion" in theme
    assert ":focus-visible" in theme
    assert "fonts.googleapis.com" not in theme


def test_model_evidence_register():
    assert len(MODEL_EVIDENCE) >= 8
    for row in MODEL_EVIDENCE:
        assert row["method"] and row["sources"] and row["evidence"] and row["status"]
    assert any("NOT" in row["evidence"] for row in MODEL_EVIDENCE)


def test_grouped_web_navigation_and_onboarding():
    router = (ROOT / "streamlit_app.py").read_text(encoding="utf-8")
    assert 'st.navigation(pages, position="sidebar"' in router
    assert 't("advanced")' in router
    assert 't("research")' in router
    assert 't("pages")' in router
    assert PROJECT["public_app"] not in router


def test_presentation_presets_are_illustrative():
    content = (ROOT / "home_app.py").read_text(encoding="utf-8")
    presets = (ROOT / "engine/scenarios.py").read_text(encoding="utf-8")
    assert "Industrial thermal store" in presets
    assert "Compact research study" in presets
    assert "CSP-assisted thermal storage" in presets
    assert "not measured Finnish plants" in content
    assert "low_power_mode" in content


def test_dependency_isolation_and_attribution():
    req = (ROOT / "requirements.txt").read_text(encoding="utf-8")
    assert len(req.strip().splitlines()) == 5
    assert "ruff" not in req
    assert "ruff" in (ROOT / "requirements-dev.txt").read_text(encoding="utf-8")
    citation = (ROOT / "CITATION.cff").read_text(encoding="utf-8")
    assert "Yağız" in citation
    assert "LicenseRef-Proprietary" not in citation
    assert not (ROOT / "LICENSE").exists()


def test_first_page_preset_interaction():
    from streamlit.testing.v1 import AppTest
    app = AppTest.from_file(str(ROOT / "home_app.py"), default_timeout=75).run(timeout=75)
    assert not app.exception, [str(x.message) for x in app.exception]
    app.selectbox(key="demo_preset").set_value("Compact research study").run(timeout=75)
    assert not app.exception, [str(x.message) for x in app.exception]

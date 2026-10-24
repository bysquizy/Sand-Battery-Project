"""Release 1.0 startup and Cloud metadata-compatibility tests."""
from pathlib import Path

from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).resolve().parents[1]
TIMEOUT = 75


def test_cloud_home_import_with_missing_optional_source_register(monkeypatch):
    """Graceful page rendering if Streamlit briefly holds older project_info."""
    import project_info

    monkeypatch.delattr(project_info, "MODEL_EVIDENCE", raising=False)
    app = AppTest.from_file(str(ROOT / "home_app.py"), default_timeout=TIMEOUT).run(
        timeout=TIMEOUT
    )
    assert not app.exception, [str(x.message) for x in app.exception]


def test_full_router_home_and_all_registered_research_pages():
    """Test exactly how the deployed site enters and navigates pages."""
    app = AppTest.from_file(
        str(ROOT / "streamlit_app.py"), default_timeout=TIMEOUT
    ).run(timeout=TIMEOUT)
    assert not app.exception, [str(x.message) for x in app.exception]
    for page in (
        "pages/1_Engineering_Research_Lab.py",
        "pages/2_Material_Atlas.py",
        "pages/3_Virtual_Experiments.py",
    ):
        app.switch_page(page).run(timeout=TIMEOUT)
        assert not app.exception, [
            f"{page}: {x.message}" for x in app.exception
        ]
    # Streamlit registers the default page by the entrypoint script rather
    # than the underlying home_app.py file.
    app.switch_page("streamlit_app.py").run(timeout=TIMEOUT)
    assert not app.exception, [str(x.message) for x in app.exception]


def test_stable_label_and_live_website_are_documented():
    from project_info import PROJECT

    assert PROJECT["public_app"].startswith("https://")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert ("v1.0 Stable" in readme or "v1.1 Research Update" in readme)
    assert PROJECT["public_app"] in readme

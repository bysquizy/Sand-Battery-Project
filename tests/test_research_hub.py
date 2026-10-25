"""Research Hub release: attribution, concise team page and interaction smoke tests."""
from pathlib import Path
from project_info import PROJECT
from research_notes import TOPICS, AUDIT, REVIEW

ROOT=Path(__file__).resolve().parents[1]

def test_all_group_members_and_canonical_repository():
    assert PROJECT["group"]=="Group 8"
    assert PROJECT["members"]==("Yağız Topaç","Semih Cenk","Fatma Ovacık")
    assert PROJECT["team_size"]==len(PROJECT["members"])
    assert PROJECT["repository"]=="https://github.com/bysquizy/Sand-Battery-Project"

def test_research_notes_have_attributions_and_boundaries():
    assert len(TOPICS)==8
    assert len({entry["id"] for entry in TOPICS})==len(TOPICS)
    assert REVIEW["doi"].startswith("https://doi.org/")
    assert all(entry["summary"] and entry["section"] and entry["model"] and entry["limitation"] for entry in TOPICS)
    assert {"P1","P2","S1","S2","U"}==set(AUDIT["tiers"])
    assert "UNRESOLVED" in AUDIT["verdicts"]

def test_project_page_has_only_requested_member_profile():
    source=(ROOT/"pages/5_Project_Research_Library.py").read_text(encoding="utf-8")
    team_block=source.split("with group:",1)[1].split("st.divider()",1)[0]
    assert 'st.markdown("## Group 8")' in team_block
    assert 'PROJECT["members"]' in team_block
    for removed in ("COURSE_MILESTONES","academic_year","instructor","ESE101","advisor"):
        assert removed not in team_block
    assert "Date" not in team_block

def test_no_duplicated_research_and_team_tabs_on_dashboard():
    source=(ROOT/"home_app.py").read_text(encoding="utf-8")
    assert "with science:" not in source
    assert "with team:" not in source
    assert 'PROJECT["repository"]' in source
    assert "Research Hub" in source

def test_repository_link_and_research_navigation_present():
    router=(ROOT/"streamlit_app.py").read_text(encoding="utf-8")
    assert "GitHub Repository" in router
    assert 'title="Research Hub"' in router
    assert "Research & Sources" in router

def test_research_hub_opens_and_can_change_topic():
    from streamlit.testing.v1 import AppTest
    app=AppTest.from_file(str(ROOT/"pages/5_Project_Research_Library.py"),default_timeout=75).run(timeout=75)
    assert not app.exception, [str(e.message) for e in app.exception]
    topic=app.selectbox(key="hub_topic")
    topic.set_value(TOPICS[1]["label"]).run(timeout=75)
    assert not app.exception, [str(e.message) for e in app.exception]

def test_new_reference_summary_exists_in_docs():
    doc=(ROOT/"docs/RESEARCH_GUIDE.md").read_text(encoding="utf-8")
    assert "Bošnjaković" in doc
    assert "Kankaanpää" in doc and "Vatajankoski" in doc
    assert "UNRESOLVED" in doc

"""Sand Battery Studio — research-oriented, compact multipage navigation.

File-based pages are registered explicitly to work reliably on Streamlit Cloud.
"""
import streamlit as st
from scenario_state import sidebar_editor, active

pages = {
    "Simulation": [
        st.Page("home_app.py", title="Engineering Dashboard", icon="🏠", default=True),
        st.Page("pages/4_Thermal_Design_Studio.py", title="Thermal Design Studio", icon="📐"),
        st.Page("pages/6_Scenario_Manager.py", title="Scenario Manager", icon="🗂️"),
        st.Page("pages/7_Model_Verification.py", title="Model Verification", icon="📏"),
        st.Page("pages/8_Visual_Story_Studio.py", title="Visual Story Studio", icon="🎬"),
    ],
    "Advanced Research": [
        st.Page("pages/1_Engineering_Research_Lab.py", title="Advanced Research Lab", icon="🔬"),
        st.Page("pages/2_Material_Atlas.py", title="Material Atlas", icon="🧱"),
        st.Page("pages/3_Virtual_Experiments.py", title="Virtual Experiments", icon="🧪"),
    ],
    "Research & Sources": [
        st.Page("pages/5_Project_Research_Library.py", title="Research Hub", icon="📚"),
    ],
}
current = st.navigation(pages, position="sidebar", expanded=True)
with st.sidebar:
    st.html(
        '<div style="padding:14px 13px 12px;border-radius:15px;'
        'border:1px solid #385e69;background:linear-gradient(125deg,#193d44,#102431);'
        'margin:4px 0 15px">'
        '<div style="color:#72e9d1;letter-spacing:.18em;font-size:.67rem;'
        'font-weight:800">GROUP 8 · RESEARCH SOFTWARE</div>'
        '<div style="color:#f4fafc;font-size:1.19rem;font-weight:800;'
        'letter-spacing:-.03em;margin-top:5px">Sand Battery Studio</div>'
        '<div style="color:#c5d7df;font-size:.75rem;margin-top:4px">'
        'Physics · Design · Evidence</div></div>'
    )
sidebar_editor()
with st.sidebar:
    st.caption("Active model: " + active().name)
    with st.expander("Getting started · platform guide", expanded=False):
        st.markdown(
            "**01 · Dashboard:** Start with 0-D charging, losses and outputs.\n\n"
            "**02 · Design Studio:** Compare envelope insulation and module sizing.\n\n"
            "**03 · Scenarios:** Save, compare and restore A/B/C designs.\n\n"
            "**04 · Model Verification:** Inspect 0-D/1-D and idealized closed-pipe limits.\n\n"
            "**05 · Visual Story:** Animate calculated axial states and export reports.\n\n"
            "**06 · Advanced Research:** Explore LTNE, renewables, exergy and costs.\n\n"
            "**07 · Material Atlas:** Compare material assumptions and heat capacity.\n\n"
            "**08 · Virtual Experiments:** Run numerical grid/loss/Ergun checks.\n\n"
            "**09 · Research Hub:** Review sourced methods, field claims and Group 8.\n\n"
            "**Important:** This is a simulation-only academic application, not measured equipment."
        )
    st.link_button("GitHub Repository · Source & Methods",
                   "https://github.com/bysquizy/Sand-Battery-Project",
                   width="stretch")
    st.link_button("Open the live platform",
                   "https://sand-battery-project-a5twmepge6cqbndgbz9jmj.streamlit.app/",
                   width="stretch")
current.run()

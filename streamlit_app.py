"""Sand Battery Studio — browser-first research platform routing.

All four pages are registered explicitly to prevent Cloud page-link errors.
"""
import streamlit as st

pages = [
    st.Page("home_app.py", title="Dashboard", icon="🏠", default=True),
    st.Page("pages/1_Engineering_Research_Lab.py", title="Engineering Research Lab", icon="🔬"),
    st.Page("pages/2_Material_Atlas.py", title="Material Atlas", icon="🧱"),
    st.Page("pages/3_Virtual_Experiments.py", title="Virtual Experiments", icon="🧪"),
]
pg = st.navigation(pages, position="sidebar")
with st.sidebar:
    st.caption("IZTECH · ENERGY SYSTEMS ENGINEERING · ESE101 / GROUP 8")
    st.link_button("🌐 Public web application", "https://sand-battery-project-a5twmepge6cqbndgbz9jmj.streamlit.app/", use_container_width=True)
    st.link_button("⌘ GitHub source & documentation", "https://github.com/bysquizy/Sand-Battery-Project", use_container_width=True)
pg.run()

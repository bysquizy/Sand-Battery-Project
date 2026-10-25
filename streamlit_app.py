"""Sand Battery Studio — research-oriented, compact multipage navigation.

File-based pages are registered explicitly to work reliably on Streamlit Cloud.
"""
import streamlit as st

pages = {
    "Simulation": [
        st.Page("home_app.py", title="Engineering Dashboard", icon="🏠", default=True),
        st.Page("pages/4_Thermal_Design_Studio.py", title="Thermal Design Studio", icon="📐"),
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
    st.caption("SAND BATTERY STUDIO · GROUP 8")
    with st.expander("Getting started", expanded=False):
        st.markdown(
            "**01 · Dashboard:** Start with the 0-D charge/hold/discharge calculation.\n\n"
            "**02 · Thermal Design:** Compare cooling curves, modules and insulation.\n\n"
            "**03 · Advanced Research:** Explore optional 1-D, heat exchanger, and uncertainty studies.\n\n"
            "**04 · Material Atlas:** Understand property assumptions and material comparisons.\n\n"
            "**05 · Research Hub:** Read the source summaries, key equations, evidence quality and reference links.\n\n"
            "**Important:** This is a simulation-only academic application, not measured equipment."
        )
    st.link_button("GitHub Repository ↗",
                   "https://github.com/bysquizy/Sand-Battery-Project",
                   width="stretch")
    st.link_button("Live web platform ↗",
                   "https://sand-battery-project-a5twmepge6cqbndgbz9jmj.streamlit.app/",
                   width="stretch")
current.run()

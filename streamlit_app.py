"""Sand Battery Studio — lightweight, grouped research navigation.

Every page remains on the existing Streamlit-hosted Python backend.
"""
import streamlit as st

pages = {
    "Simulation": [
        st.Page("home_app.py", title="Engineering Dashboard", icon="🏠", default=True),
    ],
    "Research & Comparison": [
        st.Page("pages/1_Engineering_Research_Lab.py", title="Advanced Research Lab", icon="🔬"),
        st.Page("pages/2_Material_Atlas.py", title="Material Atlas", icon="🧱"),
    ],
    "Model Verification": [
        st.Page("pages/3_Virtual_Experiments.py", title="Virtual Experiments", icon="🧪"),
    ],
}
current = st.navigation(pages, position="sidebar", expanded=True)
with st.sidebar:
    st.caption("IZTECH · ENERGY SYSTEMS ENGINEERING · ESE101 / GROUP 8")
    with st.expander("How to use this simulator", expanded=False):
        st.markdown(
            "**1.** Start with the Engineering Dashboard and choose a design.\n\n"
            "**2.** Run optional 1-D or LTNE experiments only when needed.\n\n"
            "**3.** Compare illustrative media and their assumptions in Material Atlas.\n\n"
            "**4.** Review the Evidence Library before citing numerical results.\n\n"
            "**Important:** No experimental measurements or certified equipment behavior are simulated."
        )
    st.link_button("Open public web application ↗",
                   "https://sand-battery-project-a5twmepge6cqbndgbz9jmj.streamlit.app/",
                   use_container_width=True)
    st.link_button("GitHub source & citations ↗",
                   "https://github.com/bysquizy/Sand-Battery-Project",
                   use_container_width=True)
current.run()

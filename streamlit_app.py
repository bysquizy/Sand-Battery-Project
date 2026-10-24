"""Sand Battery Studio — explicit, Cloud-safe multipage entry point.

The complete v2 dashboard is in home_app.py; research models and visualizations
remain in their existing modules. Route registration happens once per session.
"""
import streamlit as st

pages = [
    st.Page("home_app.py", title="Dashboard", icon="🏠", default=True),
    st.Page("pages/1_Engineering_Research_Lab.py", title="Engineering Research Lab", icon="🔬"),
    st.Page("pages/2_Material_Atlas.py", title="Material Atlas", icon="🧱"),
    st.Page("pages/3_Virtual_Experiments.py", title="Virtual Experiments", icon="🧪"),
]
st.navigation(pages, position="sidebar").run()

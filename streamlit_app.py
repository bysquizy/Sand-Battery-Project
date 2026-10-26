"""Sand Battery student project navigation with bilingual controls."""
import streamlit as st
from localization import t, tr
from scenario_state import sidebar_editor, active

with st.sidebar:
    st.selectbox("Dil / Language", ["English", "Türkçe"], placeholder=None, index=1 if st.session_state.get("sb_language")=="tr" else 0,
                 key="sb_language_select", on_change=lambda: st.session_state.update(
                     sb_language="tr" if st.session_state["sb_language_select"]=="Türkçe" else "en"))
    st.session_state["sb_language"] = "tr" if st.session_state["sb_language_select"] == "Türkçe" else "en"

pages = {
    t("simulation"): [
        st.Page("home_app.py", title=t("dashboard"), icon="🏠", default=True),
        st.Page("pages/9_How_It_Works.py", title=t("how"), icon="❔"),
        st.Page("pages/4_Thermal_Design_Studio.py", title=t("design"), icon="📐"),
        st.Page("pages/6_Scenario_Manager.py", title=t("scenarios"), icon="🗂️"),
        st.Page("pages/7_Model_Verification.py", title=t("verification"), icon="📏"),
        st.Page("pages/8_Visual_Story_Studio.py", title=t("visuals"), icon="🎬"),
    ],
    t("advanced"): [
        st.Page("pages/1_Engineering_Research_Lab.py", title=t("laboratory"), icon="🔬"),
        st.Page("pages/2_Material_Atlas.py", title=t("materials"), icon="🧱"),
        st.Page("pages/3_Virtual_Experiments.py", title=t("experiments"), icon="🧪"),
    ],
    t("research"): [
        st.Page("pages/5_Project_Research_Library.py", title=t("research_hub"), icon="📚"),
    ],
}
current = st.navigation(pages, position="sidebar", expanded=True)
with st.sidebar:
    st.markdown("### Sand Battery Project")
    st.caption(t("intro"))
sidebar_editor()
with st.sidebar:
    st.caption(t("active") + ": " + active().name)
    with st.expander(t("pages"), expanded=False):
        st.markdown(tr(
            "Dashboard: heat storage and losses. Design: insulation and geometry. Scenarios: compare settings. Verification: numerical assumptions. Visuals: graphs and exports. Research: sources and methods.",
            "Panel: depolama ve ısı kayıpları. Tasarım: yalıtım ve geometri. Senaryolar: ayarları karşılaştırın. Doğrulama: sayısal varsayımlar. Görseller: grafik ve raporlar. Araştırma: kaynaklar ve yöntemler."
        ))
    st.link_button("⌘ " + t("github"), "https://github.com/bysquizy/Sand-Battery-Project", width="stretch")
    st.caption(tr("Project team: Yağız Topaç · Semih Cenk · Fatma Ovacık","Proje ekibi: Yağız Topaç · Semih Cenk · Fatma Ovacık"))
    st.caption(tr("Website & application development: Yağız Topaç (@bysquizy)","Web sitesi ve uygulama geliştirme: Yağız Topaç (@bysquizy)"))
current.run()

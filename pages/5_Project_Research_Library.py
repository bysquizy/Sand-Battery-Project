"""Sand Battery Studio Research Hub — concise, sourced educational briefs."""
from __future__ import annotations
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from project_info import PROJECT, FIELD_REFERENCES, REFERENCES, MODEL_EVIDENCE, bibliography_text
from research_notes import TOPICS, REVIEW, AUDIT, SOURCE_NOTES
from ui_theme import inject

st.set_page_config(page_title="Research Hub | Sand Battery Studio",page_icon="📚",layout="wide")
inject()
st.caption("SAND BATTERY STUDIO  /  SCIENTIFIC RESEARCH")
st.title("Research Hub")
st.write("Understand the engineering concepts behind the simulations, review their limitations and inspect the original sources.")
st.link_button("View this project's GitHub repository",PROJECT["repository"],type="primary")
st.caption("Educational research summaries based on the supplied technical review, manufacturer notes and source-quality audit. No laboratory calibration has been performed.")

guide,methods,case_studies,sources,group=st.tabs([
    "Research guide","Methods & evidence","Real-world systems","Sources & references","Group 8"
])

with guide:
    st.markdown("### Start with the science")
    st.write("The technical review organizes sand thermal energy storage around how energy is charged, stored and discharged, how heat moves, and what makes a design practical.")
    a,b,c=st.columns(3)
    a.metric("Operating phases","3")
    b.metric("Research themes",str(len(TOPICS)))
    c.metric("Source categories",str(len({r["group"] for r in REFERENCES})))
    st.markdown("#### The thermal-energy pathway")
    phase=st.radio("Explore one phase",["Charging","Standby","Thermal delivery"],horizontal=True,key="hub_phase")
    details={
        "Charging":("Renewable/grid electricity or a specified solar-thermal input supplies heat. Input power, heater/optical efficiency and temperature limits matter.","Input energy is not automatically recoverable thermal energy."),
        "Standby":("Stored heat declines because the medium loses energy across the insulation and outer surfaces. Geometry and ambient conditions matter.","A high capacity does not imply negligible long-duration loss."),
        "Thermal delivery":("Useful thermal energy is transferred to a consumer through the selected heat-transfer system; temperature grade and exchanger limitations matter.","The web model assumes simplified output constraints, not a certified delivery temperature."),
    }
    with st.container(border=True):
        st.markdown(f"**{phase}**")
        st.write(details[phase][0])
        st.caption(details[phase][1])
    sank=go.Figure(go.Sankey(
        node=dict(label=["Heat source","Storage medium","Useful process heat","Conversion & ambient losses"],
                  pad=28,thickness=18,color=["#69aacd","#eeb37e","#58dfc3","#bc7980"]),
        link=dict(source=[0,0,1,1],target=[1,3,2,3],value=[75,25,57,18],
                  color=["rgba(238,179,126,.38)","rgba(191,120,128,.3)","rgba(88,223,195,.38)","rgba(191,120,128,.23)"])))
    sank.update_layout(template="plotly_dark",height=270,margin=dict(l=5,r=5,t=15,b=5),
                       paper_bgcolor="rgba(0,0,0,0)",font=dict(color="#edf3f7",size=12))
    st.plotly_chart(sank,width="stretch",key="hub_flow_diagram")
    st.caption("Conceptual Sankey proportions are decorative illustrations, NOT measured energy fractions. Use Dashboard for calculated balances.")

    st.markdown("### Explore research themes")
    lookup={t["label"]:t for t in TOPICS}
    choose=st.selectbox("Choose a topic",list(lookup),key="hub_topic")
    t=lookup[choose]
    with st.container(border=True):
        st.caption(f"Reading location: {t['section']} · Bošnjaković & Santa (2026)")
        st.markdown(f"#### {t['label']}")
        st.write(t["summary"])
        st.markdown("**Essential takeaways**")
        for item in t["key_points"]:
            st.markdown(f"- {item}")
        st.markdown(f"**Where it appears in the application:** {t['model']}")
        st.info(f"**Important boundary:** {t['limitation']}")
        st.code(t["equation"],language="text")
        st.link_button("Read the research review",REVIEW["doi"])
    st.markdown("#### All eight topics at a glance")
    for t in TOPICS:
        with st.expander(f"{t['label']}  ·  {t['section']}",expanded=False):
            st.write(t["summary"])
            st.caption("Application: "+t["model"])
            st.caption("Limitation: "+t["limitation"])

with methods:
    st.markdown("### What each equation can support")
    st.write("The simulator implements physical relationships and simplified numerical boundaries. Cite the method and verify the input data separately.")
    rows=pd.DataFrame(MODEL_EVIDENCE)
    st.dataframe(rows,hide_index=True,width="stretch",height=400)
    st.download_button("Download equations and evidence · CSV",rows.to_csv(index=False),
        file_name="research_method_register.csv",mime="text/csv",key="hub_methods_dl")
    col1,col2=st.columns(2)
    with col1:
        st.markdown("#### Thermal capacity")
        st.latex(r"Q=\rho_{bulk}V\int_{T_{min}}^{T_{max}}c_p(T)\,dT")
        st.caption("Theoretical sensible energy; material cp(T) is an illustrative input unless measured.")
        st.markdown("#### Mean-temperature balance")
        st.latex(r"m c_p(T)\frac{dT}{dt}=P_{charge}-P_{out}-UA(T-T_a)")
        st.caption("0-D approximation, not a certified geometry-specific thermal field.")
    with col2:
        st.markdown("#### Thermodynamic exergy")
        st.latex(r"X=m\int c_p(T)\left(1-\frac{T_0}{T}\right)dT")
        st.caption("Absolute temperatures in kelvin; exergy is not electricity actually produced.")
        st.markdown("#### Heat-exchanger effectiveness")
        st.latex(r"Q=\varepsilon C_{min}(T_{h,in}-T_{c,in})")
        st.caption("Standalone steady-state ε–NTU illustration; not a coupled validated exchanger.")
    st.warning("Temperature-dependent cp(T) does not eliminate uncertainty. The built-in quartz illustration does NOT model the ~573 °C phase transition.")
    st.markdown("### Unvalidated features and missing evidence")
    st.markdown("No measured 3-D temperature data, live sensors, construction-grade finite-element stresses, verified monetary CAPEX, or power-to-electricity round-trip results are claimed. Code tests verify numerical behavior, not physical agreement.")

with case_studies:
    st.markdown("### Commercial installations — attributed statements")
    c1,c2=st.columns(2)
    with c1:
        with st.container(border=True):
            st.markdown("#### Kankaanpää, Finland")
            st.metric("Published storage capacity","8 MWh(th)")
            st.write("**Rated thermal power is inconsistent across published sources:**")
            st.markdown("**100 kW(th)** — utility operator Vatajankoski")
            st.markdown("**200 kW(th)** — technology provider Polar Night Energy")
            st.caption("The source disagreement is unresolved. Do not use these descriptions as matched experimental time-series data.")
            st.link_button("Utility operator source","https://www.vatajankoski.fi/en/projects/sand-battery/")
            st.link_button("Developer source","https://polarnightenergy.com/reference/worlds-first-sand-battery/")
    with c2:
        with st.container(border=True):
            st.markdown("#### Pornainen, Finland")
            st.metric("Manufacturer storage specification","100 MWh(th)")
            st.metric("Manufacturer rated thermal output","1 MW(th)")
            st.write("Reported industrial medium: crushed soapstone.")
            st.caption("Manufacturer-stated plant parameters only; not a physical-validation dataset for this app.")
            st.link_button("Developer's installation report","https://polarnightenergy.com/reference/solution-for-clean-energys-big-problem/")
    with st.container(border=True):
        st.markdown("#### NREL: a distinct particle storage concept")
        st.write("NREL report 84728 discusses a particular high-purity silica particle sample, and gives material-specific measurements rather than universal numbers for all sand or crushed aggregates.")
        st.warning("Do not treat NREL modeled retention, or a different packed-bed prototype, as measured thermal efficiency of our Streamlit simulator.")
        st.link_button("NREL report 84728", "https://www.nrel.gov/docs/fy23osti/84728.pdf")
    st.caption("Each external statement is tagged by source type. Commercial capacity and rated power are not a calibration dataset and cannot validate thermal transients.")

with sources:
    st.markdown("### Your research material, organized")
    for item in SOURCE_NOTES:
        with st.expander(item["title"],expanded=item["title"]=="2026 research review"):
            st.write(f"**Evidence class:** {item['class']}")
            st.write("**Supports:** "+item["supports"])
            st.caption("Does not establish: "+item["not_valid"])
            if item["url"]:
                st.link_button("Open external original source",item["url"])
    st.divider()
    st.markdown("### Source-quality terminology")
    st.write(AUDIT["meaning"])
    col1,col2=st.columns(2)
    with col1:
        st.markdown("**Provenance tiers**")
        for key,val in AUDIT["tiers"].items():
            st.markdown(f"**{key}** — {val}")
    with col2:
        st.markdown("**Audit verdicts**")
        for key,val in AUDIT["verdicts"].items():
            st.markdown(f"**{key}** — {val}")
    st.divider()
    st.markdown("### Search the bibliography")
    groups=["All categories"]+list(dict.fromkeys(r["group"] for r in REFERENCES))
    a,b=st.columns([1,2])
    with a:selected=st.selectbox("Reference category",groups,key="hub_ref_cat")
    with b:query=st.text_input("Search papers, institutions or claims",key="hub_ref_search",placeholder="e.g. NREL or LTNE")
    matching=[r for r in REFERENCES if (selected=="All categories" or r["group"]==selected) and
              (not query or query.lower() in (r["apa"]+" "+r["claim"]+" "+r["id"]).lower())]
    st.caption(f"{len(matching)} references")
    for ref in matching:
        with st.expander(f"{ref['id'].replace('-',' ').title()} · {ref['type']}"):
            st.markdown(ref["apa"])
            st.write("**Supports:** "+ref["claim"])
            st.markdown(f"[Original link]({ref['url']})")
    st.download_button("Export APA bibliography",bibliography_text(),file_name="Sand_Battery_References.txt",
                       mime="text/plain",key="hub_bibliography_export")

with group:
    st.markdown("## Group 8")
    for member in PROJECT["members"]:
        with st.container(border=True):
            st.markdown(f"**{member}**")

st.divider()
st.caption("Research summaries are source-grounded interpretations. The site presents a numerical study, not a physical test report.")

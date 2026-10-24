"""Project and Research Library — source-transparent university research portal.

Claims are grouped by provenance, not presented as experimental validation.
"""
from __future__ import annotations
import pandas as pd
import streamlit as st
from project_info import (PROJECT, REFERENCES, FIELD_REFERENCES,
                          COURSE_MILESTONES, MODEL_EVIDENCE, bibliography_text)
from ui_theme import inject

st.set_page_config(page_title="Project & Research Library | Sand Battery Studio",
                   page_icon="📚",layout="wide")
inject()

st.markdown('<div class="eyebrow">IZTECH · ESE101 GROUP 8 · RESEARCH DOCUMENTATION</div>',unsafe_allow_html=True)
st.title("Project & Research Library")
st.write("Academic identity, the original research trail, the governing equations and the limits of our simulation.")
st.warning("This is a student-led, simulation-only research project. It is not an official IZTECH service, manufacturer product, instrumented laboratory experiment or certified industrial design.")

about,methods,plants,library=st.tabs([
    "01 · Project & Team","02 · Models & Equations",
    "03 · Real Installations","04 · References & Sources"
])

with about:
    st.markdown("### An energy-systems engineering research initiative")
    a,b,c=st.columns(3)
    a.metric("Course","ESE101")
    b.metric("Project group","08")
    c.metric("Team size","3 students")
    st.markdown(f"**University:** {PROJECT['institution']}")
    st.markdown(f"**Department:** {PROJECT['department']}")
    st.markdown(f"**Academic period:** {PROJECT['academic_year']}")
    left,right=st.columns([1.1,1])
    with left:
        st.markdown("#### Research mission")
        st.write("Develop a transparent, browser-based environment for analyzing industrial-scale sensible heat storage. Explore charging, standby heat loss, output-energy constraints, material assumptions, design geometry, and numerical verification with reproducible calculations.")
        st.markdown("#### What the models can do")
        st.markdown("""
- Calculate theoretical thermal storage capacity with temperature-dependent illustrative cp(T).
- Simulate a 0-D thermal charge–hold–discharge cycle and energy ledger.
- Explore 1-D LTE/LTNE direct-contact numerical scenarios and ideal heat exchanger/flow studies.
- Compare materials, source assumptions, insulation and geometry under explicit constraints.
- Export scenario results for transparent ESE101 research discussion.
""")
    with right:
        st.markdown("#### Researchers and ownership")
        st.markdown(f"**Project developer:** {PROJECT['lead_name']} · [@bysquizy](https://github.com/bysquizy)")
        st.markdown("**Group 8:** Three students in total. Two contributor names have not been provided and will not be invented.")
        st.markdown("**Instructor/advisor:** Not specified; explicit confirmation pending.")
        st.caption("Independent student research at IZTECH; no institutional endorsement claimed.")
        st.link_button("GitHub — source and documentation ↗","https://github.com/bysquizy/Sand-Battery-Project")
        st.link_button("Open Sand Battery Studio ↗",PROJECT["public_app"])
    st.divider()
    st.markdown("#### ESE101 academic milestones")
    st.dataframe(pd.DataFrame(COURSE_MILESTONES,columns=["Date","Tentative milestone"]),
                 hide_index=True,width="stretch")
    st.caption("Dates came from the supplied tentative course calendar. Check official course announcements for revisions.")
    st.markdown("#### Academic integrity and AI disclosure")
    st.info("The team reports receiving verbal permission from its instructor for AI-assisted coding. The general course information sheet is more restrictive; the team is responsible for confirming the scope and disclosing authorized assistance in any assessed work.")

with methods:
    st.markdown("### Traceable mathematical foundations")
    st.caption("Every model should have an equation, numerical assumption, evidence role and limitation. A citation supports methodology, not automatically the selected numerical parameters.")
    df=pd.DataFrame(MODEL_EVIDENCE)
    st.dataframe(df,hide_index=True,width="stretch",height=420)
    st.download_button("Download method–evidence traceability CSV",df.to_csv(index=False),
                       mime="text/csv",file_name="method_evidence_map.csv",key="p_methods_csv")
    st.divider()
    exp=st.expander("Core governing relations",expanded=True)
    with exp:
        a,b=st.columns(2)
        with a:
            st.latex(r"Q_{th}=\rho_{bulk}V\int_{T_{min}}^{T_{max}}c_p(T)\,dT")
            st.caption("Theoretical sensible heat; cp(T) and density are illustrative unless tied to measurements.")
            st.latex(r"\dot Q_{loss}=UA\,(T-T_{amb})")
            st.caption("0-D heat leak for the chosen approximate insulation geometry.")
            st.latex(r"V_{target}=\frac{Q_{target}}{\rho_{bulk}\int c_p(T)\,dT}")
            st.caption("Volume estimate, NOT delivered energy or a dimensioned construction drawing.")
        with b:
            st.latex(r"m c_p(T)\frac{dT}{dt}=P_{in}-P_{out}-UA(T-T_{amb})")
            st.caption("Transient mean solid temperature; no heat-exchanger pinch or structural model.")
            st.latex(r"X=m\int_{T_{min}}^{T_{max}} c_p(T)\left(1-\frac{T_0}{T}\right)\,dT")
            st.caption("Exergy upper bound, with absolute Kelvin temperatures; not electricity generation.")
            st.latex(r"\Delta P/L=\frac{150\mu(1-\epsilon)^2u}{\epsilon^3d_p^2}+\frac{1.75\rho(1-\epsilon)u^2}{\epsilon^3d_p}")
            st.caption("Ergun relation applies to a direct-contact packed-bed study, not embedded hot-air pipes.")
    st.markdown("#### Critical engineering exclusions")
    st.warning("No measured material DSC data has been fitted, the quartz α–β transition near 573 °C is NOT captured by the linear cp(T) illustration, and the LTNE direct-contact model is not the commercial closed-pipe topology. Do not infer efficiency, durability, plant certification or investment feasibility.")
    st.markdown("[Research methods and scientific limitations](https://github.com/bysquizy/Sand-Battery-Project/blob/main/docs/ADVANCED_RESEARCH_V2.md)")

with plants:
    st.markdown("### Verified reference descriptions — not model validation")
    st.caption("Reference performance is reproduced with attribution to the original operator or developer. These numbers are not independently measured by our project.")
    a,b=st.columns(2)
    with a:
        st.markdown("#### Kankaanpää, Finland (2022)")
        st.metric("Published storage capacity","8 MWh(th)")
        st.markdown("**Nominal thermal power: source discrepancy**")
        st.markdown("- Vatajankoski utility operator: **100 kW(th)**.")
        st.markdown("- Polar Night Energy system developer: **200 kW(th)**.")
        st.caption("The sources differ. Their definitions or measurement conditions are not independently reconciled.")
        st.link_button("Vatajankoski operator record ↗","https://www.vatajankoski.fi/en/projects/sand-battery/")
        st.link_button("Polar Night Energy developer record ↗","https://polarnightenergy.com/reference/worlds-first-sand-battery/")
    with b:
        st.markdown("#### Pornainen, Finland (2025)")
        st.metric("Manufacturer-described thermal capacity","100 MWh(th)")
        st.metric("Manufacturer-described thermal power","1 MW(th)")
        st.markdown("**Reported medium:** crushed soapstone.")
        st.caption("The published operating plant is a field reference, not a calibration dataset for the software.")
        st.link_button("Polar Night Energy commissioning report ↗",
                       "https://polarnightenergy.com/news/worlds-largest-sand-battery-now-in-operation/")
    st.divider()
    st.markdown("#### NREL silica-sand particle example")
    st.markdown("An NREL research report describes a specific high-purity silica sand with **1,543 kg/m³ bulk density** and measured heat-capacity variation including the quartz inversion near **573 °C**. Those measurements have NOT been substituted for the application's inherited example material coefficients.")
    st.link_button("Read NREL report 84728 ↗","https://www.nrel.gov/docs/fy23osti/84728.pdf")
    st.caption("Different equipment and particle properties mean material/density values should not be transferred blindly.")

with library:
    st.markdown("### Literature, documents and source-confidence trail")
    st.write("This page brings together the sources behind the research, while separating external publisher evidence from the team's own exploratory models.")
    st.markdown("#### Original files supplied to the project")
    st.markdown("""
- **Sand Batteries for Thermal Energy Storage: A Review of Operating Principles, Technologies, Challenges and Future Perspectives** — the submitted full Bošnjaković & Santa (2026) review; used for research scope, technology classes and limitations.
- **Sand Battery Research — Polar Night Energy** — team-assembled manufacturer statements about charging, applications, system boundaries and demonstration installations; treated as company claims.
- **Sand Battery Source Check — Enhanced Research Audit** — team-provided source-quality assessment using P1/P2/S1/S2/U provenance tiers and MATCH/QUALIFY/MISATTRIBUTED/CONTRADICTED/NOT LOCATED/UNRESOLVED verdicts.
- **Legacy sand-battery Streamlit ZIP** — used to identify engineering workflow ideas such as cooling, modularity, design sizing and visual comparisons. Its outputs are not a scientific measurement dataset.
""")
    st.caption("These descriptions summarize the supplied documents; copyrighted full articles are not republished in this public repository.")
    st.markdown("#### Reference bibliography")
    categories=["All"]+list(dict.fromkeys(x["group"] for x in REFERENCES))
    c1,c2=st.columns([1,2])
    with c1:
        category=st.selectbox("Evidence category",categories,key="portal_category")
    with c2:
        query=st.text_input("Filter titles, claims or sources",placeholder="e.g. NREL, thermal storage, university",key="portal_query")
    refs=[r for r in REFERENCES if (category=="All" or r["group"]==category)
          and (not query or query.lower() in (r["apa"]+" "+r["claim"]+" "+r["group"]).lower())]
    st.caption(f"{len(refs)} references match the selected filters.")
    for r in refs:
        with st.expander(f"{r['id'].replace('-',' ').title()} · {r['type']}",expanded=False):
            st.markdown(r["apa"])
            st.markdown(f"**Claim or method it supports:** {r['claim']}")
            st.caption(f"Provenance group: {r['group']}")
            st.markdown(f"[Read original source ↗]({r['url']})")
    st.download_button("Download APA-style bibliography · TXT",bibliography_text(),
                       mime="text/plain",file_name="Sand_Battery_APA_References.txt",key="portal_apa")
    st.markdown("#### Source-audit rules")
    st.info("P1/P2 indicate source provenance and original-company records; they do not mean a simulator is experimentally calibrated. 'UNRESOLVED' is retained where original sources disagree. Review audit context before attributing engineering or financial performance.")
    st.link_button("Repository methods and audit register ↗",
                    "https://github.com/bysquizy/Sand-Battery-Project/blob/main/docs/SOURCE_REGISTER.md")

st.divider()
st.caption("Sand Battery Studio · Independent IZTECH ESE101 Group 8 research · Yağız Topaç · Engineering interpretation requires source-specific model boundaries.")

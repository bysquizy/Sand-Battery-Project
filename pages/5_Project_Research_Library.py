"""Sand Battery Studio Research Hub — concise, sourced educational briefs."""
from __future__ import annotations
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from project_info import PROJECT, REFERENCES, MODEL_EVIDENCE, bibliography_text
from research_notes import TOPICS, REVIEW, AUDIT, SOURCE_NOTES
from ui_theme import inject, hero, footer
from localization import t, tr

st.set_page_config(page_title="Research Hub | Sand Battery Studio",page_icon="📚",layout="wide")
inject()
hero(tr("KNOWLEDGE / SOURCES","BİLGİ / KAYNAKLAR"), t("research_hub"), tr("Explore research, equations and attributed real-world systems behind the simulations.","Simülasyonun dayandığı araştırmaları, denklemleri ve gerçek sistemlere ait kaynakları inceleyin."))
st.write(tr("Understand the engineering concepts and limitations behind the simulations.","Simülasyonların mühendislik kavramlarını ve sınırlamalarını öğrenin."))
st.link_button("View this project's GitHub repository",PROJECT["repository"],type="primary")
st.caption(tr("Literature-based educational summaries; no laboratory calibration.","Bilimsel kaynaklara dayalı eğitim özeti; laboratuvar kalibrasyonu yapılmadı."))

guide,methods,case_studies,sources,group=st.tabs([
    tr("Research guide","Araştırma rehberi"),tr("Methods & evidence","Yöntemler ve kanıtlar"),tr("Real-world systems","Gerçek sistemler"),tr("Sources & references","Kaynakça"),tr("Group 8","Grup 8")
])

with guide:
    st.markdown(tr("### Start with the science","### Temel prensipler"))
    st.write(tr("The technical review examines charging, storage, discharge and practical design.","Teknik inceleme şarj, depolama, deşarj ve uygulanabilir tasarım kavramlarını ele alır."))
    a,b,c=st.columns(3)
    a.metric(tr("Operating phases","Çalışma aşamaları"),"3")
    b.metric(tr("Research themes","Araştırma başlıkları"),str(len(TOPICS)))
    c.metric(tr("Source categories","Kaynak türleri"),str(len({r["group"] for r in REFERENCES})))
    st.markdown(tr("#### The thermal-energy pathway","#### Termal enerjinin izlediği yol"))
    phase=st.radio(tr("Explore one phase","Bir aşama seçin"),["Charging","Standby","Thermal delivery"],format_func=lambda x: {"Charging":tr("Charging","Şarj"),"Standby":tr("Standby","Bekleme"),"Thermal delivery":tr("Thermal delivery","Isı çıkışı")}[x],horizontal=True,key="hub_phase")
    details={
        tr("Charging","Şarj"):("Renewable/grid electricity or a specified solar-thermal input supplies heat. Input power, heater/optical efficiency and temperature limits matter.","Input energy is not automatically recoverable thermal energy."),
        tr("Standby","Bekleme"):("Stored heat declines because the medium loses energy across the insulation and outer surfaces. Geometry and ambient conditions matter.","A high capacity does not imply negligible long-duration loss."),
        tr("Thermal delivery","Isı çıkışı"):("Useful thermal energy is transferred to a consumer through the selected heat-transfer system; temperature grade and exchanger limitations matter.","The web model assumes simplified output constraints, not a certified delivery temperature."),
    }
    with st.container(border=True):
        st.markdown(f"**{phase}**")
        st.write(details[phase][0] if t("how")=="How It Works" else {tr("Charging","Şarj"):"Şebekeden veya yenilenebilir kaynaklardan gelen enerji ısı olarak depolanır.",tr("Standby","Bekleme"):"Depolanan enerji, yalıtım ve dış ortam koşullarına bağlı olarak ısı kaybeder.",tr("Thermal delivery","Isı çıkışı"):"Depolanan ısı, ısı transfer sistemi üzerinden kullanıcıya aktarılır."}[phase])
        st.caption(details[phase][1] if t("how")=="How It Works" else "Bunlar sadeleştirilmiş sayısal modellerdir; fiziksel sistem ölçümü değildir.")
    # No decorative numeric Sankey: it could be mistaken for measured fractions.
    c1,c2,c3=st.columns(3)
    with c1:
        st.info(tr("**1 · CHARGE** Electric or solar thermal input","**1 · ŞARJ** Elektrik veya güneş kaynaklı ısı girişi"))
    with c2:
        st.info(tr("**2 · STORE** Material energy and heat losses","**2 · DEPOLA** Malzeme enerjisi ve ısı kayıpları"))
    with c3:
        st.info(tr("**3 · DELIVER** Useful heat delivery","**3 · KULLAN** Kullanılabilir ısı çıkışı"))
    st.caption("This process map is deliberately not assigned fabricated energy "
               "percentages. Dashboard shows calculated numerical energy flows.")

    st.markdown(tr("### Explore research themes","### Araştırma konuları"))
    lookup={t["label"]:t for t in TOPICS}
    choose=st.selectbox(tr("Choose a topic","Bir konu seçin"),list(lookup),key="hub_topic")
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
        st.link_button(tr("Read the research review","Bilimsel derlemeyi aç"),REVIEW["doi"])
    st.markdown("#### All eight topics at a glance")
    for t in TOPICS:
        with st.expander(f"{t['label']}  ·  {t['section']}",expanded=False):
            st.write(t["summary"])
            st.caption(tr("Application: ","Uygulama: ")+t["model"])
            st.caption(tr("Limitation: ","Sınırlama: ")+t["limitation"])

with methods:
    st.markdown("### What each equation can support")
    st.write("The simulator implements physical relationships and simplified numerical boundaries. Cite the method and verify the input data separately.")
    rows=pd.DataFrame(MODEL_EVIDENCE)
    st.dataframe(rows,hide_index=True,width="stretch",height=400)
    st.download_button(tr("Download equations and evidence · CSV","Denklemleri ve kanıtları CSV indir"),rows.to_csv(index=False),
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
    st.markdown("#### Research evidence workflow")
    st.markdown(
        "**Equation → code → numerical test → input provenance → known gap** "
        "is the traceability standard for this release. The source-register "
        "CSV above includes the closed-pipe, multilayer insulation, tabulated "
        "cp(T), axial visualization and report modules. "
        "See [the engineering methods](https://github.com/bysquizy/"
        "Sand-Battery-Project/blob/main/docs/EQUATION_TRACEABILITY.md)."
    )
    st.caption("Direct-contact LTE and closed-pipe thermal-transfer models are "
               "different idealizations, and neither has been field-calibrated.")
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
            st.link_button(tr("Utility operator source","İşletmeci kaynağı"),"https://www.vatajankoski.fi/en/projects/sand-battery/")
            st.link_button(tr("Developer source","Geliştirici kaynağı"),"https://polarnightenergy.com/reference/worlds-first-sand-battery/")
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
    st.markdown("#### Published thermal power versus storage capacity")
    df_sites=pd.DataFrame([
        {"Site":"Kankaanpää","Source":"PNE manufacturer","Thermal power (MW)":.2,"Thermal capacity (MWh)":8},
        {"Site":"Kankaanpää","Source":"Vatajankoski operator","Thermal power (MW)":.1,"Thermal capacity (MWh)":8},
        {"Site":"Pornainen","Source":"PNE manufacturer","Thermal power (MW)":1.0,"Thermal capacity (MWh)":100},
    ])
    st.dataframe(df_sites,hide_index=True,width="stretch")
    fig=go.Figure()
    for source,color in [("PNE manufacturer","#eeb37e"),("Vatajankoski operator","#58dfc3")]:
        part=df_sites[df_sites["Source"]==source]
        fig.add_trace(go.Bar(x=part["Site"],y=part["Thermal power (MW)"],
                             marker_color=color,name=source,
                             customdata=part["Thermal capacity (MWh)"],
                             hovertemplate="%{x}: %{y:.2f} MWth<br>Capacity %{customdata} MWhth<extra></extra>"))
    fig.update_layout(barmode="group",template="plotly_dark",height=300,
                      margin=dict(l=20,r=20,t=25,b=35),
                      yaxis_title="Published thermal power (MWth)")
    st.plotly_chart(fig,width="stretch",key="hub_verified_sites")
    st.caption("These are source-attributed ratings, NOT independently matched "
               "measurements. Kankaanpää's manufacturer/operator disagreement "
               "is unresolved; do not average the two estimates.")
    st.caption("Each external statement is tagged by source type. Commercial capacity and rated power are not a calibration dataset and cannot validate thermal transients.")

with sources:
    st.markdown("### Your research material, organized")
    for item in SOURCE_NOTES:
        with st.expander(item["title"],expanded=item["title"]=="2026 research review"):
            st.write(f"**Evidence class:** {item['class']}")
            st.write("**Supports:** "+item["supports"])
            st.caption("Does not establish: "+item["not_valid"])
            if item["url"]:
                st.link_button(tr("Open external original source","Özgün kaynağı aç"),item["url"])
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
    st.markdown(tr("## Group 8","## Grup 8"))
    for member in PROJECT["members"]:
        with st.container(border=True):
            st.markdown(f"**{member}**" + (" · @bysquizy · GitHub: https://github.com/bysquizy" if member == "Yağız Topaç" else ""))

st.divider()
st.caption("Research summaries are source-grounded interpretations. The site presents a numerical study, not a physical test report.")

footer()

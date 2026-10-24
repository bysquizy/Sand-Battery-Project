"""Legacy-inspired engineering tools, newly implemented with the current physics core.

Every visual represents a numerical *scenario*, never sensor or prototype data.
"""
from dataclasses import replace
import json
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from engine.materials import MATERIALS
from engine.physics import Design, summarize
from engine.design_lab import (
    volume_for_target_mwh, cooling_profile, module_comparison,
    radial_insulation_profile, bounded_geometry_candidates,
)
from ui_theme import inject

st.set_page_config(page_title="Thermal Design Studio | Sand Battery", layout="wide", page_icon="📐")
inject()
st.caption("IZTECH  /  ESE101 GROUP 8   •   ENGINEERING TOOLKIT")
st.title("Thermal Design Studio")
st.write("Explore heat retention, modular tank geometry, insulation, and energy-capacity sizing.")
st.info("Numerical examples based on the legacy study questions. Illustrative material properties, no measured sensors, and no structural certification.")

with st.form("design_lab_parameters", border=True):
    st.markdown("#### Design inputs")
    a,b,c,d=st.columns(4)
    with a:
        material_name=st.selectbox("Storage medium",list(MATERIALS),key="dl_mat")
        volume=st.number_input("Total packed volume · m³",50.,20000.,1000.,step=50.,key="dl_vol")
    with b:
        tmin=st.number_input("Minimum useful temperature · °C",20.,200.,50.,step=10.,key="dl_tmin")
        tmax=st.number_input("Maximum temperature · °C",200.,850.,550.,step=10.,key="dl_tmax")
    with c:
        modules=st.number_input("Tank modules",1,16,2,key="dl_modules")
        aspect=st.slider("Height / radius",1.,6.,3.,.25,key="dl_aspect")
    with d:
        insulation=st.slider("Insulation thickness · m",.1,1.5,.5,.05,key="dl_insul")
        ambient=st.number_input("Ambient · °C",-25.,45.,15.,key="dl_ambient")
    submitted=st.form_submit_button("Update engineering study",type="primary",use_container_width=True)

m=MATERIALS[material_name]
d=Design(volume_m3=volume,modules=int(modules),height_over_radius=aspect,
         insulation_m=insulation,ambient_c=ambient,minimum_c=tmin,maximum_c=tmax)
try:
    base=summarize(d,m)
except ValueError as exc:
    st.error(f"Correct the design inputs: {exc}")
    st.stop()

x,y,z,w=st.columns(4)
x.metric("Stored sensible heat",f"{base['capacity_mwh']:,.1f} MWh(th)")
y.metric("Initial heat loss",f"{base['initial_loss_kw']:,.1f} kW")
z.metric("Module height",f"{base['height_m']:.2f} m")
w.metric("Thermal conductance",f"{base['ua_w_k']:.1f} W/K")

cooling,modules_tab,insulation_tab,sizing=st.tabs([
    "01 · Cooling & retention","02 · Modular geometry",
    "03 · Insulation gradients","04 · Capacity sizing"
])

with cooling:
    st.subheader("Passive standby cooling")
    st.caption("Solves a lumped energy balance with temperature-dependent heat capacity. No thermal load or charging during standby.")
    days=st.slider("Simulated standby period · days",1,90,14,1,key="dl_days")
    try:
        res=cooling_profile(d,m,float(days),samples=121)
        cols=st.columns(3)
        cols[0].metric("End temperature",f"{res['temperature_c'][-1]:.1f} °C")
        cols[1].metric("Accumulated heat loss",f"{res['loss_mwh'][-1]:.2f} MWh")
        cols[2].metric("Final instantaneous heat loss",f"{res['heat_loss_kw'][-1]:.1f} kW")
        fig=go.Figure()
        fig.add_trace(go.Scatter(x=res['days'],y=res['temperature_c'],name="Average medium temperature",
                      mode="lines",line=dict(color="#eeb37e",width=4)))
        fig.add_hline(y=tmin,line_dash="dot",line_color="#58dfc3",
                      annotation_text="Minimum useful temperature")
        fig.update_layout(template="plotly_dark",height=340,
                          xaxis_title="Standby duration (days)",yaxis_title="Mean solid temperature (°C)")
        st.plotly_chart(fig,width="stretch",key="dl_cooling_fig")
        fig2=go.Figure()
        fig2.add_trace(go.Scatter(x=res['days'],y=res['loss_mwh'],name="Cumulative ambient loss",
                     fill="tozeroy",line=dict(color="#58dfc3",width=3)))
        fig2.update_layout(template="plotly_dark",height=290,xaxis_title="Standby duration (days)",
                           yaxis_title="Heat lost since charged (MWh)")
        st.plotly_chart(fig2,width="stretch",key="dl_cooling_losses")
        export=pd.DataFrame({"standby_days":res["days"],"mean_temperature_c":res["temperature_c"],
            "cumulative_loss_mwh":res["loss_mwh"],"instant_loss_kw":res["heat_loss_kw"]})
        st.download_button("Download cooling time-series · CSV",export.to_csv(index=False),
                           file_name="cooling_scenario.csv",mime="text/csv",key="dl_cool_csv")
    except (ValueError,RuntimeError) as exc:
        st.error(str(exc))
    st.latex(r"m c_p(T) \frac{dT}{dt} = -UA(T-T_{amb})")
    st.caption("With constant cp this reduces to Newton cooling; with cp(T), a numerical ODE solution is used.")

with modules_tab:
    st.subheader("Same storage capacity, different silo arrangements")
    st.caption("Split the same packed volume into multiple identical cylindrical modules. Only geometry and simplified heat-loss resistance change.")
    try:
        rows=module_comparison(d,m,(1,2,3,4,6,8,12,16))
        frame=pd.DataFrame(rows)
        f=go.Figure()
        f.add_trace(go.Scatter(x=frame["Modules"],y=frame["Initial heat loss (kW)"],
                  mode="lines+markers",name="Total initial heat loss",line=dict(color="#eeb37e",width=3)))
        f.update_layout(template="plotly_dark",height=350,xaxis_title="Number of identical tanks",
                        yaxis_title="Total initial heat loss (kW)")
        st.plotly_chart(f,width="stretch",key="dl_modules_graph")
        a,b=st.columns([1.3,1])
        with a:
            st.dataframe(frame.round(3),hide_index=True,width="stretch",height=340)
        with b:
            show_n=st.slider("Visualize modular tank array",1,16,int(modules),key="dl_modules_3d")
            # Illustrative array of silo centerlines and pointwise upper/lower perimeters.
            cols=int(np.ceil(np.sqrt(show_n)))
            pos=np.arange(show_n)
            xx=(pos%cols)*3.2; yy=(pos//cols)*3.2
            fig3=go.Figure()
            for n,(cx,cy) in enumerate(zip(xx,yy),1):
                angles=np.linspace(0,2*np.pi,40)
                for h0 in [0,3.5]:
                    fig3.add_trace(go.Scatter3d(x=cx+np.cos(angles),y=cy+np.sin(angles),
                       z=np.full_like(angles,h0),mode="lines",line=dict(color="#58dfc3" if h0 else "#eeb37e",width=4),
                       showlegend=False,hovertemplate=f"Module {n}<extra></extra>"))
                fig3.add_trace(go.Scatter3d(x=[cx,cx],y=[cy,cy],z=[0,3.5],mode="lines",
                        line=dict(color="#8aaec0",width=2),showlegend=False))
            fig3.update_layout(template="plotly_dark",height=330,margin=dict(l=0,r=0,t=0,b=0),
                  scene=dict(xaxis_visible=False,yaxis_visible=False,zaxis_visible=False,aspectmode="data"))
            st.plotly_chart(fig3,width="stretch",key="dl_module_arrangement")
            st.caption("Module array is schematic only. Spacing, outer footprint and structural foundations are not optimized.")
        st.download_button("Download module comparison · CSV",frame.to_csv(index=False),
            file_name="module_comparison.csv",mime="text/csv",key="dl_module_csv")
    except ValueError as exc:
        st.error(str(exc))

with insulation_tab:
    st.subheader("Illustrative radial insulation temperature")
    st.caption("Quasi-steady heat conduction through the cylindrical SIDE insulation with outside convection. The graph is NOT a transient 2-D solid-temperature prediction.")
    t_inner=st.slider("Insulation inner-face temperature · °C",float(ambient),float(tmax),float(tmax),step=5.,key="dl_inner")
    try:
        rprof=radial_insulation_profile(d,t_inner)
        a,b=st.columns([1.7,1])
        with a:
            fig=go.Figure(go.Scatter(x=rprof["radius_m"],y=rprof["temperature_c"],mode="lines",
                   line=dict(color="#eeb37e",width=4),fill="tozeroy",fillcolor="rgba(238,179,126,.12)"))
            fig.update_layout(template="plotly_dark",height=370,
                  xaxis_title="Radial distance from silo center (m)",
                  yaxis_title="Insulation temperature (°C)")
            st.plotly_chart(fig,width="stretch",key="dl_radial")
        with b:
            st.metric("Outer insulation surface",f"{rprof['surface_c']:.1f} °C")
            st.metric("Sidewall heat loss / module",f"{rprof['side_heat_kw_per_module']:.2f} kW")
            st.caption("End-cap losses are accounted for separately in the 0-D design summary.")
        if st.checkbox("Animate a quasi-steady wall profile across cooldown",value=False,key="dl_wall_animation"):
            cool=cooling_profile(d,m,14.,samples=16)
            profiles=[radial_insulation_profile(d,float(temp),nodes=45)["temperature_c"]
                        for temp in cool["temperature_c"]]
            ff=go.Figure(go.Heatmap(x=np.linspace(0,14,16),y=rprof["radius_m"],
                     z=np.array(profiles).T,colorscale="Turbo",colorbar=dict(title="°C"),
                     hovertemplate="Day %{x:.1f}<br>Radius %{y:.2f}m<br>T %{z:.1f}°C<extra>Numerical scenario</extra>"))
            ff.update_layout(template="plotly_dark",height=340,
                             xaxis_title="Cooling time (days)",yaxis_title="Radial position (m)")
            st.plotly_chart(ff,width="stretch",key="dl_wall_heatmap")
            st.caption("Each time slice is a steady wall approximation driven by the bulk 0-D cooling model.")
    except (ValueError,RuntimeError) as exc:
        st.error(str(exc))

with sizing:
    st.subheader("Reverse-size the theoretical energy capacity")
    st.caption("Find the bulk volume needed for a *theoretical sensible heat target*. This is NOT useful delivered heat or site construction clearance.")
    target=st.number_input("Target theoretical storage · MWh(th)",1.,10000.,250.,step=25.,key="dl_target")
    try:
        needed=volume_for_target_mwh(m,tmin,tmax,target)
        st.metric("Minimum theoretical packed volume",f"{needed:,.1f} m³")
        st.caption("Based on the material's *illustrative* packed density and cp(T) assumptions.")
        max_h=st.number_input("Maximum silo height · m",5.,100.,35.,step=1.,key="dl_maxheight")
        max_d=st.number_input("Maximum outside diameter · m",3.,60.,24.,step=1.,key="dl_maxdiam")
        st.markdown("**Bounded geometry candidates for your current volume**")
        candidate=bounded_geometry_candidates(d,m,max_h,max_d)
        if candidate:
            cf=pd.DataFrame(candidate)
            fig=go.Figure(go.Scatter(x=cf["Insulation volume (m³)"],
                       y=cf["Initial loss (kW)"],mode="markers",marker=dict(
                       size=14,color=cf["H/R"],colorscale="Viridis",showscale=True,
                       colorbar=dict(title="H/R")),text=[f"H/R={v:g}" for v in cf["H/R"]]))
            fig.update_layout(template="plotly_dark",height=330,
                       xaxis_title="Simple insulation shell volume (m³)",yaxis_title="Initial heat leak (kW)")
            st.plotly_chart(fig,width="stretch",key="dl_sizing_pareto")
            st.dataframe(cf.round(3),hide_index=True,width="stretch")
            st.download_button("Download feasible geometry · CSV",cf.to_csv(index=False),
                               file_name="feasible_geometry.csv",key="dl_geo_csv")
        else:
            st.warning("No geometry candidates satisfy both limits. Increase facility dimensions or change the base volume.")
        st.download_button("Export design inputs · JSON",
            json.dumps({"material":material_name,"design":d.__dict__,
                        "target_theoretical_mwh":target,"required_volume_m3":needed},indent=2),
            file_name="thermal_design_inputs.json",mime="application/json",key="dl_json")
    except ValueError as exc:
        st.error(str(exc))

st.divider()
st.markdown("**Method references:** Bošnjaković & Santa (2026), DOI 10.3390/cleantechnol8050165; original team legacy calculation archive (engineering workflow), not a measured dataset.")
st.caption("All figures are mathematical visualization of numerical assumptions; no real prototype, instrumentation, CFD, structural qualification or cost validation is included.")

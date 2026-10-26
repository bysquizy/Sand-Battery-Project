"""Advanced numerical research tools with on-demand, selected workspace rendering."""
from dataclasses import replace
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st
from engine.materials import MATERIALS
from engine.physics import summarize,simulate_cycle
from engine.input_validation import parse_hourly_dispatch_csv
from scenario_state import active, scenario_banner
from engine.research_v2 import (exergy_mwh,illustrative_renewables,dispatch,
   Exchanger,exchanger,ergun,uncertainty,levelized_heat,LTNE,ltne)

st.set_page_config(page_title="Engineering Research Lab | Sand Battery Studio",page_icon="🔬",layout="wide")
from ui_theme import inject, hero, footer
inject()

hero("RESEARCH / ADVANCED PHYSICS", "Engineering Research Lab", "Compare second-law bounds, renewable dispatch, packed-bed heat transfer, heat exchangers, uncertainty and research-grade economics.")
shared = active()
scenario_banner()
st.write("Interactive calculations, parameter studies and physical model comparisons. **All results are numerical scenarios, not measured laboratory performance.**")
st.warning("The 1-D gas/solid packed-bed model is not a calibrated closed-loop pipe-in-sand design. Material properties are approximate and require independent verification.")

with st.sidebar:
    st.subheader("Local research variations")
    st.caption("Starts from the shared design. Edits here are exploratory and do not change Active Scenario.")
    name=st.selectbox("Base medium",list(MATERIALS),index=list(MATERIALS).index(shared.material_name),key="research_medium")
    m=MATERIALS[name]
    volume=st.number_input("Packed material volume (m³)",50.,20000.,float(shared.volume_m3),step=100.,key="research_vol")
    minimum=st.number_input("Minimum solid temperature (°C)",20.,200.,float(shared.minimum_c),step=10.,key="research_low")
    maximum=st.number_input("Maximum solid temperature (°C)",250.,850.,float(shared.maximum_c),step=10.,key="research_high")
    inputmw=st.number_input("Charging power (MW)",.2,300.,float(shared.charge_power_mw()),step=.5,key="research_power")
    heatmw=st.number_input("Thermal discharge rating (MW)",.1,40.,float(shared.thermal_output_mw),step=.5,key="research_load")
    st.caption(m.provenance)
d=replace(shared.make_design(), volume_m3=volume, minimum_c=minimum, maximum_c=maximum, charge_mw=inputmw, thermal_output_mw=heatmw)
try:
    s = summarize(d, m)
except ValueError as exc:
    st.error(f"Check the thermal design: {exc}")
    st.stop()
# Streamlit tabs eagerly render all children. Select exactly one computation
# to avoid repeating Monte Carlo, dispatch and thermal-cycle work every rerun.
study = st.radio(
    "Select research method",
    ["Exergy", "Renewable Dispatch", "LTNE & Flow", "Exchanger",
     "Uncertainty", "Cost Lab"],
    horizontal=True, key="research_workspace",
    label_visibility="collapsed",
)

if study == 'Exergy':
    st.subheader("Thermal storage vs reversible work potential")
    x=exergy_mwh(m,volume,minimum,maximum,d.ambient_c)
    a,b=st.columns(2)
    a.metric("Sensible thermal storage",f"{s['capacity_mwh']:,.1f} MWhth")
    b.metric("Reversible exergy upper bound",f"{x:,.1f} MWhex")
    ts=np.linspace(minimum+1,maximum,50)
    capacity=m.bulk_density*volume*(m.enthalpy(ts)-m.enthalpy(minimum))/3.6e9
    ex=np.array([exergy_mwh(m,volume,minimum,t,d.ambient_c) for t in ts])
    fig=go.Figure()
    fig.add_trace(go.Scatter(x=ts,y=capacity,mode='lines',name='Stored thermal energy',line=dict(color='#e8a670',width=4)))
    fig.add_trace(go.Scatter(x=ts,y=ex,mode='lines',name='Exergy upper bound',line=dict(color='#67dcc9',width=4)))
    fig.update_layout(template='plotly_dark',height=380,xaxis_title='Maximum temperature (°C)',yaxis_title='MWh')
    st.plotly_chart(fig,width='stretch',key="research_exergy_fig")
    st.latex(r'Q=m\int_{T_\min}^{T_\max}c_p(T)\,dT')
    st.latex(r'X=m\int_{T_\min}^{T_\max}c_p(T)\left(1-\frac{T_0}{T}\right)dT')
    st.caption("Exergy uses Kelvin absolute temperatures and represents reversible availability, NOT electricity delivered.")

elif study == 'Renewable Dispatch':
    st.subheader("Hourly renewable energy and heat-demand matching")
    a,b,c=st.columns(3)
    with a:days=st.slider("Scenario days",1,14,7,key="research_days")
    with b:pv=st.slider("PV rating (MWp)",0.,30.,10.,1.,key="research_pv")
    with c:wind=st.slider("Wind rating (MW)",0.,30.,8.,1.,key="research_wind")
    upload=st.file_uploader("Optional user CSV: available_mw,demand_mw (up to 1 MB / 8,760 rows)",type="csv",key="research_csv")
    try:
        if upload:
            if upload.size > 1_000_000:
                raise ValueError("CSV must not exceed 1 MB.")
            supply, requested = parse_hourly_dispatch_csv(upload.getvalue())
            source="User CSV: unverified data"
        else:
            supply=illustrative_renewables(24*days,pv,wind)
            requested=np.full(len(supply),heatmw)
            source="Synthetic source values, not weather measurements"
        r=dispatch(d,m,supply,requested)
        k1,k2,k3=st.columns(3)
        k1.metric("Thermal demand fulfilled",f"{100*sum(r['delivered_mwh'])/max(1e-10,sum(requested)):.1f}%")
        k2.metric("Renewable input curtailed",f"{sum(r['curtailed_mwh']):.1f} MWh")
        k3.metric("Conservation residual",f"{r['balance_residual_mwh']:.1e} MWh")
        fig=make_subplots(rows=2,cols=1,shared_xaxes=True,vertical_spacing=.12,
           subplot_titles=("Source power and thermal load","Storage SOC"))
        fig.add_trace(go.Scatter(y=supply,name="Renewable source",line=dict(color="#e8a670")),1,1)
        fig.add_trace(go.Scatter(y=requested,name="Heat demand",line=dict(color="#67dcc9")),1,1)
        fig.add_trace(go.Scatter(y=r["soc_pct"],name="Stored SOC",fill="tozeroy",line=dict(color="#a99cff")),2,1)
        fig.update_layout(template="plotly_dark",height=560)
        fig.update_yaxes(title_text="MW",row=1,col=1)
        fig.update_yaxes(title_text="SOC (%)",row=2,col=1)
        fig.update_xaxes(title_text="Hours",row=2,col=1)
        st.plotly_chart(fig,width="stretch",key="research_dispatch_fig")
        export=pd.DataFrame({"available_mw":supply,"demand_mw":requested,"delivered_mwh":r["delivered_mwh"],
            "curtailed_mwh":r["curtailed_mwh"],"storage_soc_pct":r["soc_pct"][1:]})
        st.download_button("Export simulated dispatch CSV",export.to_csv(index=False),file_name="dispatch.csv")
        st.caption(source+". Hourly simplified charge–loss–delivery sequence; no price-aware optimization or exchanger pinch.")
    except (ValueError, KeyError, TypeError) as exc:
        st.error(f"Invalid hourly scenario: {exc}")

elif study == 'LTNE & Flow':
    st.subheader("Direct-contact packed-bed fluid–solid model")
    c1,c2,c3=st.columns(3)
    with c1:cells=st.slider("Axial cells",8,40,20,4,key="research_cells")
    with c2:hours=st.slider("Duration (hours)",.5,8.,2.,.5,key="research_hours")
    with c3:hv=st.number_input("Gas-solid h_v (W/m³K)",100.,15000.,1500.,100.,key="research_hv")
    if st.button("Solve gas/solid two-temperature profiles",type="primary",key="research_solve"):
        try:
            cfg=LTNE(cells=cells,hours=hours,hv=hv,initial_c=minimum,inlet_c=maximum)
            with st.spinner("Solving coupled finite-volume equations"):
                st.session_state["research_ltne"]=ltne(d,m,cfg)
                st.session_state["research_cfg"]=(d,m,cfg)
        except (RuntimeError,ValueError) as exc:st.error(str(exc))
    cfg=LTNE(cells=cells,hours=hours,hv=hv,initial_c=minimum,inlet_c=maximum)
    if st.session_state.get("research_cfg")==(d,m,cfg):
        r=st.session_state["research_ltne"]
        st.metric("1-D energy closure residual",f"{r['residual_mwh']:.3e} MWh")
        fig=make_subplots(rows=1,cols=2,subplot_titles=("Gas temperature","Solid temperature"))
        for i,z in enumerate(["gas_c","solid_c"],1):
            fig.add_trace(go.Heatmap(z=r[z],x=r["z_m"],y=r["time_h"],colorscale='Turbo',showscale=i==2),1,i)
        fig.update_layout(template="plotly_dark",height=430)
        st.plotly_chart(fig,width="stretch",key="research_ltne_fig")
    else:st.info("Run the optional transport solver to view two-phase heatmaps.")
    st.divider()
    st.subheader("Ergun pressure loss and illustrative fan power")
    c1,c2=st.columns(2)
    with c1:eps=st.slider("Void fraction",.25,.65,.42,.01,key="research_eps")
    with c2:v=st.slider("Superficial velocity (m/s)",.0,.15,.025,.005,key="research_vel")
    z=ergun(12,15,eps,.016,v)
    p1,p2,p3=st.columns(3)
    p1.metric("Pressure drop",f"{z['delta_p_pa']:.1f} Pa")
    p2.metric("Fan power",f"{z['fan_kw']:.3f} kW")
    p3.metric("Particle Reynolds number",f"{z['particle_re']:.0f}")
    st.caption("Direct-contact Ergun equation, not a commercial closed-pipe fan calculation. Liu et al. 2024 tested 16 mm glass beads, Re 58–252.")

elif study == 'Exchanger':
    st.subheader("Effectiveness–NTU heat exchanger")
    u1,u2,u3=st.columns(3)
    with u1:th=st.number_input("Hot inlet °C",100.,800.,500.,key="research_th")
    with u2:tc=st.number_input("Cold inlet °C",10.,400.,60.,key="research_tc")
    with u3:ua=st.number_input("Exchanger UA (kW/K)",.5,500.,40.,key="research_ua")
    kind=st.selectbox("Flow arrangement",["counterflow","parallel"],key="research_arr")
    try:
        inp=Exchanger(th,tc,25,20,ua,kind)
        out=exchanger(inp)
        p1,p2,p3=st.columns(3)
        p1.metric("Transferred power",f"{out['q_mw']:.2f} MWth")
        p2.metric("Effectiveness",f"{100*out['effectiveness']:.1f}%")
        p3.metric("NTU",f"{out['ntu']:.2f}")
        fig=go.Figure()
        fig.add_trace(go.Scatter(x=['In','Out'],y=[th,out['hot_out_c']],name='Hot side',mode='lines+markers'))
        fig.add_trace(go.Scatter(x=['In','Out'],y=[tc,out['cold_out_c']],name='Cold side',mode='lines+markers'))
        fig.update_layout(template='plotly_dark',height=330,yaxis_title="Temperature (°C)")
        st.plotly_chart(fig,width="stretch",key="research_exchanger_fig")
    except ValueError as exc:st.error(str(exc))
    st.latex(r'Q=\epsilon C_{\min}(T_{h,in}-T_{c,in}),\;\;NTU=UA/C_{\min}')
    st.caption("Steady exchanger experiment only, not thermally coupled to the dynamic bed.")

elif study == 'Uncertainty':
    st.subheader("Assumption-based uncertainty propagation")
    sd=st.slider("Assumed input standard deviation (%)",0,30,10,key="research_sigma")/100
    r=uncertainty(d,m,400,sd,seed=23)
    ci=np.percentile(r["capacity_samples_mwh"],[5,50,95])
    st.metric("Illustrative P05–P95 capacity",f"{ci[0]:.1f}–{ci[2]:.1f} MWhth")
    fig=go.Figure(go.Histogram(x=r["capacity_samples_mwh"],nbinsx=32,marker_color="#e8a670"))
    fig.update_layout(template="plotly_dark",height=360,xaxis_title="Theoretical capacity (MWhth)")
    st.plotly_chart(fig,width="stretch",key="research_uncertainty_fig")
    st.warning("Input distributions are assumptions, not empirically estimated uncertainty bounds.")

elif study == 'Cost Lab':
    st.subheader("Transparent financial scenario — LCOH")
    a,b,c=st.columns(3)
    with a:capex=st.number_input("Hypothetical CAPEX (€)",0.,100_000_000.,2_000_000.,100_000.,key="research_capex")
    with b:price=st.number_input("Input energy price (€/MWh)",0.,500.,70.,5.,key="research_price")
    with c:cycles=st.slider("Annual equivalent cycles",1,365,150,key="research_cycles")
    try:
        r=simulate_cycle(d,m,max_step_s=3600)
        value=levelized_heat(capex,20,.08,cycles,r["useful_heat_mwh"],r["source_input_mwh"],price,30000)
        st.metric("Scenario levelized cost of heat",f"{value:.1f} €/MWhth")
        prices=np.linspace(0,max(1,price*2),25)
        costs=[levelized_heat(capex,20,.08,cycles,r["useful_heat_mwh"],r["source_input_mwh"],p,30000) for p in prices]
        fig=go.Figure(go.Scatter(x=prices,y=costs,mode="lines",line=dict(color="#67dcc9",width=3)))
        fig.update_layout(template="plotly_dark",height=350,xaxis_title="Input price (€/MWh)",yaxis_title="LCOH (€/MWh)")
        st.plotly_chart(fig,width="stretch",key="research_lcoh_fig")
    except (ValueError,RuntimeError) as exc:st.error(str(exc))
    st.caption("This is not an investment recommendation, market quote or techno-economic validation.")

st.divider()
st.caption("References: Bošnjaković & Santa (2026), DOI 10.3390/cleantechnol8050165; Liu et al. (2024), DOI 10.1016/j.est.2023.109957. Sources, assumptions and test limitations must be disclosed.")

footer()

"""Independent Stage 3 physics verification and idealized closed-pipe research."""
from __future__ import annotations

from dataclasses import replace
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from engine.closed_pipe import PipeLoop, pipe_transfer, simulate_closed_pipe
from engine.design_lab import cooling_profile
from engine.materials import MATERIALS
from engine.physics import simulate_cycle, summarize
from engine.property_curves import TabulatedMaterial
from engine.insulation_layers import InsulationLayer, layered_cylinder
from engine.thermocline import simulate_thermocline
from scenario_state import active, scenario_banner
from ui_theme import inject, hero, footer
from localization import tr

st.set_page_config(page_title="Model Verification | Sand Battery Studio",
                   page_icon="📏", layout="wide")
inject()
hero(tr("METHODS / VERIFICATION","YÖNTEMLER / DOĞRULAMA"), tr("Model Verification","Model Doğrulama"), tr("Compare physical topologies, inspect numerical conservation and explore the limits of simplified exchanger models.","Fiziksel modelleri, enerji korunumunu ve basitleştirilmiş ısı değiştiricilerinin sınırlarını karşılaştırın."))
s = active()
scenario_banner()
d = s.make_design()
m = MATERIALS[s.material_name]
st.warning("Research-grade numerical approximations, NOT experimentally calibrated "
           "equipment, design certification or published plant performance.")
compare_tab, pipe_tab, material_tab, insulation_tab, convergence_tab = st.tabs([
    tr("0-D vs 1-D","0B ve 1B karşılaştırması"), tr("Closed-Pipe Heat Transfer","Kapalı boruda ısı transferi"), "cp(T) Data Integrity",
    "Layered Insulation", "Verification Benchmarks",
])


@st.cache_data(max_entries=12, ttl=1800, show_spinner=False)
def _comparison(design, material, count, c_charge, c_discharge):
    zero = simulate_cycle(design, material, max_step_s=3600)
    one = simulate_thermocline(
        design, material, n_cells=count,
        charge_cutoff_pct=c_charge, discharge_cutoff_pct=c_discharge,
    )
    return zero, one


@st.cache_data(max_entries=12, ttl=1800, show_spinner=False)
def _pipe(design, material, parameters):
    return simulate_closed_pipe(design, material, parameters, max_step_s=3600)


@st.cache_data(max_entries=12, ttl=1800, show_spinner=False)
def _grid(design, material, c_charge, c_discharge):
    records = []
    for n in (16, 32, 64):
        r = simulate_thermocline(
            design, material, n_cells=n, charge_cutoff_pct=c_charge,
            discharge_cutoff_pct=c_discharge,
        )
        records.append({
            "Axial cells": n,
            "Delivered MWh(th)": r["useful_heat_mwh"],
            "Energy residual MWh(th)": r["energy_balance_residual_mwh"],
            "Discharge h": r["discharge_h"],
        })
    return pd.DataFrame(records)


with compare_tab:
    st.subheader("Different physical topologies, different model boundaries")
    st.write("The 0-D model stores all energy at one uniform temperature and "
             "delivers constant heat down to Tmin. The 1-D LTE model represents "
             "axial through-bed flow with a temperature front and separate "
             "charge/discharge cutoff rules. Agreement is **not** expected "
             "unless the boundaries are first made physically equivalent.")
    a, b, c = st.columns(3)
    with a:
        n = st.slider("1-D axial cells", 16, 80, 32, 8, key="verify_cells")
    with b:
        charge_cut = st.slider("Charge cutoff (% of temperature span)",
                               1, 50, 10, 1, key="verify_charge_cutoff")
    with c:
        discharge_cut = st.slider("Discharge cutoff (% of temperature span)",
                                  20, 95, 70, 1, key="verify_discharge_cutoff")
    if st.button("Calculate and compare both models", type="primary",
                 key="verify_compare_run"):
        try:
            with st.spinner("Solving the 0-D energy balance and axial 1-D model"):
                result = _comparison(d, m, n, charge_cut, discharge_cut)
            st.session_state["verified_comparison"] = result
            st.session_state["verified_comparison_config"] = (d, m, n, charge_cut, discharge_cut)
        except (ValueError, RuntimeError, OverflowError, FloatingPointError) as exc:
            st.error(f"Model comparison could not be completed: {exc}")

    if st.session_state.get("verified_comparison_config") == (d, m, n, charge_cut, discharge_cut):
        zero, one = st.session_state["verified_comparison"]
        frame = pd.DataFrame([
            {"Approach": "0-D uniform body", "Useful heat (MWhth)": zero["useful_heat_mwh"],
             "Charge (h)": zero["charge_hours"], "Discharge (h)": zero["discharge_hours"],
             "Residual (MWh)": zero["energy_balance_residual_mwh"]},
            {"Approach": "1-D direct contact LTE", "Useful heat (MWhth)": one["useful_heat_mwh"],
             "Charge (h)": one["charge_h"], "Discharge (h)": one["discharge_h"],
             "Residual (MWh)": one["energy_balance_residual_mwh"]},
        ])
        st.dataframe(frame, hide_index=True, width="stretch")
        st.metric("1-D relative to 0-D useful heat",
                  f"{100 * (one['useful_heat_mwh']/max(zero['useful_heat_mwh'],1e-9)-1):+.1f}%")
        fig = go.Figure()
        for _, row in frame.iterrows():
            fig.add_trace(go.Bar(name=row["Approach"], x=["Useful thermal heat"],
                                 y=[row["Useful heat (MWhth)"]]))
        fig.update_layout(barmode="group",template="plotly_dark",height=320,
                          yaxis_title="Modelled delivered heat (MWhth)")
        st.plotly_chart(fig,width="stretch",key="verify_model_bar")
        st.caption("1-D cutoffs are relative to Tmin–Tmax and are not the same "
                   "physical constraint as the 0-D constant-power stopping condition. "
                   "The 1-D residual is a numerical energy-ledger check, not calibration.")
    else:
        st.info("Run both models to see the comparison and the reasons for differing results.")

with pipe_tab:
    st.subheader("Embedded-pipe topology — idealized lumped-solid exchanger")
    st.write("This separate model uses fluid convection, cylindrical metal-wall "
             "conduction and an effective radial solid conduction resistance. "
             "The solid has one mean temperature. Pipe temperature is solved "
             "through a steady effectiveness relation; hot-loop input and "
             "temperature-grade-limited useful heat are separately integrated.")
    a, b, c = st.columns(3)
    with a:
        tubes = st.number_input("Number of parallel tubes",1,2000,40,5,key="pipe_tubes")
        length = st.number_input("Tube length each (m)",1.0,150.0,25.0,1.0,key="pipe_length")
        pitch = st.slider("Representative tube pitch (m)",0.15,1.0,0.40,0.05,key="pipe_pitch")
    with b:
        flow = st.slider("Total fluid mass flow (kg/s)",0.5,100.0,6.0,0.5,key="pipe_flow")
        coefficient = st.slider("Internal convection h (W/m²K)",10.0,500.0,40.0,10.0,key="pipe_h")
        medium_k = st.slider("Effective solid conductivity (W/mK)",0.2,5.0,1.0,0.2,key="pipe_k")
    with c:
        hot = st.number_input("Hot-loop inlet (°C)", float(d.maximum_c + 1), 1200.0,
                              float(d.maximum_c + 100), 10.0,key="pipe_hot")
        cold = st.number_input("Cool-loop return (°C)",
                               float(d.ambient_c-25), float(d.minimum_c-1),
                               float(d.minimum_c-20), 1.0,key="pipe_return")
        useful = st.number_input("Minimum useful outlet (°C)",
                                 float(cold+1),float(d.maximum_c),float(d.minimum_c),
                                 1.0,key="pipe_grade")

    parameters = PipeLoop(
        tubes=int(tubes), length_m=float(length), pitch_m=float(pitch),
        mass_flow_kg_s=float(flow), fluid_h_w_m2k=float(coefficient),
        effective_solid_k_w_mk=float(medium_k), hot_inlet_c=float(hot),
        return_inlet_c=float(cold), useful_outlet_c=float(useful),
    )
    try:
        info = pipe_transfer(parameters, d)
        p1, p2, p3, p4 = st.columns(4)
        p1.metric("Pipe-system UA", f"{info['ua_w_k']:,.0f} W/K")
        p2.metric("Transfer effectiveness", f"{info['effectiveness']*100:.1f}%")
        p3.metric("Heat-transfer NTU", f"{info['ntu']:.2f}")
        p4.metric("Delivery cutoff solid T",f"{info['minimum_solid_for_delivery_c']:.1f} °C")
        source = np.linspace(d.minimum_c, d.maximum_c, 100)
        output = info["fluid_capacity_w_k"] * info["effectiveness"] * (
            source - parameters.return_inlet_c) / 1e6
        fig = go.Figure(go.Scatter(
            x=source, y=np.maximum(output,0), mode="lines",
            line=dict(color="#58dfc3",width=3),
            name="Thermal transfer to return loop"))
        fig.add_hline(y=d.thermal_output_mw,line_dash="dash",line_color="#eeb37e",
                      annotation_text="Requested maximum output")
        fig.add_vline(x=info["minimum_solid_for_delivery_c"],
                      line_dash="dot",line_color="#bc7980",
                      annotation_text="Minimum useful outlet grade")
        fig.update_layout(template="plotly_dark",height=340,
                          xaxis_title="Uniform solid temperature (°C)",
                          yaxis_title="Idealized heat transfer (MWth)")
        st.plotly_chart(fig, width="stretch",key="pipe_power_vs_temp")
        st.caption("The plotted transfer curve is an upper idealization for "
                   "fixed geometry, constant cp and h. The thermal loop may "
                   "not be deliverable below the required outlet temperature.")
    except ValueError as exc:
        info = None
        st.error(f"Pipe-loop parameters are outside the model domain: {exc}")

    if st.button("Run charge → standby → deliver", key="pipe_solve",
                 type="primary", disabled=info is None):
        try:
            with st.spinner("Solving the lumped solid and loop energy ledger"):
                out = _pipe(d, m, parameters)
            st.session_state["closed_pipe_result"] = out
            st.session_state["closed_pipe_config"] = (d, m, parameters)
        except (RuntimeError, ValueError) as exc:
            st.error(f"Cannot complete loop scenario: {exc}")
    if st.session_state.get("closed_pipe_config") == (d, m, parameters):
        out = st.session_state["closed_pipe_result"]
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Loop charge duration", f"{out['charge_hours']:.1f} h")
        c2.metric("Useful heat", f"{out['useful_heat_mwhth']:.1f} MWhth")
        c3.metric(tr("Thermal delivery","Isı çıkışı"), f"{out['discharge_hours']:.1f} h")
        c4.metric("Energy residual", f"{out['energy_balance_residual_mwhth']:.2e} MWh")
        flow = pd.DataFrame([
            {"Energy flow": "Hot-loop heat added", "MWhth": out["loop_input_mwhth"]},
            {"Energy flow": "Ambient loss", "MWhth": out["ambient_loss_mwhth"]},
            {"Energy flow": "Useful heat delivered", "MWhth": out["useful_heat_mwhth"]},
            {"Energy flow": "Final stored energy vs Tmin", "MWhth": out["final_relative_energy_mwhth"]},
        ])
        st.dataframe(flow,hide_index=True,width="stretch")
        st.caption("Hot-loop input is transferred thermal energy, NOT "
                   "total solar/electrical system input. Pump/fan electricity, "
                   "construction, contact resistance, piping length validation "
                   "and measured local hot spots are excluded.")
    else:
        st.caption("Execute the separate pipe scenario to calculate transient thermal output.")

with material_tab:
    st.subheader("Source-labelled material data and an interpolation method")
    st.write(f"**{m.name}** — model input: {m.provenance}. Current base model "
             "uses an illustrative linear cp(T), NOT measured DSC curves.")
    st.markdown("**Illustrative cp(T) profile — user-controlled, not a NREL dataset**")
    a, b, c = st.columns(3)
    with a:
        cp1 = st.number_input("cp at Tmin (J/kgK)",400.,2000.,800.,50.,key="verify_cp1")
    with b:
        cp2 = st.number_input("cp halfway (J/kgK)",400.,2000.,950.,50.,key="verify_cp2")
    with c:
        cp3 = st.number_input("cp at Tmax (J/kgK)",400.,2000.,1050.,50.,key="verify_cp3")
    try:
        middle = (d.minimum_c + d.maximum_c)/2
        tabulated = TabulatedMaterial(
            name="Illustrative assumed cp(T)",bulk_density=m.bulk_density,
            temperatures_c=(d.minimum_c,middle,d.maximum_c),
            cp_j_kgk=(cp1,cp2,cp3),
            provenance="Hypothetical user-defined profile, not laboratory data.",
        )
        temps = np.linspace(d.minimum_c,d.maximum_c,101)
        frame = pd.DataFrame({
            "Temperature (°C)":temps,
            "Assumed tabulated cp (J/kgK)":tabulated.cp(temps),
            "Current linear cp (J/kgK)":m.cp(temps),
        })
        st.line_chart(frame.set_index("Temperature (°C)"),height=280)
        actual = summarize(d,m)["capacity_mwh"]
        hypothetical = (m.bulk_density*d.volume_m3*(
            tabulated.enthalpy(d.maximum_c)-tabulated.enthalpy(d.minimum_c))/3.6e9)
        st.metric("Hypothetical table-based theoretical capacity",f"{hypothetical:.1f} MWhth")
        st.caption(f"Existing linear-model capacity: {actual:.1f} MWhth. "
                   "Difference is a **user assumption study**, NOT improved experimental accuracy.")
    except ValueError as exc:
        st.error(str(exc))
    st.info("NREL 84728 reports one characterized high-purity silica specimen "
            "(bulk density 1,543 kg/m³, measured heat-capacity curve and a "
            "quartz inversion near 573 °C). Those values do not validate "
            "the five illustrative app materials. Do not invent a phase-transition "
            "enthalpy spike without its digitized, sourced dataset.")
    st.link_button("Review NREL source (report 84728)",
                   "https://www.nrel.gov/docs/fy23osti/84728.pdf")

with insulation_tab:
    st.subheader("Two-layer insulation thermal resistance study")
    st.write("Explore independent inner/outer insulation assumptions. "
             "The cylinder side is radial conduction; the two caps use "
             "simplified plane conduction and outdoor convection.")
    a,b,c=st.columns(3)
    with a:
        inner_t=st.slider("Inner layer thickness (m)",0.05,1.0,0.25,0.05,key="layer_t1")
        inner_k=st.slider("Inner conductivity (W/mK)",0.02,0.3,0.09,0.01,key="layer_k1")
    with b:
        outer_t=st.slider("Outer layer thickness (m)",0.05,1.0,0.25,0.05,key="layer_t2")
        outer_k=st.slider("Outer conductivity (W/mK)",0.02,0.3,0.05,0.01,key="layer_k2")
    with c:
        ext_h=st.slider("Exterior convection (W/m²K)",2.0,30.0,10.0,1.0,key="layer_h")
        skin_t=st.slider("Assumed inner-face temperature (°C)",
                         float(d.ambient_c),float(d.maximum_c),
                         float(d.maximum_c),key="layer_inner")
    try:
        base=summarize(d,m)
        data=layered_cylinder(
            base["radius_m"],base["height_m"],
            (InsulationLayer(inner_t,inner_k,"Inner assumed layer"),
             InsulationLayer(outer_t,outer_k,"Outer assumed layer")),
            ext_h,skin_t,d.ambient_c,
        )
        a,b,c=st.columns(3)
        a.metric("Layered total UA",f"{d.modules*data['ua_total_w_k']:.1f} W/K")
        b.metric("Outer-side temperature",f"{data['outer_surface_c']:.1f} °C")
        c.metric("Total modeled heat leak",
                 f"{d.modules*data['total_loss_w']/1000:.1f} kW")
        ff=pd.DataFrame({
            "Radius (m)":data["radial_positions_m"],
            "Temperature (°C)":data["interface_temperatures_c"],
        })
        st.line_chart(ff.set_index("Radius (m)"),height=280)
        st.caption(f"Existing one-layer baseline UA: {base['ua_w_k']:.1f} W/K. "
                   "These models have different insulation properties and "
                   "are not experimentally calibrated alternatives.")
    except ValueError as exc:
        st.error(str(exc))


with convergence_tab:
    st.subheader("Analytic and numerical boundary checks")
    st.write("The 0-D constant-cp standby solution has an analytic Newton-cooling "
             "limit. Its comparison with the numerical solver is a software "
             "verification test, not evidence of plant temperature accuracy.")
    try:
        constant = replace(m, cp_slope=0.0)
        from math import exp
        cool = cooling_profile(d, constant, days=3,samples=21)
        mass = d.volume_m3 * constant.bulk_density
        ua = summarize(d, constant)["ua_w_k"]
        expected = d.ambient_c + (d.maximum_c-d.ambient_c)*exp(
            -3*86400*ua/(mass*constant.cp_25))
        st.metric("3-day constant-cp Newton analytical error",
                  f"{abs(cool['temperature_c'][-1]-expected):.3e} °C")
        st.caption("Constant-cp is a synthetic mathematical limit; it does not "
                   "remove real material-property uncertainty.")
    except (ValueError, RuntimeError) as exc:
        st.error(str(exc))
    charge_cut_grid = st.slider("Convergence charge cutoff (%)",
                                1, 50, 10,key="verify_grid_charge")
    discharge_cut_grid = st.slider("Convergence discharge cutoff (%)",
                                   20, 95, 70,key="verify_grid_discharge")
    if st.button("Run 16 / 32 / 64 cell refinement",type="primary",
                 key="verify_grid_run"):
        try:
            with st.spinner("Checking 1-D mesh sensitivity"):
                frame = _grid(d,m,charge_cut_grid,discharge_cut_grid)
            st.session_state["verify_grid_result"]=frame
            st.session_state["verify_grid_config"]=(d,m,charge_cut_grid,discharge_cut_grid)
        except (ValueError, RuntimeError) as exc:
            st.error(str(exc))
    if st.session_state.get("verify_grid_config")==(d,m,charge_cut_grid,discharge_cut_grid):
        frame=st.session_state["verify_grid_result"]
        st.dataframe(frame,hide_index=True,width="stretch")
        st.line_chart(frame.set_index("Axial cells")[["Delivered MWh(th)"]],height=270)
        st.caption("A small 16→32→64 change alone does not establish an "
                   "asymptotic grid convergence order or physical calibration.")
    st.caption("Model foundations: Bošnjaković & Santa (2026), "
               "DOI 10.3390/cleantechnol8050165; NREL 84728. "
               "Wakao et al. (1979) packed-bed correlations apply to different "
               "direct-contact regimes and are not assigned to this closed-pipe model.")

footer()

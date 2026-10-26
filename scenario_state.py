"""Shared Streamlit session state and one compact global scenario editor.

All pages receive the same committed Scenario. Draft controls in a form do not
change calculations until Apply is pressed. Session data are ephemeral.
"""
from __future__ import annotations
from dataclasses import asdict
import streamlit as st

from engine.materials import MATERIALS
from engine.scenarios import PRESETS, SLOTS, SOURCES, Scenario, from_mapping


def ensure_session() -> None:
    if "active_scenario" not in st.session_state:
        st.session_state["active_scenario"] = PRESETS["Industrial thermal store"]
    if "saved_scenarios" not in st.session_state:
        st.session_state["saved_scenarios"] = {slot: None for slot in SLOTS}
    if "scenario_epoch" not in st.session_state:
        st.session_state["scenario_epoch"] = 0


def active() -> Scenario:
    ensure_session()
    return st.session_state["active_scenario"]


def set_active(scenario: Scenario) -> None:
    scenario.validate()
    ensure_session()
    st.session_state["active_scenario"] = scenario
    st.session_state["scenario_epoch"] += 1
    # Reset local exploratory controls so the next page uses the shared input.
    for key in ("atlas_volume", "atlas_low", "atlas_high", "research_medium",
                "research_vol", "research_low", "research_high",
                "research_power", "research_load", "dl_inner", "dl_modules_3d"):
        st.session_state.pop(key, None)
    for key in ("tc_result", "tc_config", "research_ltne", "research_cfg",
                "candidate_results", "candidate_config", "v2_grid_results",
                "v2_loss_results"):
        st.session_state.pop(key, None)


def scenario_banner() -> None:
    s = active()
    st.caption(
        f"ACTIVE DESIGN · {s.name} · {s.material_name} · "
        f"{s.volume_m3:,.0f} m³ · {s.minimum_c:g}–{s.maximum_c:g} °C · "
        f"{s.source} (illustrative)"
    )


def sidebar_editor() -> None:
    scenario = active()
    with st.sidebar:
        st.markdown("**Active Scenario**")
        st.caption(f"{scenario.name} · {scenario.volume_m3:g} m³ · "
                   f"{scenario.material_name}")
        with st.expander("Edit shared design", expanded=False):
            # Epoch changes only when a validated design/preset is committed;
            # the edit widgets are re-created with current scenario defaults.
            with st.form(f"scenario_editor_{st.session_state['scenario_epoch']}"):
                name = st.text_input("Scenario name", value=scenario.name,
                                     max_chars=48)
                medium = st.selectbox(
                    "Material", list(MATERIALS),
                    index=list(MATERIALS).index(scenario.material_name))
                volume = st.number_input(
                    "Packed volume · m³", 50.0, 20000.0,
                    float(scenario.volume_m3), step=25.0)
                minimum = st.number_input(
                    "Minimum useful temperature · °C", 20.0, 200.0,
                    float(scenario.minimum_c), step=10.0)
                maximum = st.number_input(
                    "Maximum storage temperature · °C", 250.0, 800.0,
                    float(scenario.maximum_c), step=10.0)
                source = st.selectbox("Charge source", SOURCES,
                                      index=SOURCES.index(scenario.source))
                output = st.number_input(
                    "Thermal demand · MW", 0.1, 40.0,
                    float(scenario.thermal_output_mw), step=0.5)
                st.markdown("**Advanced geometry & source parameters**")
                with st.container(border=False):  # Group controls without nested expanders.
                    modules = st.number_input("Identical silos", 1, 16,
                                              int(scenario.modules))
                    ratio = st.slider("Height / inner radius", 1.0, 6.0,
                                      float(scenario.height_over_radius), 0.25)
                    insulation = st.slider("Insulation thickness · m", 0.1, 1.5,
                                            float(scenario.insulation_m), 0.05)
                    ambient = st.number_input(
                        "Ambient · °C", -25.0, 45.0, float(scenario.ambient_c))
                    hold = st.slider("Standby · days", 0.0, 30.0,
                                      float(scenario.hold_days), 0.5)
                    electric = st.number_input("Electric charging · MW",
                         0.2, 100.0, float(scenario.electric_mw), step=0.5)
                    aperture = st.number_input("CSP aperture · m²",
                         100.0, 150000.0, float(scenario.csp_aperture_m2), step=100.0)
                    dni = st.number_input("CSP DNI · W/m²", 100.0, 1400.0,
                         float(scenario.csp_dni_w_m2), step=25.0)
                    opt = st.slider("CSP efficiency", 0.1, 0.95,
                                     float(scenario.csp_efficiency), 0.05)
                    pv = st.number_input("PV rated · MWp", 0.0, 200.0,
                         float(scenario.pv_mwp), step=1.0)
                    pvcf = st.slider("PV capacity factor", 0.0, 0.6,
                                      float(scenario.pv_capacity_factor), 0.05)
                    wind = st.number_input("Wind rated · MW", 0.0, 200.0,
                         float(scenario.wind_mw), step=1.0)
                    windcf = st.slider("Wind capacity factor", 0.0, 0.75,
                                        float(scenario.wind_capacity_factor), 0.05)
                submitted = st.form_submit_button(
                    "Apply to all pages", type="primary", use_container_width=True)
            if submitted:
                data = asdict(scenario)
                data.update(
                    name=name, material_name=medium, volume_m3=volume,
                    minimum_c=minimum, maximum_c=maximum,
                    source=source, thermal_output_mw=output,
                    modules=modules, height_over_radius=ratio,
                    insulation_m=insulation, ambient_c=ambient,
                    hold_days=hold, electric_mw=electric,
                    csp_aperture_m2=aperture, csp_dni_w_m2=dni,
                    csp_efficiency=opt, pv_mwp=pv, pv_capacity_factor=pvcf,
                    wind_mw=wind, wind_capacity_factor=windcf,
                )
                try:
                    set_active(from_mapping(data))
                    st.rerun()
                except ValueError as exc:
                    st.error(str(exc))
        st.caption("Changes affect all workspaces only after Apply. "
                   "For saved A/B/C comparisons, open Scenario Manager.")

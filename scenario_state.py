"""Shared Streamlit session state and one compact global scenario editor.

All pages receive the same committed Scenario. Draft controls in a form do not
change calculations until Apply is pressed. Session data are ephemeral.
"""
from __future__ import annotations
from dataclasses import asdict
from html import escape
import streamlit as st
from localization import tr

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
    """Shared compact scenario ribbon; labels are escaped before HTML use."""
    s = active()
    pills = [
        s.material_name,
        f"{s.volume_m3:,.0f} m³",
        f"{s.minimum_c:g}–{s.maximum_c:g} °C",
        f"{s.charge_power_mw():,.2f} MW " + tr("charge","şarj"),
        s.source,
    ]
    content = "".join(
        '<span class="sb-chip">' + escape(str(value)) + '</span>'
        for value in pills
    )
    st.html(
        '<div class="sb-context" role="note" aria-label="Active design details">' +
        tr('<span class="sb-context-label">ACTIVE DESIGN</span>','<span class="sb-context-label">AKTİF TASARIM</span>') +
        '<strong style="font-size:.85rem;color:#fff">'
        + escape(s.name) + '</strong>' + content + '</div>'
    )


def sidebar_editor() -> None:
    scenario = active()
    with st.sidebar:
        st.markdown(tr("**Active Scenario**","**Aktif senaryo**"))
        st.caption(f"{scenario.name} · {scenario.volume_m3:g} m³ · "
                   f"{scenario.material_name}")
        with st.expander(tr("Edit shared design","Ortak tasarımı düzenle"), expanded=False):
            # Epoch changes only when a validated design/preset is committed;
            # the edit widgets are re-created with current scenario defaults.
            with st.form(f"scenario_editor_{st.session_state['scenario_epoch']}"):
                name = st.text_input(tr("Scenario name","Senaryo adı"), value=scenario.name,
                                     max_chars=48)
                medium = st.selectbox(
                    tr("Material","Malzeme"), list(MATERIALS),
                    index=list(MATERIALS).index(scenario.material_name))
                volume = st.number_input(
                    tr("Packed volume · m³","Dolu hacim · m³"), 50.0, 20000.0,
                    float(scenario.volume_m3), step=25.0)
                minimum = st.number_input(
                    tr("Minimum useful temperature · °C","Minimum kullanılabilir sıcaklık · °C"), 20.0, 200.0,
                    float(scenario.minimum_c), step=10.0)
                maximum = st.number_input(
                    tr("Maximum storage temperature · °C","Maksimum depolama sıcaklığı · °C"), 250.0, 800.0,
                    float(scenario.maximum_c), step=10.0)
                source = st.selectbox(tr("Charge source","Şarj kaynağı"), SOURCES,
                                      index=SOURCES.index(scenario.source))
                output = st.number_input(
                    tr("Thermal demand · MW","Isı talebi · MW"), 0.1, 40.0,
                    float(scenario.thermal_output_mw), step=0.5)
                st.markdown("**Advanced geometry & source parameters**")
                with st.container(border=False):  # Group controls without nested expanders.
                    modules = st.number_input(tr("Identical silos","Özdeş depolar"), 1, 16,
                                              int(scenario.modules))
                    ratio = st.slider(tr("Height / inner radius","Yükseklik / iç yarıçap"), 1.0, 6.0,
                                      float(scenario.height_over_radius), 0.25)
                    insulation = st.slider(tr("Insulation thickness · m","Yalıtım kalınlığı · m"), 0.1, 1.5,
                                            float(scenario.insulation_m), 0.05)
                    ambient = st.number_input(
                        tr("Ambient · °C","Ortam · °C"), -25.0, 45.0, float(scenario.ambient_c))
                    hold = st.slider(tr("Standby · days","Bekleme · gün"), 0.0, 30.0,
                                      float(scenario.hold_days), 0.5)
                    electric = st.number_input(tr("Electric charging · MW","Elektrikle şarj · MW"),
                         0.2, 100.0, float(scenario.electric_mw), step=0.5)
                    aperture = st.number_input(tr("CSP aperture · m²","Yoğunlaştırılmış güneş açıklığı · m²"),
                         100.0, 150000.0, float(scenario.csp_aperture_m2), step=100.0)
                    dni = st.number_input(tr("CSP DNI · W/m²","Doğrudan güneş ışınımı · W/m²"), 100.0, 1400.0,
                         float(scenario.csp_dni_w_m2), step=25.0)
                    opt = st.slider(tr("CSP efficiency","CSP verimi"), 0.1, 0.95,
                                     float(scenario.csp_efficiency), 0.05)
                    pv = st.number_input(tr("PV rated · MWp","Güneş PV nominal gücü · MWp"), 0.0, 200.0,
                         float(scenario.pv_mwp), step=1.0)
                    pvcf = st.slider(tr("PV capacity factor","PV kapasite faktörü"), 0.0, 0.6,
                                      float(scenario.pv_capacity_factor), 0.05)
                    wind = st.number_input(tr("Wind rated · MW","Rüzgâr nominal gücü · MW"), 0.0, 200.0,
                         float(scenario.wind_mw), step=1.0)
                    windcf = st.slider(tr("Wind capacity factor","Rüzgâr kapasite faktörü"), 0.0, 0.75,
                                        float(scenario.wind_capacity_factor), 0.05)
                submitted = st.form_submit_button(
                    tr("Apply to all pages","Tüm sayfalara uygula"), type="primary", width="stretch")
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

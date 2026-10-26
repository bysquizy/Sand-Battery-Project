"""Stage 4 — light web-native scientific visualizations and reproducible reports.

Every 3-D color frame is a cylindrical rendering of a numerically solved 1-D
axial profile: this is *not* a radial CFD field or measured sensor data.
Heavy models run only after a user clicks Run, then are cached by inputs.
"""
from __future__ import annotations

from dataclasses import replace
import pandas as pd
import streamlit as st

from engine.materials import MATERIALS
from engine.physics import simulate_cycle, summarize
from engine.thermocline import simulate_thermocline
from engine.report_exports import html_report, pdf_report
from engine.scenarios import SLOTS, to_json
from scenario_state import active, scenario_banner
from visuals import timeline, ledger
from visuals_advanced import (
    axial_cylinder_animation, axial_history_heatmap, design_frontier_chart,
    sensitivity_tornado,
)
from ui_theme import inject, hero, footer
from localization import tr

st.set_page_config(page_title="Visual Story Studio | Sand Battery Studio",
                   page_icon="🎬", layout="wide")
inject()
hero(tr("VISUALS / THERMAL INSIGHT","GÖRSELLER / ISIL ANALİZ"), tr("Visual Story Studio","Görsel Analiz"), tr("Watch computed thermal fronts, compare design options and publish a reproducible engineering snapshot.","Hesaplanan sıcaklık dağılımlarını izleyin, tasarımları karşılaştırın ve rapor oluşturun."))
scenario = active()
scenario_banner()
d = scenario.make_design()
m = MATERIALS[scenario.material_name]
st.write(tr("Explore model-linked thermal animation, energy flows, design tradeoffs and downloadable engineering reports.","Model tabanlı ısıl animasyonları, enerji akışlarını, tasarım karşılaştırmalarını ve indirilebilir mühendislik raporlarını inceleyin."))
st.warning(tr("Every chart is an illustrative simulation. The 3D color field maps a computed 1-D axial profile around a cylinder; radial gradients are **not** solved and no measured sensors exist.","Tüm grafikler temsili sayısal simülasyondur. 3B renk görünümü, hesaplanmış 1B eksenel sıcaklık profilini silindire yansıtır; radyal gradyanlar çözülmez ve gerçek sensör ölçümü kullanılmaz."))

workspace = st.radio(
    tr("Visualization workspace","Görselleştirme çalışma alanı"),
    (tr("Thermal playback","Isıl animasyon"), tr("Energy & sensitivities","Enerji ve duyarlılık"), tr("Design tradeoffs","Tasarım ödünleşimleri"),
     tr("Engineering report","Mühendislik raporu")),
    horizontal=True, label_visibility="collapsed", key="visual_workspace",
)

@st.cache_data(max_entries=8, ttl=1200, show_spinner=False)
def _axial(design, material, count):
    return simulate_thermocline(design, material, n_cells=count)


@st.cache_data(max_entries=18, ttl=1800, show_spinner=False)
def _cycle(design, material):
    return simulate_cycle(design, material, max_step_s=3600)


@st.cache_data(max_entries=8, ttl=1200, show_spinner=False)
def _frontier(design, material):
    rows = []
    volumes = sorted(set(
        min(20000., max(50., design.volume_m3*factor))
        for factor in (.55,.8,1.0,1.25)
    ))
    insulation = sorted(set(
        min(1.5, max(.1, value)) for value in (.3,.5,.8,design.insulation_m)
    ))
    for vol in volumes:
        for thick in insulation:
            design_i = replace(design, volume_m3=vol, insulation_m=thick)
            try:
                out = _cycle(design_i, material)
            except (ValueError, RuntimeError):
                # At fixed source power some candidate designs cannot charge.
                continue
            rows.append({
                "volume_m3":vol, "insulation_m":thick,
                "modules":design_i.modules,
                "initial_loss_kw":out["initial_loss_kw"],
                "useful_heat_mwh":out["useful_heat_mwh"],
                "source_input_mwh":out["source_input_mwh"],
            })
    return rows


@st.cache_data(max_entries=8, ttl=1200, show_spinner=False)
def _sensitivity(design, material):
    baseline = _cycle(design, material)["useful_heat_mwh"]
    results = []
    for name, property_name in (
        ("Packed volume", "volume_m3"),
        ("Insulation thickness", "insulation_m"),
        ("Charging power", "charge_mw"),
        ("Thermal demand", "thermal_output_mw"),
    ):
        val = getattr(design, property_name)
        def one(factor):
            new=replace(design, **{property_name:val*factor})
            try:
                return _cycle(new, material)["useful_heat_mwh"]
            except (RuntimeError, ValueError):
                return float("nan")
        low, high = one(.9), one(1.1)
        if pd.notna(low) and pd.notna(high):
            results.append({"parameter":name,"low_mwh":low,"high_mwh":high})
    return baseline, results


if workspace == tr("Thermal playback","Isıl animasyon"):
    st.subheader(tr("Computed axial temperature evolution","Hesaplanan eksenel sıcaklık değişimi"))
    c1,c2 = st.columns([1,2])
    with c1:
        cells=st.slider(tr("Axial finite-volume cells","Eksenel sonlu hacim hücreleri"),16,64,24,8,key="visual_cells")
        lite=st.toggle(tr("2D-only / mobile-friendly view","Yalnızca 2B / mobil uyumlu görünüm"),value=False,key="visual_lite")
        st.caption(tr("Run explicitly to avoid heavy CPU usage on slider changes.","Kaydırıcı değiştiğinde yoğun işlemci kullanımını önlemek için hesaplamayı düğmeyle başlatın."))
        run=st.button(tr("Solve & build thermal playback","Hesapla ve ısıl animasyonu oluştur"),type="primary",key="visual_run_thermal")
    with c2:
        st.info(tr("The snapshots come from the 1-D LTE charge / standby / discharge solver, including its specified 10%/70% cutoff assumptions. The animation represents axial state, **not an instrumented 3D thermal measurement**.","Görüntüler 1B LTE şarj / bekleme / deşarj çözümünden üretilir. %10/%70 kesme varsayımları kullanılır. Animasyon yalnızca eksenel durumu gösterir; **ölçülmüş bir 3B sıcaklık alanı değildir**."))
    cfg=(d,m,cells)
    if run:
        try:
            with st.spinner("Computing finite-volume time slices"):
                st.session_state["visual_animation_result"]=_axial(*cfg)
                st.session_state["visual_animation_cfg"]=cfg
        except (ValueError, RuntimeError, OverflowError) as exc:
            st.error(f"Thermal animation calculation failed: {exc}")
    if st.session_state.get("visual_animation_cfg")==cfg:
        field=st.session_state["visual_animation_result"]
        a,b,c = st.columns(3)
        a.metric(tr("Charging duration","Şarj süresi"),f"{field['charge_h']:.1f} h")
        b.metric(tr("Useful thermal heat","Kullanılabilir ısı"),f"{field['useful_heat_mwh']:.1f} MWhth")
        c.metric(tr("Energy ledger residual","Enerji dengesi kalanı"),f"{field['energy_balance_residual_mwh']:.2e} MWh")
        if not lite:
            st.plotly_chart(axial_cylinder_animation(
                field, float(summarize(d,m)["radius_m"]),
                d.minimum_c,d.maximum_c),width="stretch",
                key="visual_axial_3d")
        st.subheader("Time–height temperature field")
        st.plotly_chart(axial_history_heatmap(field),width="stretch",
                        key="visual_axial_map")
        st.caption("Snapshots are computed, not interpolated animation guesses. "
                   "This model is direct-contact LTE and does not represent "
                   "a validated closed-loop pipe installation.")
        frame=pd.DataFrame(field["animation_profiles_c"],
                           columns=[f"height_{z:.2f}_m" for z in field["z_m"]])
        frame.insert(0,"elapsed_time_h",field["animation_times_h"])
        frame.insert(1,"phase",field["animation_phases"])
        st.download_button("Download computed temperature snapshots · CSV",
                           frame.to_csv(index=False),
                           file_name="axial_temperature_snapshots.csv",
                           mime="text/csv",key="visual_axial_csv",
                           on_click="ignore")
    else:
        st.caption("Run the 1-D solver to reveal real computed animation frames.")

elif workspace == tr("Energy & sensitivities","Enerji ve duyarlılık"):
    st.subheader("Thermal energy and assumption sensitivity")
    try:
        r=_cycle(d,m)
        st.plotly_chart(timeline(r),width="stretch",key="visual_0d_trace")
        energy=ledger(r)
        if energy is not None:
            st.plotly_chart(energy,width="stretch",key="visual_energy_ledger")
        if st.button(tr("Compute ±10% input sensitivity","±%10 girdi duyarlılığını hesapla"),
                     type="primary",key="visual_run_sensitivity"):
            with st.spinner("Recalculating controlled input perturbations"):
                st.session_state["visual_sensitivity"]=_sensitivity(d,m)
                st.session_state["visual_sensitivity_cfg"]=(d,m)
        if st.session_state.get("visual_sensitivity_cfg")==(d,m):
            baseline, rows=st.session_state["visual_sensitivity"]
            if rows:
                st.plotly_chart(sensitivity_tornado(baseline,rows),
                                width="stretch",key="visual_tornado")
                st.dataframe(pd.DataFrame(rows),hide_index=True,width="stretch")
            else:
                st.info("No numerically feasible ±10% candidates were found.")
        st.caption("The sensitivity is a local deterministic model comparison, "
                   "NOT statistical measurement uncertainty.")
    except (RuntimeError, ValueError) as exc:
        st.error(f"Unable to evaluate active scenario: {exc}")

elif workspace == tr("Design tradeoffs","Tasarım ödünleşimleri"):
    st.subheader("Thermal capacity vs envelope heat-loss tradeoff")
    st.write("Screen at most 16 variations of the active design's volume and "
             "insulation. The reported heat is recomputed by the same 0-D solver; "
             "it is not a globally optimized engineering solution.")
    if st.button(tr("Screen design alternatives","Tasarım alternatiflerini tara"),type="primary",key="visual_run_frontier"):
        with st.spinner("Solving bounded design comparisons"):
            st.session_state["visual_frontier"]=_frontier(d,m)
            st.session_state["visual_frontier_cfg"]=(d,m)
    if st.session_state.get("visual_frontier_cfg")==(d,m):
        records=st.session_state["visual_frontier"]
        if records:
            st.plotly_chart(design_frontier_chart(records),width="stretch",
                            key="visual_frontier_chart")
            data=pd.DataFrame(records)
            st.dataframe(data,hide_index=True,width="stretch")
            st.download_button("Export alternative designs · CSV",
                               data.to_csv(index=False),
                               file_name="sand_battery_design_tradeoffs.csv",
                               mime="text/csv",key="visual_frontier_csv",
                               on_click="ignore")
        else:
            st.error("No feasible candidate design under the selected source constraints.")
    else:
        st.caption("Run the design screen to display the source-constrained tradeoff.")

elif workspace == tr("Engineering report","Mühendislik raporu"):
    st.subheader("Publish a reproducible scenario snapshot")
    st.write("Download the active model inputs and its freshly computed "
             "charging–holding–discharging results. The offline HTML contains "
             "a calculated vector chart, inputs, full energy ledger, team "
             "credits and selected citation links. The compact PDF is a "
             "text-first version with the same principal numbers.")
    try:
        result=_cycle(d,m)
    except (RuntimeError, ValueError) as exc:
        st.error(f"Cannot make a report for this scenario: {exc}")
    else:
        cols=st.columns(3)
        cols[0].metric(tr("Theoretical capacity","Teorik kapasite"),f"{result['capacity_mwh']:.1f} MWhth")
        cols[1].metric(tr("Useful delivered heat","Kullanılabilir ısı çıkışı"),f"{result['useful_heat_mwh']:.1f} MWhth")
        cols[2].metric(tr("Energy conservation residual","Enerji korunumu kalanı"),
                       f"{result['energy_balance_residual_mwh']:.2e} MWh")
        with st.spinner("Building self-contained report formats"):
            html=html_report(scenario,result)
            pdf=pdf_report(scenario,result)
        col1,col2,col3=st.columns(3)
        col1.download_button(
            "Download illustrated HTML",
            html, file_name="Sand_Battery_Engineering_Report.html",
            mime="text/html", key="visual_report_html", on_click="ignore",
            use_container_width=True)
        col2.download_button(
            "Download compact PDF",
            pdf, file_name="Sand_Battery_Engineering_Report.pdf",
            mime="application/pdf",key="visual_report_pdf",
            on_click="ignore",use_container_width=True)
        col3.download_button(
            "Download editable scenario JSON",
            to_json(scenario, {slot:None for slot in SLOTS}),
            file_name="Sand_Battery_Scenario.json",
            mime="application/json",key="visual_report_json",
            on_click="ignore",use_container_width=True)
        st.caption("HTML uses UTF-8 and preserves team names; PDF is an "
                   "offline basic-font print version and may transliterate "
                   "non-ASCII characters. HTML can also be printed to PDF "
                   "with full browser typography. All results are model-generated.")

footer()

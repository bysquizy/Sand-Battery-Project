"""Compare up to three numerically calculated browser-session designs.

This does not write to the cloud filesystem. Import/export uses bounded JSON
with a version and strict named fields; data are not executable Python.
"""
from __future__ import annotations
import pandas as pd
import streamlit as st

from engine.materials import MATERIALS
from engine.export_safety import safe_csv
from engine.physics import simulate_cycle
from engine.scenarios import SLOTS, MAX_IMPORT_BYTES, from_json, to_json
from scenario_state import active, ensure_session, set_active, scenario_banner
from ui_theme import inject, hero, footer
from localization import tr

st.set_page_config(page_title="Scenario Manager | Sand Battery Studio",
                   page_icon="🗂️",layout="wide")
inject()
ensure_session()
hero(tr("SCENARIOS / DESIGN COMPARISON","SENARYOLAR / TASARIM KARŞILAŞTIRMASI"), tr("Scenario Manager","Senaryo Yöneticisi"), tr("Save three designs, compare simulated performance and export portable, validated scenarios.","Üç tasarımı kaydedin, simülasyon sonuçlarını karşılaştırın ve senaryoları dışa aktarın."))
scenario_banner()
st.write(tr('Save up to three versions of your design, compare like-for-like model results, or export a versioned JSON bundle.', 'Tasarımınızın en fazla üç sürümünü kaydedin, model sonuçlarını karşılaştırın veya sürümlü JSON paketi indirin.'))
st.info(tr('Saved scenarios last for this browser session only. Download JSON to keep your work. All comparisons are numerical scenarios, not field data.', 'Senaryolar yalnızca mevcut oturumda saklanır; sayfayı yenilemek veya bağlantının kopması kayıtları silebilir. Çalışmanızı korumak için JSON indirin. Karşılaştırmalar saha ölçümü değil, sayısal senaryolardır.'))

slots = st.session_state["saved_scenarios"]
columns = st.columns(3)
for col, slot in zip(columns, SLOTS):
    with col:
        with st.container(border=True):
            saved = slots[slot]
            st.markdown(tr(f"### Scenario {slot}", f"### Senaryo {slot}"))
            st.write(saved.name if saved else tr("Empty slot", "Boş yuva"))
            if saved:
                st.caption(f"{saved.material_name} · {saved.volume_m3:,.0f} m³ · "
                           f"{saved.maximum_c:g} °C")
            if st.button(tr(f"Save active → {slot}", f"Aktif senaryoyu kaydet → {slot}"),key=f"slot_save_{slot}",
                         use_container_width=True):
                slots[slot] = active()
                st.rerun()
            if st.button(tr(f"Load {slot} as active", f"{slot} senaryosunu uygula"),key=f"slot_load_{slot}",
                         disabled=saved is None,use_container_width=True):
                set_active(saved)
                st.rerun()
            if st.button(tr(f"Clear {slot}", f"{slot} yuvasını temizle"),key=f"slot_clear_{slot}",
                         disabled=saved is None,use_container_width=True):
                slots[slot] = None
                st.rerun()


@st.cache_data(max_entries=18, ttl=1200, show_spinner=False)
def _comparison(scenario):
    design = scenario.make_design()
    out = simulate_cycle(design, MATERIALS[scenario.material_name],
                         max_step_s=3600)
    return {
        "Capacity (MWhth)": float(out["capacity_mwh"]),
        "Useful heat (MWhth)": float(out["useful_heat_mwh"]),
        "Initial loss (kW)": float(out["initial_loss_kw"]),
        "Delivered / source (%)": float(out["source_to_useful_heat_pct"]),
        "Discharge (h)": float(out["discharge_hours"]),
        "Energy residual (MWh)": float(out["energy_balance_residual_mwh"]),
    }


st.subheader(tr('Compare saved designs', 'Kayıtlı tasarımları karşılaştırın'))
rows = []
for slot, scenario in slots.items():
    if scenario is None:
        continue
    row = {
        "Slot":slot, "Name":scenario.name, "Material":scenario.material_name,
        "Volume (m³)":scenario.volume_m3, "Tmin (°C)":scenario.minimum_c,
        "Tmax (°C)":scenario.maximum_c, "Charging source":scenario.source,
        "Thermal demand (MW)":scenario.thermal_output_mw,
    }
    try:
        row.update(_comparison(scenario))
    except (ValueError, RuntimeError, OverflowError, ZeroDivisionError) as exc:
        row["Simulation status"] = f"Unavailable: {exc}"
    else:
        row["Simulation status"] = "Simulated"
    rows.append(row)
if rows:
    df = pd.DataFrame(rows)
    st.dataframe(df,hide_index=True,width="stretch")
    st.caption(tr("Comparisons preserve each saved scenario's own geometry, material and operating boundaries; results are not normalized unless the inputs were intentionally made equal.", 'Her kayıtlı senaryonun kendi geometrisi, malzemesi ve çalışma sınırları korunur. Girdiler eşitlenmedikçe sonuçlar normalize edilmez.'))
    st.download_button(tr('Export comparison · CSV', 'Karşılaştırmayı indir · CSV'),safe_csv(df),
       file_name="sand_battery_comparison.csv",mime="text/csv",
       key="manager_compare_csv")
    good = df[df["Simulation status"]=="Simulated"]
    if not good.empty:
        st.bar_chart(good.set_index("Slot")[["Capacity (MWhth)",
                                           "Useful heat (MWhth)"]],height=280)
else:
    st.caption(tr('Save your active design into A, B or C to begin comparing.', 'Karşılaştırmaya başlamak için aktif tasarımı A, B veya C yuvasına kaydedin.'))

st.divider()
st.subheader(tr('Portable scenario bundle', 'Taşınabilir senaryo paketi'))
st.download_button(
    tr('Download active + A/B/C · JSON', 'Aktif senaryo + A/B/C indir · JSON'),
    to_json(active(),slots),
    file_name="sand_battery_scenarios_v1.json",
    mime="application/json",key="manager_export")
upload = st.file_uploader(tr('Import your versioned scenario JSON (max 40 kB)', 'Sürümlü senaryo JSON dosyası yükleyin (en fazla 40.000 bayt)'),
                          type="json", key="scenario_json_upload", max_upload_size=1)
st.caption(tr("The file picker transfers up to 1 MB; scenario validation accepts at most 40,000 bytes.",
              "Dosya seçici 1 MB’a kadar aktarabilir; senaryo denetimi en fazla 40.000 bayt kabul eder."))
if upload is not None:
    if upload.size > MAX_IMPORT_BYTES:
        st.error(tr('Scenario bundle exceeds the 40 kB safety limit.', 'Senaryo paketi 40.000 bayt güvenlik sınırını aşıyor. Mevcut senaryolar değiştirilmedi.'))
    else:
        try:
            parsed_active,parsed_slots = from_json(upload.getvalue())
        except ValueError as exc:
            st.error(tr(f"Cannot import scenario: {exc}", f"Senaryo yüklenemedi: {exc}"))
        else:
            st.success(tr('Valid scenario bundle. Review the name before applying.', 'Senaryo paketi geçerli. Uygulamadan önce tasarım adını kontrol edin.'))
            st.caption(f"Active: {parsed_active.name} · "
                       f"{parsed_active.material_name} · "
                       f"{parsed_active.volume_m3:g} m³")
            st.warning(tr("Applying replaces the active design AND all A/B/C slots. Download your current bundle first if you need to keep it.",
                          "Uygulamak aktif tasarımı VE tüm A/B/C yuvalarını değiştirir. Mevcut çalışmanızı korumak için önce JSON paketini indirin."))
            if st.button(tr('Replace active design and saved slots', 'Aktif tasarımı ve kayıtlı yuvaları değiştir'),
                         type="primary",key="manager_import_apply"):
                st.session_state["saved_scenarios"] = parsed_slots
                set_active(parsed_active)
                st.rerun()
st.caption(tr('JSON files are validated against the current schema. No imported scripts, object serialization, untrusted code or local paths run.', 'JSON dosyaları mevcut şemaya göre denetlenir. Yüklenen betikler, serileştirilmiş nesneler veya yerel dosya yolları çalıştırılmaz.'))

footer()

"""Sand Battery Studio — bilingual academic engineering dashboard.

ESE101 Group 8. No AI service calls or heavy ML frameworks.
The demo visualizations do not constitute product certification.
"""
import json
from dataclasses import asdict
import numpy as np
import pandas as pd
import streamlit as st

from engine.materials import MATERIALS
from engine.physics import simulate_cycle
from engine.thermocline import simulate_thermocline
from engine.optimization import screen_designs
from visuals import timeline, ledger, plant_3d, material_comparison, thermocline_plot, optimization_scatter
from engine.reporting import scenario_markdown
from project_version import APP_VERSION
from engine.scenarios import PRESETS, SLOTS, to_json
from scenario_state import active, set_active, scenario_banner

st.set_page_config(page_title='Sand Battery Studio | Engineering Workspace',page_icon='🌡️',
                   layout='wide',initial_sidebar_state='expanded')

from ui_theme import inject, hero, footer
from localization import tr
inject()


@st.cache_data(max_entries=24,ttl=1800,show_spinner=False)
def _cached_cycle(d,m):
    """Reuse a valid scenario instead of re-solving on every UI rerun."""
    return simulate_cycle(d,m)

DEMO_PRESETS = tuple(PRESETS)

# All numerical pages now consume the same committed, validated design.
# The global editor lives in streamlit_app.py's sidebar.
with st.sidebar:
    preset_name = st.selectbox(
        tr("Illustrative presentation scenario","Örnek simülasyon senaryosu"),DEMO_PRESETS,key="demo_preset")
    st.caption(tr('Example configurations only — not measured Finnish plants.', 'Yalnızca örnek yapılandırmalardır; Finlandiya tesislerinin ölçüm verileri değildir.'))
    if st.button(tr("Use selected preset","Seçili senaryoyu uygula"), key="home_apply_preset",
                 use_container_width=True):
        set_active(PRESETS[preset_name])
        st.rerun()
    lightweight = st.toggle(
        tr("Light mode (skip 3D animation)","Hafif mod (3B animasyonu atla)"), value=False, key="low_power_mode",
        help=tr('Useful for mobile or lower-power devices.', 'Mobil veya düşük güçlü cihazlar için uygundur.'))
    st.caption(tr('Edit volume, temperatures, modules and charging inputs in the shared Active Scenario editor above.', 'Hacim, sıcaklık, depo sayısı ve şarj girdilerini yukarıdaki ortak Aktif senaryo düzenleyicisinden değiştirin.'))

current_scenario = active()
scenario_banner()

hero(
    tr("GROUP 8 · SAND BATTERY PROJECT","GRUP 8 · KUM BATARYASI PROJESİ"),
    tr("Sand Battery Thermal Storage Simulation","Kum Bataryası Isı Depolama Simülasyonu"),
    tr("An academic project for modeling sand-based thermal energy storage, heat losses, charging and discharging, and insulation design.","Kumla ısı depolama, ısı kayıpları, şarj-deşarj ve yalıtım tasarımı üzerine sayısal mühendislik projesi."),
)
st.caption(tr("Academic numerical model · Not experimentally validated", "Akademik sayısal model · Deneysel olarak doğrulanmamıştır"))
st.link_button(tr("GitHub: Project files and research","GitHub: Proje dosyaları ve araştırma"),
               "https://github.com/bysquizy/Sand-Battery-Project")
st.caption(tr('Open Research Hub for source attribution and methods. Visual Story Studio provides model-driven animations and downloadable reports.', 'Kaynaklar ve yöntemler için Araştırma Merkezi’ni açın. Görsel Analiz sayfasında model tabanlı animasyonlar ve indirilebilir raporlar bulunur.'))

try:
    design = current_scenario.make_design()
    material = MATERIALS[current_scenario.material_name]
    tmin = current_scenario.minimum_c
    tmax = current_scenario.maximum_c
    result = _cached_cycle(design, material)
except (ValueError, RuntimeError, OverflowError, ZeroDivisionError) as exc:
    st.error(tr(f"This configuration cannot be simulated: {exc}", f"Bu yapılandırma hesaplanamıyor: {exc}"))
    st.info(tr('Adjust the active design, source power or temperature limits in the shared sidebar editor.', 'Yan menüdeki ortak düzenleyiciden aktif tasarımı, kaynak gücünü veya sıcaklık sınırlarını değiştirin.'))
    st.stop()

if tmax>570 and 'silica' in material.name.lower():
    st.warning(tr('Quartz transforms near 573 °C. The illustrative linear specific-heat model does not represent this phase transition. Validate material data before using this temperature regime.', 'Kuvars yaklaşık 573 °C’de dönüşüm geçirir. Temsili doğrusal özgül ısı modeli bu faz dönüşümünü içermez. Bu sıcaklıklarda kullanmadan önce malzeme verilerini doğrulayın.'))

c1,c2,c3,c4=st.columns(4)
c1.metric(tr("THEORETICAL HEAT CAPACITY","TEORİK ISI KAPASİTESİ"),f"{result['capacity_mwh']:,.1f} MWh")
c2.metric(tr("DELIVERED USEFUL HEAT","KULLANILABİLİR ISI ÇIKIŞI"),f"{result['useful_heat_mwh']:,.1f} MWh")
c3.metric(tr("SOURCE → USEFUL HEAT","KAYNAKTAN YARARLI ISIYA"),f"{result['source_to_useful_heat_pct']:.1f}%")
c4.metric(tr("INITIAL THERMAL LOSS","BAŞLANGIÇ ISI KAYBI"),f"{result['initial_loss_kw']:.1f} kW")

# Render only the selected workspace so costly 3D figures and thermal
# screening calculations are not reconstructed on every widget interaction.
view = st.radio(
    tr("Engineering workspace","Mühendislik çalışma alanı"),
    ('Overview', 'Thermal Dynamics', '3D Plant Explorer', 'Materials & Optimization'),
    format_func={key: tr(key, translated) for key, translated in {'Overview': 'Genel bakış', 'Thermal Dynamics': 'Isıl dinamikler', '3D Plant Explorer': '3B tesis görünümü', 'Materials & Optimization': 'Malzemeler ve optimizasyon'}.items()}.__getitem__,
    key="home_workspace", horizontal=True, label_visibility="collapsed",
)
if view == 'Overview':
    a,b=st.columns([1.45,1],gap='large')
    with a:
        st.markdown(tr('<div class="sect">Operating temperature profile</div>','<div class="sect">Çalışma sıcaklığı profili</div>'),unsafe_allow_html=True)
        st.plotly_chart(timeline(result),width='stretch',key='chart_overview_timeline')
    with b:
        st.markdown(tr('<div class="sect">Energy distribution</div>','<div class="sect">Enerji dağılımı</div>'),unsafe_allow_html=True)
        flow=ledger(result)
        if flow is not None:
            st.plotly_chart(flow,width='stretch',key='chart_overview_ledger')
        else:
            st.info(tr('Standby cooled below the minimum useful temperature. A nonnegative Sankey cannot represent this reference state; use the ledger below.', 'Bekleme sırasında sıcaklık minimum kullanılabilir sıcaklığın altına düştü. Bu referans durumu Sankey grafiğinde gösterilemiyor; aşağıdaki enerji bilançosunu kullanın.'))
    c1,c2,c3,c4=st.columns(4)
    c1.metric(tr("Charge time","Şarj süresi"),f"{result['charge_hours']:,.1f} h")
    c2.metric(tr("Autonomy at rated output","Nominal çıkışta çalışma süresi"),f"{result['discharge_hours']:,.1f} h")
    c3.metric(tr("Mass of storage medium","Depolama malzemesi kütlesi"),f"{result['mass_t']:,.0f} t")
    c4.metric(tr("Energy-balance residual","Enerji dengesi kalanı"),f"{result['energy_balance_residual_mwh']:.2e} MWh")
    with st.expander(tr('ENERGY ACCOUNTING — see all flows', 'ENERJİ BİLANÇOSU — tüm akışları göster')):
        df=pd.DataFrame([{'Term':'Modeled source energy supplied (MWh)','Energy':result['source_input_mwh']},
            {'Term':'Charging conversion loss (MWh)','Energy':result['heater_loss_mwh']},
            {'Term':'Charge-phase ambient loss (MWh)','Energy':result['charge_loss_mwh']},
            {'Term':'Standby ambient loss (MWh)','Energy':result['standby_loss_mwh']},
            {'Term':'Discharge ambient loss (MWh)','Energy':result['discharge_loss_mwh']},
            {'Term':'Useful thermal delivery (MWh)','Energy':result['useful_heat_mwh']},
            {'Term':'Remaining energy relative to Tmin (MWh)','Energy':result['ending_relative_energy_mwh']}])
        st.dataframe(df,hide_index=True,width='stretch')
    st.caption(tr('Energy Sankey and time series represent simulated flows. Reported conservation residual checks numerical accounting, not agreement with measured hardware.', 'Sankey ve zaman grafikleri simülasyon akışlarını gösterir. Enerji dengesi kalanı sayısal hesabı denetler; gerçek donanım ölçümleriyle uyumu kanıtlamaz.'))
    st.markdown('<div class="info-line"><b>Interpretation:</b> Theoretical sensible heat assumes the full selected temperature interval. The useful-heat result additionally includes ambient losses, but assumes a constant-temperature-grade heat consumer down to the set minimum. It is not a measured plant output.</div>',unsafe_allow_html=True)

elif view == 'Thermal Dynamics':
    st.markdown(tr('<div class="sect">Transient response · 0-D energy balance</div>','<div class="sect">Geçici rejim · 0B enerji dengesi</div>'),unsafe_allow_html=True)
    st.plotly_chart(timeline(result),width='stretch',key='chart_thermal_timeline')
    st.markdown(tr('<div class="sect">1-D thermocline · exploratory comparison</div>','<div class="sect">1B termoklin · karşılaştırma</div>'),unsafe_allow_html=True)
    st.caption(tr('Finite-volume direct-contact/local-thermal-equilibrium model. This is NOT a validated simulation of Polar Night Energy’s closed-loop air pipes.', 'Sonlu hacim tabanlı doğrudan temas/yerel ısıl denge modeli. Polar Night Energy’nin kapalı çevrim hava borularının doğrulanmış simülasyonu değildir.'))
    cells=st.slider(tr("Axial resolution · cells","Eksenel çözünürlük · hücre"),16,80,32,8)
    if st.button(tr("Run 1-D temperature-field simulation","1B sıcaklık simülasyonunu çalıştır"),type='primary'):
        with st.spinner(tr('Solving the axial finite-volume model…', 'Eksenel sonlu hacim modeli çözülüyor…')):
            try:
                tc=simulate_thermocline(design,material,n_cells=cells)
                st.session_state['tc_result']=tc
                st.session_state['tc_config']=(design,material,cells)
            except (ValueError,RuntimeError) as exc:
                st.error(str(exc))
    if st.session_state.get('tc_config')==(design,material,cells):
        tc=st.session_state['tc_result']
        k1,k2,k3=st.columns(3)
        k1.metric(tr("1-D delivered heat","1B ısı çıkışı"),f"{tc['useful_heat_mwh']:.1f} MWh")
        k2.metric(tr("1-D charge duration","1B şarj süresi"),f"{tc['charge_h']:.1f} h")
        k3.metric(tr("1-D discharge duration","1B deşarj süresi"),f"{tc['discharge_h']:.1f} h")
        st.plotly_chart(thermocline_plot(tc,design),width='stretch',key='chart_1d_profile')
        st.caption(tr('This surrogate uses axial through-bed advection and its boundary power varies with outlet temperature. Comparing its absolute outputs directly with the fixed-power 0-D system requires care.', 'Bu yaklaşık model, dolgu boyunca eksenel taşınım kullanır; sınır gücü çıkış sıcaklığıyla değişir. Mutlak sonuçları sabit güçlü 0B sistemle doğrudan karşılaştırırken bu farkı gözetin.'))
    else:
        st.info(tr('Run the 1-D model to view vertical temperature profiles and source-specific differences.', 'Düşey sıcaklık profillerini ve kaynaklara bağlı farkları görmek için 1B modeli çalıştırın.'))

elif view == '3D Plant Explorer':
    st.subheader(tr("Thermal storage · 3D cutaway", "Isıl depolama · 3B kesit"))
    st.caption(tr("Rotate the model to inspect the layers. Playback follows the calculated 0-D cycle.",
                  "Katmanları incelemek için modeli çevirin. Animasyon hesaplanan 0B çevrimini izler."))
    presentation = st.radio(
        tr("Silo view", "Depo görünümü"), ("exterior", "cutaway"), index=1,
        format_func={"exterior": tr("Exterior", "Dış görünüm"),
                     "cutaway": tr("Cutaway", "Kesit görünümü")}.__getitem__,
        horizontal=True, key="silo_presentation", label_visibility="collapsed")
    if lightweight:
        st.info(tr("3D rendering is disabled in Light mode. Turn it off in the sidebar to explore the silo.",
                   "Hafif modda 3B çizim kapalıdır. Depoyu incelemek için yan menüden Hafif modu kapatın."))
    else:
        st.plotly_chart(plant_3d(result, design, material, cutaway=presentation == "cutaway"),
                        width="stretch", key="chart_3d_silo",
                        config={"displayModeBar": False, "scrollZoom": False,
                                "displaylogo": False})
        st.markdown(
            '<div style="display:flex;justify-content:center;gap:20px;flex-wrap:wrap;'
            'font-size:13px;padding:12px;color:#dce7ef">'
            '<span><span style="color:#b9c7d1">●</span> ' + tr("Steel cladding", "Çelik gövde") + '</span>'
            '<span><span style="color:#e7dfcc">●</span> ' + tr("Insulation", "Yalıtım") + '</span>'
            '<span><span style="color:#d4a65c">●</span> ' + tr("Storage medium", "İç dolgu") + '</span></div>',
            unsafe_allow_html=True)
        st.caption(tr(f"Illustrative color scale: {design.ambient_c:g}–{design.maximum_c:g} °C; use the numerical temperature readout.",
                      f"Temsili renk ölçeği: {design.ambient_c:g}–{design.maximum_c:g} °C; sayısal sıcaklık göstergesini esas alın."))
        st.caption(tr("Thermal colors apply only to the inner storage medium; the metallic shell color is not its surface temperature. Heat is for all modules above Tmin; time spans charge, standby and discharge.",
                      "Sıcaklık renkleri yalnızca iç dolguya aittir; metal kabuğun rengi yüzey sıcaklığı değildir. Isı, tüm modüllerin Tmin üzerindeki enerjisidir; süre şarj, bekleme ve deşarjı kapsar."))
    st.markdown(tr("### Plant geometry", "### Tesis geometrisi"))
    a, b = st.columns(2)
    a.metric(tr("Internal radius", "İç yarıçap"), f"{result['radius_m']:.2f} m")
    b.metric(tr("Module height", "Modül yüksekliği"), f"{result['height_m']:.2f} m")
    c, e = st.columns(2)
    c.metric(tr("Insulation thickness", "Yalıtım kalınlığı"), f"{design.insulation_m:.2f} m")
    e.metric(tr("Outer diameter", "Dış çap"), f"{result['outer_diameter_m']:.2f} m")
    st.caption(tr(f"One representative module shown · {design.modules} identical module(s) in the calculation · {material.name}",
                  f"Bir temsilî modül gösteriliyor · Hesaplamada {design.modules} özdeş modül · {material.name}"))
    st.info(tr("Uniform-temperature 0-D model. Cladding, lid, fasteners and base are schematic; they are not a construction drawing. No radial gradients or measured temperatures are shown. For computed axial profiles, open Visual Story Studio.",
               "Tek ortalama sıcaklıklı 0B model. Gövde, kapak, bağlantılar ve taban şematiktir; imalat çizimi değildir. Radyal gradyan veya ölçülmüş sıcaklık gösterilmez. Hesaplanan eksenel profiller için Görsel Analiz sayfasını açın."))

elif view == 'Materials & Optimization':
    st.markdown(tr('<div class="sect">Material screening and source transparency</div>','<div class="sect">Malzeme karşılaştırması ve kaynaklar</div>'),unsafe_allow_html=True)
    rows=[]
    for m in MATERIALS.values():
        q=(design.volume_m3*m.bulk_density*(m.enthalpy(tmax)-m.enthalpy(tmin))/3.6e9)
        rows.append({'Material':m.name,'Theoretical MWh':q,
                     'Bulk density (kg/m³)':m.bulk_density,'cp at 25°C (J/kg K)':m.cp_25,
                     'Evidence status':m.provenance})
    compare=pd.DataFrame(rows).sort_values('Theoretical MWh',ascending=False)
    c1,c2=st.columns([1.05,1],gap='large')
    with c1:st.plotly_chart(material_comparison(compare),width='stretch',key='chart_materials')
    with c2:st.dataframe(compare,hide_index=True,width='stretch')
    st.warning(tr('All material-specific properties here are legacy or assumed inputs; material screening does not establish material suitability, stability or a safe design temperature.', 'Malzeme özellikleri önceki veya varsayılan girdilerdir. Bu karşılaştırma malzemenin uygunluğunu, kararlılığını veya güvenli tasarım sıcaklığını kanıtlamaz.'))
    st.divider()
    st.markdown(tr('<div class="sect">Maximum usable heat · constrained design screening</div>','<div class="sect">En yüksek kullanılabilir ısı · tasarım taraması</div>'),unsafe_allow_html=True)
    st.caption(tr('Discrete parametric screening, not a globally convergent numerical optimizer. Larger feasible volumes will usually increase capacity; enter a realistic site limit.', 'Ayrık parametrik taramadır; küresel en iyi çözümü garanti etmez. Uygun hacim büyüdükçe kapasite genellikle artar; gerçekçi bir alan sınırı girin.'))
    b1,b2,b3=st.columns(3)
    with b1:mv=st.number_input(tr("Site volume limit · m³","Alan hacmi sınırı · m³"),min_value=100.,max_value=20000.,value=2000.,step=100.)
    with b2:mh=st.number_input(tr("Max module height · m","En fazla modül yüksekliği · m"),min_value=5.,max_value=70.,value=25.,step=1.)
    with b3:md=st.number_input(tr("Max outer diameter · m","En fazla dış çap · m"),min_value=4.,max_value=60.,value=20.,step=1.)
    if st.button(tr("Explore feasible designs","Uygun tasarımları incele"),type='primary'):
        with st.spinner(tr('Checking feasible geometry and heat-delivery results…', 'Uygun geometri ve ısı çıkışı sonuçları hesaplanıyor…')):
            try:
                candidates=screen_designs(design,material,
                    np.linspace(.45*mv,mv,4),[1.8,2.8,3.8],[.25,.5,.85],mh,md)
                st.session_state['candidate_results']=candidates
                st.session_state['candidate_config']=(design,material,mv,mh,md)
            except Exception as exc:
                st.error(tr(f"Screening error: {exc}", f"Tarama hatası: {exc}"))
    if st.session_state.get('candidate_config')==(design,material,mv,mh,md):
        rows=st.session_state['candidate_results']
        if rows:
            df=pd.DataFrame(rows)
            st.success(f'{len(rows)} geometrically feasible candidates. Best of the sampled designs: {rows[0]["usable_mwh"]:.1f} MWh useful heat.')
            st.plotly_chart(optimization_scatter(df),width='stretch',key='chart_screening')
            st.dataframe(df.head(20),hide_index=True,width='stretch')
            st.download_button(tr('↓  Export screening · CSV', '↓ Tarama sonuçlarını indir · CSV'),df.to_csv(index=False),file_name='capacity_screening.csv',mime='text/csv')
        else:st.info(tr('No candidate satisfies the current height/diameter limits.', 'Mevcut yükseklik/çap sınırlarını sağlayan aday bulunamadı.'))


st.info(tr("To reopen your design, use Save active scenario JSON. Numerical results JSON is an output snapshot and cannot be imported into Scenario Manager.",
           "Tasarımınızı yeniden açmak için Aktif senaryoyu kaydet JSON dosyasını kullanın. Sayısal sonuçlar JSON dosyası bir sonuç kaydıdır; Senaryo Yöneticisi’ne yüklenemez."))

payload={'version':APP_VERSION,'design':asdict(design),'material':asdict(material),
         'results':{k:float(v) for k,v in result.items() if isinstance(v,(int,float,np.floating))},
         'status':'numerical-research-preview; not experimentally validated'}
st.download_button(tr('↓ Export numerical results · JSON', '↓ Sayısal sonuçları indir · JSON'),json.dumps(payload,indent=2),
                   file_name='sand_battery_scenario.json',mime='application/json')
st.download_button(
    tr('↓ Save active scenario · JSON (Scenario Manager)', '↓ Aktif senaryoyu kaydet · JSON (Senaryo Yöneticisi)'),
    to_json(current_scenario, {slot: None for slot in SLOTS}),
    file_name="sand_battery_active_scenario.json",
    mime="application/json", key="home_scenario_export",
)
st.download_button(tr('↓ Export engineering summary · Markdown', '↓ Mühendislik özetini indir · Markdown'),scenario_markdown(design,material,result),file_name='sand_battery_engineering_summary.md',mime='text/markdown')
st.markdown('<div class="foot">SAND BATTERY STUDIO · GROUP 8 · EDUCATIONAL NUMERICAL SIMULATION<br>Research and source references are available in the dedicated Research Hub.</div>',unsafe_allow_html=True)

footer()

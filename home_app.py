"""Sand Battery Studio — English-only academic engineering dashboard.

ESE101 Group 8. No AI service calls or heavy ML frameworks.
The demo visualizations do not constitute product certification.
"""
import json
from dataclasses import asdict, replace
import numpy as np
import pandas as pd
import streamlit as st

from engine.materials import MATERIALS, blend
from engine.physics import Design, summarize, simulate_cycle
from engine.solar import csp_thermal_mw, electrical_renewables_mw
from engine.thermocline import simulate_thermocline
from engine.optimization import screen_designs
from visuals import timeline, ledger, plant_3d, material_comparison, thermocline_plot, optimization_scatter
from engine.reporting import scenario_markdown
from project_info import PROJECT, REFERENCES, FIELD_REFERENCES, COURSE_MILESTONES, bibliography_text

st.set_page_config(page_title='Sand Battery Studio | Engineering Workspace',page_icon='🌡️',
                   layout='wide',initial_sidebar_state='expanded')

st.markdown("""
<style>
:root {--copper:#eeb37e;--mint:#58dfc3;--ink:#08111d;--faint:#8ca4b6;}
html,body,[class*='css'] {font-family:'Segoe UI',system-ui,sans-serif}
.stApp {background:radial-gradient(ellipse 900px 450px at 75% -200px,rgba(45,124,145,.14),transparent 80%),#08111d;color:#e7eff5;}
[data-testid='stAppViewContainer'] .main .block-container {padding-top:1.25rem;padding-bottom:4rem;max-width:1480px;}
[data-testid='stSidebar'] {background:#0c1825;border-right:1px solid #213440;}
[data-testid='stSidebar'] div[data-testid='stMarkdownContainer'] p {font-size:.89rem;}
[data-testid='stSidebar'] h3 {font-size:1rem;letter-spacing:.01em;}
section[data-testid='stSidebar'] .block-container {padding-top:1rem;}
[data-testid='stMetric'] {background:linear-gradient(130deg,rgba(30,50,63,.93),rgba(14,30,44,.98));border:1px solid #253b48;border-radius:16px;padding:16px 17px;min-height:113px;transition:transform .2s ease,border-color .2s;}
[data-testid='stMetric']:hover {transform:translateY(-2px);border-color:#ca9a6c;}
[data-testid='stMetricLabel'] p{font-size:.76rem;color:#9bb1c0;letter-spacing:.025em;font-weight:600;}
[data-testid='stMetricValue'] {font-family:'Segoe UI',system-ui,sans-serif;font-size:1.7rem;font-weight:800;color:#f0f7fb;}
div[data-testid='stTabs'] button[role='tab'] {font-size:.89rem;font-weight:700;padding-left:15px;padding-right:15px;color:#93abba;}
div[data-testid='stTabs'] button[aria-selected='true'] {color:#eeb37e;}
div[data-testid='stTabs'] [data-baseweb='tab-highlight'] {background-color:#eeb37e;}
[data-testid='stPlotlyChart'] {border:1px solid #233744;border-radius:17px;background:linear-gradient(145deg,#111e2b,#0b1724);padding:2px 7px;}
div[data-testid='stExpander'] {border:1px solid #273d4a;border-radius:11px;background:rgba(18,32,45,.62)}
[data-testid='stAlert'] {border-radius:10px}
.stButton button[kind='primary'] {background:linear-gradient(105deg,#f2c48e,#df9874);color:#08111d;border:0;font-weight:800;border-radius:10px;}
.stDownloadButton button {border:1px solid #406274;color:#c7e6ed;border-radius:11px;}
.hero {position:relative;overflow:hidden;border:1px solid #304652;border-radius:20px;padding:27px 32px;margin:2px 0 24px;background:linear-gradient(110deg,#132e3b 0%,#10222e 55%,#1d2830 100%);}
.hero:after{content:'';position:absolute;width:420px;height:420px;border-radius:50%;right:-125px;top:-225px;border:55px solid rgba(235,166,105,.10);box-shadow:0 0 110px #4be6c21a;animation:orbit 13s ease-in-out infinite alternate;pointer-events:none;}
@keyframes orbit{to{transform:translate(-42px,55px) rotate(55deg)}}
.eyebrow {font-size:.70rem;letter-spacing:.2em;text-transform:uppercase;color:#72ddcb;font-weight:800;}
.hero h1 {font-family:'Segoe UI',system-ui,sans-serif;font-size:clamp(1.65rem,3.4vw,2.55rem);font-weight:800;margin:.5rem 0;letter-spacing:-.045em;color:#f1f7fc;}
.hero p {color:#a8bfcd;max-width:700px;font-size:.93rem;line-height:1.7;margin:0;}
.pill {display:inline-flex;align-items:center;font-size:.7rem;padding:5px 10px;color:#94f6dd;border:1px solid #387a72;background:#143936;border-radius:20px;margin-left:9px;}
.info-line {border-left:3px solid #eeb37e;background:#12232e;border-radius:0 9px 9px 0;padding:12px 16px;color:#abc1cd;font-size:.86rem;margin:12px 0;}
.sect {font-family:'Segoe UI',system-ui,sans-serif;font-size:1.12rem;font-weight:800;color:#e9f3f8;margin:15px 0 10px;}
.label-block {color:#eeb37e;font-weight:800;font-size:.82rem;text-transform:uppercase;letter-spacing:.09em;}
.small {font-size:.81rem;color:#96abba;line-height:1.65;}
.foot {border-top:1px solid #243947;margin-top:28px;padding-top:16px;color:#8da5b5;font-size:.75rem;line-height:1.8;}
@media(max-width:680px){.hero{padding:19px}.hero:after{display:none}}
</style>
""",unsafe_allow_html=True)

@st.cache_data(max_entries=24,ttl=1800,show_spinner=False)
def _cached_cycle(d,m):
    """Reuse a valid scenario instead of re-solving on every UI rerun."""
    return simulate_cycle(d,m)

with st.sidebar:
    st.markdown('''<div class="eyebrow">ENGINEERING PLATFORM</div>
    <h2 style="font-family:Manrope;margin:5px 0 4px;font-size:1.37rem">◉ Sand Battery Studio</h2>
    <div class="small">ESE101 · GROUP 08 · v2.1 web</div>''',unsafe_allow_html=True)
    st.divider()
    with st.expander('01  STORAGE GEOMETRY',expanded=True):
        vol=st.number_input('Total storage volume · m³',min_value=25.,max_value=20000.,value=1000.,step=25.)
        modules=st.number_input('Identical modules',min_value=1,max_value=20,value=1)
        ratio=st.slider('Height / inner radius',.8,6.,3.,.1)
        insulation=st.slider('Insulation thickness · m',.1,2.,.5,.05)
    with st.expander('02  THERMAL CONDITIONS',expanded=True):
        tmin=st.number_input('Minimum useful temperature · °C',min_value=20.,max_value=250.,value=50.,step=10.)
        tmax=st.number_input('Maximum medium temperature · °C',min_value=180.,max_value=800.,value=550.,step=10.)
        tamb=st.number_input('Ambient temperature · °C',min_value=-30.,max_value=45.,value=15.)
        standby=st.slider('Standby time · days',0.,30.,2.,.5)
        output=st.number_input('Useful heat output · MW',min_value=.1,max_value=40.,value=2.,step=.5)
    with st.expander('03  STORAGE MATERIAL',expanded=True):
        choice=st.selectbox('Storage material',list(MATERIALS))
        material=MATERIALS[choice]
        if st.toggle('Ideal composite blend',value=False):
            other=st.selectbox('Second material',[k for k in MATERIALS if k!=choice])
            pct=st.slider('First material volume fraction · %',0,100,60,5)
            material=blend(material,MATERIALS[other],pct/100,basis='volume')
    with st.expander('04  CHARGING SOURCE',expanded=True):
        method=st.selectbox('Scenario',('Electric heater','CSP — Fresnel / heliostat','PV + wind — average power'))
        eta=.99
        if method=='Electric heater':
            power=st.number_input('Electrical input power · MW',.2,100.,5.,.2)
        elif method.startswith('CSP'):
            area=st.number_input('Collector aperture · m²',100.,150000.,10000.,500.)
            dni=st.slider('Assumed constant DNI · W/m²',100,1400,850,25)
            optical=st.slider('Optical-to-thermal efficiency · %',10,95,70,5)
            power=csp_thermal_mw(area,dni,optical/100)
            eta=1.0
        else:
            pv=st.number_input('PV rated peak · MWp',0.,200.,10.)
            pvcf=st.slider('Assumed average PV capacity factor · %',0,60,20)
            wind=st.number_input('Wind rated power · MW',0.,200.,8.)
            windcf=st.slider('Assumed average wind capacity factor · %',0,75,35)
            power=electrical_renewables_mw(pv,pvcf/100,wind,windcf/100)
        st.caption(f'Modeled source power: {power:.2f} MW')
    st.markdown('<div class="small">No live weather feed. CSP/PV/wind inputs are steady illustrative power scenarios.</div>',unsafe_allow_html=True)

st.markdown('''<div class="info-line"><b>v2.1 Research Laboratory:</b> Additional physics-based studies and numerical experiments are available using the built-in Streamlit page navigation.</div>''',unsafe_allow_html=True)
st.markdown('<div class="small">WEB-FIRST RESEARCH PLATFORM · NO LOCAL INSTALLATION REQUIRED · V2.1</div>',unsafe_allow_html=True)
st.caption("Simulation assumptions and uncertainty are disclosed in the Evidence Library. New calculations are illustrative and not equipment design certifications.")
st.markdown('''<div class="hero"><div class="eyebrow">IZTECH · ESE101 · GROUP 8 <span class="pill">● RESEARCH PLATFORM</span></div>
<h1>Design the next era of thermal storage.</h1>
<p>Explore industrial-scale sand batteries through physics-based simulation, high-temperature materials, thermal dynamics and constraint-driven design screening. Built for clarity, not complexity.</p></div>''',unsafe_allow_html=True)

try:
    design=Design(volume_m3=vol,modules=int(modules),height_over_radius=ratio,insulation_m=insulation,
        source_kind=("solar_thermal" if method.startswith("CSP") else "electricity"),
        minimum_c=tmin,maximum_c=tmax,ambient_c=tamb,hold_days=standby,
        thermal_output_mw=output,charge_mw=power,charge_efficiency=eta)
    result=_cached_cycle(design,material)
except (ValueError,RuntimeError,OverflowError,ZeroDivisionError) as exc:
    st.error(f'This configuration cannot be simulated: {exc}')
    st.info('Adjust temperature limits, available charging power or heat-loss parameters in the sidebar.')
    st.stop()

if tmax>570 and 'silica' in material.name.lower():
    st.warning('Quartz transforms near 573 °C. The illustrative linear specific-heat model does not represent this phase transition. Validate material data before using this temperature regime.')

c1,c2,c3,c4=st.columns(4)
c1.metric('THEORETICAL HEAT CAPACITY',f"{result['capacity_mwh']:,.1f} MWh")
c2.metric('DELIVERED USEFUL HEAT',f"{result['useful_heat_mwh']:,.1f} MWh")
c3.metric('SOURCE → USEFUL HEAT',f"{result['source_to_useful_heat_pct']:.1f}%")
c4.metric('INITIAL THERMAL LOSS',f"{result['initial_loss_kw']:.1f} kW")

overview,thermal,explorer,material_tab,science,team=st.tabs([
    '◈  Overview','⌁  Thermal Dynamics','⬡  3D Plant Explorer','▤  Materials & Optimization','◎  Evidence Library','◇  Project & Team'])
with overview:
    a,b=st.columns([1.45,1],gap='large')
    with a:
        st.markdown('<div class="sect">Operating temperature profile</div>',unsafe_allow_html=True)
        st.plotly_chart(timeline(result),width='stretch',key='chart_overview_timeline')
    with b:
        st.markdown('<div class="sect">Energy distribution</div>',unsafe_allow_html=True)
        flow=ledger(result)
        if flow is not None:
            st.plotly_chart(flow,width='stretch',key='chart_overview_ledger')
        else:
            st.info('Standby cooled below the minimum useful temperature. A nonnegative Sankey cannot represent this reference state; use the ledger below.')
    c1,c2,c3,c4=st.columns(4)
    c1.metric('Charge time',f"{result['charge_hours']:,.1f} h")
    c2.metric('Autonomy at rated output',f"{result['discharge_hours']:,.1f} h")
    c3.metric('Mass of storage medium',f"{result['mass_t']:,.0f} t")
    c4.metric('Energy-balance residual',f"{result['energy_balance_residual_mwh']:.2e} MWh")
    with st.expander('ENERGY ACCOUNTING — see all flows'):
        df=pd.DataFrame([{'Term':'Modeled source energy supplied (MWh)','Energy':result['source_input_mwh']},
            {'Term':'Charging conversion loss (MWh)','Energy':result['heater_loss_mwh']},
            {'Term':'Charge-phase ambient loss (MWh)','Energy':result['charge_loss_mwh']},
            {'Term':'Standby ambient loss (MWh)','Energy':result['standby_loss_mwh']},
            {'Term':'Discharge ambient loss (MWh)','Energy':result['discharge_loss_mwh']},
            {'Term':'Useful thermal delivery (MWh)','Energy':result['useful_heat_mwh']},
            {'Term':'Remaining energy relative to Tmin (MWh)','Energy':result['ending_relative_energy_mwh']}])
        st.dataframe(df,hide_index=True,width='stretch')
    st.markdown('<div class="info-line"><b>Interpretation:</b> Theoretical sensible heat assumes the full selected temperature interval. The useful-heat result additionally includes ambient losses, but assumes a constant-temperature-grade heat consumer down to the set minimum. It is not a measured plant output.</div>',unsafe_allow_html=True)

with thermal:
    st.markdown('<div class="sect">Transient response · 0-D energy balance</div>',unsafe_allow_html=True)
    st.plotly_chart(timeline(result),width='stretch',key='chart_thermal_timeline')
    st.markdown('<div class="sect">1-D thermocline · exploratory comparison</div>',unsafe_allow_html=True)
    st.caption('Finite-volume direct-contact/local-thermal-equilibrium model. This is NOT a validated simulation of Polar Night Energy’s closed-loop air pipes.')
    cells=st.slider('Axial resolution · cells',16,80,32,8)
    if st.button('Run 1-D temperature-field simulation',type='primary'):
        with st.spinner('Solving the axial finite-volume model…'):
            try:
                tc=simulate_thermocline(design,material,n_cells=cells)
                st.session_state['tc_result']=tc
                st.session_state['tc_config']=(design,material,cells)
            except (ValueError,RuntimeError) as exc:
                st.error(str(exc))
    if st.session_state.get('tc_config')==(design,material,cells):
        tc=st.session_state['tc_result']
        k1,k2,k3=st.columns(3)
        k1.metric('1-D delivered heat',f"{tc['useful_heat_mwh']:.1f} MWh")
        k2.metric('1-D charge duration',f"{tc['charge_h']:.1f} h")
        k3.metric('1-D discharge duration',f"{tc['discharge_h']:.1f} h")
        st.plotly_chart(thermocline_plot(tc,design),width='stretch',key='chart_1d_profile')
        st.caption('This surrogate uses axial through-bed advection and its boundary power varies with outlet temperature. Comparing its absolute outputs directly with the fixed-power 0-D system requires care.')
    else:
        st.info('Run the 1-D model to view vertical temperature profiles and source-specific differences.')

with explorer:
    left,right=st.columns([1.3,1],gap='large')
    with left:
        st.markdown('<div class="sect">Animated thermal storage module</div>',unsafe_allow_html=True)
        st.plotly_chart(plant_3d(result,design),width='stretch',key='chart_3d_silo')
    with right:
        st.markdown('<div class="sect">Plant geometry</div>',unsafe_allow_html=True)
        st.metric('Internal silo radius',f"{result['radius_m']:.2f} m")
        st.metric('Module height',f"{result['height_m']:.2f} m")
        st.metric('Outer silo diameter',f"{result['outer_diameter_m']:.2f} m")
        st.metric('Identical modules',str(design.modules))
        st.markdown('<div class="info-line">The 3D animation communicates the <b>average temperature state</b> across operational phases. It is a design visualization, not a CFD simulation, structural model, or a radial thermal measurement.</div>',unsafe_allow_html=True)

with material_tab:
    st.markdown('<div class="sect">Material screening and source transparency</div>',unsafe_allow_html=True)
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
    st.warning('All material-specific properties here are legacy or assumed inputs; material screening does not establish material suitability, stability or a safe design temperature.')
    st.divider()
    st.markdown('<div class="sect">Maximum usable heat · constrained design screening</div>',unsafe_allow_html=True)
    st.caption('Discrete parametric screening, not a globally convergent numerical optimizer. Larger feasible volumes will usually increase capacity; enter a realistic site limit.')
    b1,b2,b3=st.columns(3)
    with b1:mv=st.number_input('Site volume limit · m³',min_value=100.,max_value=20000.,value=2000.,step=100.)
    with b2:mh=st.number_input('Max module height · m',min_value=5.,max_value=70.,value=25.,step=1.)
    with b3:md=st.number_input('Max outer diameter · m',min_value=4.,max_value=60.,value=20.,step=1.)
    if st.button('Explore feasible designs',type='primary'):
        with st.spinner('Checking feasible geometry and heat-delivery results…'):
            try:
                candidates=screen_designs(design,material,
                    np.linspace(.45*mv,mv,4),[1.8,2.8,3.8],[.25,.5,.85],mh,md)
                st.session_state['candidate_results']=candidates
                st.session_state['candidate_config']=(design,material,mv,mh,md)
            except Exception as exc:
                st.error(f'Screening error: {exc}')
    if st.session_state.get('candidate_config')==(design,material,mv,mh,md):
        rows=st.session_state['candidate_results']
        if rows:
            df=pd.DataFrame(rows)
            st.success(f'{len(rows)} geometrically feasible candidates. Best of the sampled designs: {rows[0]["usable_mwh"]:.1f} MWh useful heat.')
            st.plotly_chart(optimization_scatter(df),width='stretch',key='chart_screening')
            st.dataframe(df.head(20),hide_index=True,width='stretch')
            st.download_button('↓  Export screening · CSV',df.to_csv(index=False),file_name='capacity_screening.csv',mime='text/csv')
        else:st.info('No candidate satisfies the current height/diameter limits.')

with science:
    st.markdown('<div class="sect">Mathematical model and reliability boundary</div>',unsafe_allow_html=True)
    st.latex(r'Q_{th} = m\int_{T_{min}}^{T_{max}}c_p(T)\,dT')
    st.latex(r'm c_p(T)\frac{dT}{dt} = P_{charge,th}-P_{delivered,th}-UA(T-T_{ambient})')
    st.markdown('''**0-D:** finite volume, constant average temperature and parametric thermal conductance. 
**1-D:** an illustrative axial LTE finite-volume model, not a detailed commercial pipe exchanger. 
**Material blending:** ideal mass/volume averaging; unverified for composite packing or temperature cycling. 
**Weather:** fixed DNI or averaged PV/wind capacity factors are scenarios; there is no location-aware solar position or hourly meteorology. 
**No claims:** electrical reconversion efficiency, structural stability, laboratory-calibrated thermal conductivity, lifetime or actual CAPEX.''')
    st.markdown('<div class="sect">Verified reference installations</div>',unsafe_allow_html=True)
    st.caption('Manufacturer-stated capacities are context, not calibration data for this solver.')
    rows=[{
        "Installation":site["site"],
        "Year":site["year"],
        "Manufacturer power (MWth)":site["thermal_power_mw"],
        "Operator power (MWth)":site.get("operator_power_mw"),
        "Storage (MWh thermal)":site["thermal_capacity_mwh"],
        "Medium":site["material"],
        "Evidence":site["evidence"],
        "Reference URL":site["url"],
    } for site in FIELD_REFERENCES]
    st.dataframe(pd.DataFrame(rows),hide_index=True,width='stretch')
    st.info('Kankaanpää source discrepancy: Polar Night Energy lists 200 kW / 8 MWh; operator Vatajankoski lists 100 kW / 8 MWh. Different rating definitions may apply; the discrepancy is unresolved. Neither figure calibrates our model.')
    st.markdown('<div class="sect">Evidence Library · APA references</div>',unsafe_allow_html=True)
    st.caption('Primary sources, peer-reviewed work, manufacturer statements and software documentation are categorized separately.')
    for category in dict.fromkeys(r["group"] for r in REFERENCES):
        with st.expander(category,expanded=(category=="Peer-reviewed research")):
            for reference in REFERENCES:
                if reference["group"] != category:
                    continue
                st.markdown(reference["apa"])
                st.caption(f"Evidence type: {reference['type']} · Supports: {reference['claim']}")
                st.link_button('Open original source ↗',reference["url"])
                st.divider()
    st.download_button('↓ Download bibliography · TXT',bibliography_text(),file_name='sand_battery_apa_references.txt',mime='text/plain')
    st.warning('NREL’s >95% five-day heat retention refers to a DIFFERENT particle-TES architecture and a modeled commercial-scale case. It does not validate this simulator. Stored heat and delivered heat are not electrical round-trip efficiency.')

with team:
    st.markdown('<div class="sect">Academic identity & project team</div>',unsafe_allow_html=True)
    st.markdown(f"### {PROJECT['institution']}")
    st.markdown(f"**{PROJECT['department']}**")
    st.markdown(f"**{PROJECT['course']}** · {PROJECT['academic_year']} · **{PROJECT['group']}**")
    st.caption(PROJECT["affiliation_notice"])
    left,right=st.columns(2)
    with left:
        st.markdown('**Lead developer & repository maintainer**')
        st.markdown(f"**{PROJECT['lead_name']}** · [@bysquizy](https://github.com/bysquizy)")
        st.caption('Name shown on the linked GitHub profile; corrections can be requested from the maintainer.')
    with right:
        st.markdown('**Two other Group 8 team members**')
        st.caption('Names are not yet provided, so no student identities are invented.')
    st.markdown('<div class="sect">Course milestones</div>',unsafe_allow_html=True)
    st.dataframe(pd.DataFrame(COURSE_MILESTONES,columns=['Date','Tentative ESE101 milestone']),hide_index=True,width='stretch')
    st.caption('Dates from the uploaded tentative course calendar; Teams updates may supersede them.')
    st.link_button('Open the live web application ↗',PROJECT['public_app'])
    st.markdown('**Project objective:** Analyze sensible-heat storage, losses, thermal delivery and constrained geometrical capacity optimization with transparent input assumptions.')
    st.markdown('**Academic integrity:** The team reports verbal permission for AI-assisted coding. The written course sheet generally limits AI to brainstorming; clarify and disclose the authorized exception before academic submission.')
    st.link_button('Visit the project on GitHub ↗','https://github.com/bysquizy/Sand-Battery-Project')

payload={'version':'2.1-web','design':asdict(design),'material':asdict(material),
         'results':{k:float(v) for k,v in result.items() if isinstance(v,(int,float,np.floating))},
         'status':'numerical-research-preview; not experimentally validated'}
st.download_button('↓  Export current simulation · JSON',json.dumps(payload,indent=2),
                   file_name='sand_battery_scenario.json',mime='application/json')
st.download_button('↓ Export engineering summary · Markdown',scenario_markdown(design,material,result),file_name='sand_battery_engineering_summary.md',mime='text/markdown')
st.markdown('<div class="foot">SAND BATTERY STUDIO v2.1 · IZTECH / DEPARTMENT OF ENERGY SYSTEMS ENGINEERING · ESE101 GROUP 8<br>Maintainer: Yağız Topaç (@bysquizy) · Independent research demonstration · Not experimentally validated or university endorsed.</div>',unsafe_allow_html=True)

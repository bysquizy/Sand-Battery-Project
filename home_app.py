"""Sand Battery Studio — English-only academic engineering dashboard.

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
from project_info import PROJECT
from project_version import APP_VERSION, APP_VERSION_LABEL
from engine.scenarios import PRESETS, SLOTS, to_json
from scenario_state import active, set_active, scenario_banner

st.set_page_config(page_title='Sand Battery Studio | Engineering Workspace',page_icon='🌡️',
                   layout='wide',initial_sidebar_state='expanded')

from ui_theme import inject, hero, footer
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
        "Illustrative presentation scenario",DEMO_PRESETS,key="demo_preset")
    st.caption("Example configurations only — not measured Finnish plants.")
    if st.button("Use selected preset", key="home_apply_preset",
                 use_container_width=True):
        set_active(PRESETS[preset_name])
        st.rerun()
    lightweight = st.toggle(
        "Light mode (skip 3D animation)", value=False, key="low_power_mode",
        help="Useful for mobile or lower-power devices.")
    st.caption("Edit volume, temperatures, modules and charging inputs in "
               "the shared Active Scenario editor above.")

current_scenario = active()
scenario_banner()

hero(
    "GROUP 8 · SAND BATTERY PROJECT",
    "Sand Battery Thermal Storage Simulation",
    "An academic project for modeling sand-based thermal energy storage, "
    "heat losses, charging and discharging, and insulation design.",
)
st.caption(
    "Academic numerical model · Not experimentally validated"
)
st.link_button("GitHub: Project files and research",
               "https://github.com/bysquizy/Sand-Battery-Project")
st.caption("Open Research Hub for source attribution and methods. "
           "Visual Story Studio provides model-driven animations and downloadable reports.")

try:
    design = current_scenario.make_design()
    material = MATERIALS[current_scenario.material_name]
    tmin = current_scenario.minimum_c
    tmax = current_scenario.maximum_c
    result = _cached_cycle(design, material)
except (ValueError, RuntimeError, OverflowError, ZeroDivisionError) as exc:
    st.error(f"This configuration cannot be simulated: {exc}")
    st.info("Adjust the active design, source power or temperature limits "
            "in the shared sidebar editor.")
    st.stop()

if tmax>570 and 'silica' in material.name.lower():
    st.warning('Quartz transforms near 573 °C. The illustrative linear specific-heat model does not represent this phase transition. Validate material data before using this temperature regime.')

c1,c2,c3,c4=st.columns(4)
c1.metric('THEORETICAL HEAT CAPACITY',f"{result['capacity_mwh']:,.1f} MWh")
c2.metric('DELIVERED USEFUL HEAT',f"{result['useful_heat_mwh']:,.1f} MWh")
c3.metric('SOURCE → USEFUL HEAT',f"{result['source_to_useful_heat_pct']:.1f}%")
c4.metric('INITIAL THERMAL LOSS',f"{result['initial_loss_kw']:.1f} kW")

# Render only the selected workspace so costly 3D figures and thermal
# screening calculations are not reconstructed on every widget interaction.
view = st.radio(
    "Engineering workspace",
    ("Overview", "Thermal Dynamics", "3D Plant Explorer", "Materials & Optimization"),
    key="home_workspace", horizontal=True, label_visibility="collapsed",
)
if view == 'Overview':
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
    st.caption('Energy Sankey and time series represent simulated flows. Reported conservation residual checks numerical accounting, not agreement with measured hardware.')
    st.markdown('<div class="info-line"><b>Interpretation:</b> Theoretical sensible heat assumes the full selected temperature interval. The useful-heat result additionally includes ambient losses, but assumes a constant-temperature-grade heat consumer down to the set minimum. It is not a measured plant output.</div>',unsafe_allow_html=True)

elif view == 'Thermal Dynamics':
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

elif view == '3D Plant Explorer':
    left,right=st.columns([1.3,1],gap='large')
    with left:
        st.markdown('<div class="sect">Animated thermal storage module</div>',unsafe_allow_html=True)
        if lightweight:
            st.info("3D animation is paused in Light mode. Disable Light mode to explore the interactive silo.")
        else:
            st.plotly_chart(plant_3d(result,design),width='stretch',key='chart_3d_silo')
    with right:
        st.markdown('<div class="sect">Plant geometry</div>',unsafe_allow_html=True)
        st.metric('Internal silo radius',f"{result['radius_m']:.2f} m")
        st.metric('Module height',f"{result['height_m']:.2f} m")
        st.metric('Outer silo diameter',f"{result['outer_diameter_m']:.2f} m")
        st.metric('Identical modules',str(design.modules))
        st.markdown('<div class="info-line">The 3D animation communicates the <b>average temperature state</b> across operational phases. It is a design visualization, not a CFD simulation, structural model, or a radial thermal measurement.</div>',unsafe_allow_html=True)

elif view == 'Materials & Optimization':
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


payload={'version':APP_VERSION,'design':asdict(design),'material':asdict(material),
         'results':{k:float(v) for k,v in result.items() if isinstance(v,(int,float,np.floating))},
         'status':'numerical-research-preview; not experimentally validated'}
st.download_button('↓ Export numerical results · JSON',json.dumps(payload,indent=2),
                   file_name='sand_battery_scenario.json',mime='application/json')
st.download_button(
    "↓ Save active scenario · JSON (Scenario Manager)",
    to_json(current_scenario, {slot: None for slot in SLOTS}),
    file_name="sand_battery_active_scenario.json",
    mime="application/json", key="home_scenario_export",
)
st.download_button('↓ Export engineering summary · Markdown',scenario_markdown(design,material,result),file_name='sand_battery_engineering_summary.md',mime='text/markdown')
st.markdown('<div class="foot">SAND BATTERY STUDIO · GROUP 8 · EDUCATIONAL NUMERICAL SIMULATION<br>Research and source references are available in the dedicated Research Hub.</div>',unsafe_allow_html=True)

footer()

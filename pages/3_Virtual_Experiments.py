"""Additional numerically reproducible engineering experiments."""
from dataclasses import replace
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from engine.physics import simulate_cycle
from engine.materials import MATERIALS
from engine.research_v2 import LTNE,ltne,ergun
from scenario_state import active, scenario_banner
st.set_page_config(page_title='Virtual Experiments | Sand Battery Studio',page_icon='🧪',layout='wide')
from ui_theme import inject, hero, footer
from localization import tr
inject()
hero(tr("EXPERIMENTS / NUMERICAL TESTBENCH","DENEYLER / SAYISAL TESTLER"), tr("Virtual Experiments","Sanal Deneyler"), tr("Investigate flow resistance, solver grid sensitivity and thermal retention using reproducible virtual studies.","Akış direnci, ağ duyarlılığı ve ısı depolama davranışını sanal deneylerle inceleyin."))
shared = active()
scenario_banner()
st.info('All experiments use theoretical numerical models. Smooth plots and small solver residuals do not prove experimental agreement.')
air,grid,loss=st.tabs(['💨 Ergun & Fan','🧮 Grid Refinement','♨ Insulation vs Standby'])
with air:
    st.subheader('Direct-contact packed-bed pressure-loss experiment')
    a,b,c=st.columns(3)
    with a:
        void=st.slider('Void fraction',.25,.65,.42,.01,key='exp_void')
        particle=st.slider('Particle diameter (mm)',2.,30.,16.,1.,key='exp_particle')/1000
    with b:
        height=st.slider('Bed height (m)',2.,35.,12.,1.,key='exp_height')
        area=st.slider('Bed cross-section (m²)',1.,100.,15.,1.,key='exp_area')
    with c:velocity=st.slider('Superficial velocity (m/s)',.002,.1,.025,.002,key='exp_velocity')
    r=ergun(height,area,void,particle,velocity)
    z1,z2,z3=st.columns(3)
    z1.metric('Pressure loss',f"{r['delta_p_pa']:,.1f} Pa")
    z2.metric('Fan power',f"{r['fan_kw']:.3f} kW")
    z3.metric('Particle Reynolds number',f"{r['particle_re']:.0f}")
    xs=np.linspace(.001,.12,45)
    ys=np.array([ergun(height,area,void,particle,float(v))['delta_p_pa'] for v in xs])
    fig=go.Figure(go.Scatter(x=xs,y=ys,mode='lines',line=dict(color='#ecac75',width=4)))
    fig.update_layout(template='plotly_dark',height=380,xaxis_title='Superficial velocity (m/s)',yaxis_title='Bed pressure loss (Pa)')
    st.plotly_chart(fig,width='stretch',key='exp_ergun_plot')
    st.latex(r'\Delta P/L=150\mu(1-\varepsilon)^2u/(\varepsilon^3d_p^2)+1.75\rho(1-\varepsilon)u^2/(\varepsilon^3d_p)')
    st.warning('Ergun applies to approximately packed particle beds, NOT the embedded closed-loop pipe network of an actual Polar Night Energy plant.')
with grid:
    st.subheader('Spatial resolution and conservation')
    if st.button('Run gas/solid simulations at 8, 16 and 32 cells',type='primary',key='exp_grid_run'):
        with st.spinner('Solving three finite-volume configurations'):
            rows=[]
            d=replace(shared.make_design(),volume_m3=400,charge_mw=3,thermal_output_mw=1)
            for n in [8,16,32]:
                r=ltne(d,MATERIALS[shared.material_name],LTNE(cells=n,hours=2))
                rows.append({'cells':n,'final_avg_solid_c':float(r['solid_c'][-1].mean()),
                             'energy_residual_mwh':r['residual_mwh']})
            st.session_state['v2_grid_results']=rows
            st.session_state["v2_grid_config"] = shared
    if st.session_state.get('v2_grid_config') == shared and 'v2_grid_results' in st.session_state:
        df=pd.DataFrame(st.session_state['v2_grid_results'])
        st.dataframe(df,hide_index=True,width='stretch')
        fig=go.Figure(go.Scatter(x=df.cells,y=df.final_avg_solid_c,mode='lines+markers',line=dict(color='#70e1cd',width=3)))
        fig.update_layout(template='plotly_dark',height=340,xaxis_title='Axial cells',yaxis_title='Mean final solid temperature °C')
        st.plotly_chart(fig,width='stretch',key='exp_grid_fig')
    else:st.caption('Compute results only on demand, avoiding unnecessary cloud CPU usage.')
    st.caption('This study fixes a 400 m³ reference volume while retaining the active material and temperatures. The comparison reveals mesh sensitivity; it is not a formal proof of convergence or validation on measured data.')
with loss:
    st.subheader('Insulation / standby heat sensitivity')
    blankets=[.2,.4,.6,.8,1.]; days=[0,1,2,4,7]
    if st.button('Run 25 thermal simulations',type='primary',key='exp_loss_run'):
        with st.spinner('Comparing insulation and standby constraints'):
            data=[]
            base=shared.make_design()
            for thick in blankets:
                row=[]
                for day in days:
                    out=simulate_cycle(replace(base,insulation_m=thick,hold_days=day),MATERIALS[shared.material_name],max_step_s=3600)
                    row.append(out['useful_heat_mwh'])
                data.append(row)
            st.session_state['v2_loss_results']=data
            st.session_state['v2_loss_config']=shared
    if st.session_state.get('v2_loss_config') == shared and 'v2_loss_results' in st.session_state:
        z=np.asarray(st.session_state['v2_loss_results'])
        fig=go.Figure(go.Heatmap(x=days,y=blankets,z=z,colorscale='Turbo',colorbar=dict(title='MWhth')))
        fig.update_layout(template='plotly_dark',height=430,xaxis_title='Standby duration (days)',yaxis_title='Insulation thickness (m)')
        st.plotly_chart(fig,width='stretch',key='exp_loss_fig')
        st.download_button('Export thermal design matrix (CSV)',pd.DataFrame(z,index=blankets,columns=days).to_csv(),file_name='loss_experiment.csv')
    st.caption('Model includes mean bulk temperature, geometry and UA only; no thermal bridging, exchanger outlet pinch or structural model.')

footer()

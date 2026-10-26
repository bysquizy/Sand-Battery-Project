"""Extended material database and sensitivity explorer (not certified data)."""
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from engine.materials import MATERIALS,blend
from engine.material_scenarios_v2 import SCENARIOS
from engine.research_v2 import exergy_mwh
from engine.input_validation import temperature_sweep
from scenario_state import active, scenario_banner
st.set_page_config(page_title='Material Atlas | Sand Battery Studio',page_icon='🧱',layout='wide')
from ui_theme import inject, hero, footer
from localization import tr
inject()
hero(tr("MATERIALS / EVIDENCE FIRST","MALZEMELER / KAYNAKLAR"), tr("Material Atlas","Malzeme Atlası"), tr("Explore storage media, thermal properties and screening scenarios with clear source and assumption labels.","Depolama malzemelerini, termal özellikleri ve varsayımları karşılaştırın."))
shared = active()
scenario_banner()
st.caption('Local screening overrides below do not modify the shared scenario.')
st.warning("Additional granular media are hypothetical screening inputs. Do not use material curves or maximum temperatures for engineering specification without testing.")
all_materials={**MATERIALS,**SCENARIOS}
a,b,c=st.columns(3)
with a:vol=st.number_input(tr(tr("Packed bulk volume (m³)","Yığın hacmi (m³)"),"Yığın hacmi (m³)"),50.,20000.,float(shared.volume_m3),step=100.,key='atlas_volume')
with b:low=st.number_input(tr(tr("Minimum temperature (°C)","Minimum sıcaklık (°C)"),"Minimum sıcaklık (°C)"),20.,250.,float(shared.minimum_c),step=10.,key='atlas_low')
with c:high=st.number_input(tr(tr("Maximum temperature (°C)","Maksimum sıcaklık (°C)"),"Maksimum sıcaklık (°C)"),250.,850.,float(shared.maximum_c),step=10.,key='atlas_high')
if high <= low:
    st.error('Maximum temperature must be above the minimum temperature.')
    st.stop()
if high >= 570:
    st.warning('Around 573 °C, quartz-rich media have a phase inversion not represented by these linear specific-heat curves. Rankings are not validated above this region.')
rows=[]
for m in all_materials.values():
    heat=m.bulk_density*vol*(m.enthalpy(high)-m.enthalpy(low))/3.6e9
    rows.append({'Medium':m.name,'Thermal capacity MWh':heat,'Exergy upper bound MWh':exergy_mwh(m,vol,low,high,15),
                 'Packed density kg/m3':m.bulk_density,'cp 25°C J/kgK':m.cp_25,'Property status':m.provenance})
df=pd.DataFrame(rows).sort_values('Thermal capacity MWh',ascending=False)
st.caption(f'{len(df)} material scenarios. Capacity ranking is NOT a safety, durability, price or validated performance ranking.')
col1,col2=st.columns([1.1,1])
with col1:
    ranked=df.head(15).sort_values('Thermal capacity MWh')
    fig=go.Figure(go.Bar(
        x=ranked['Thermal capacity MWh'],y=ranked['Medium'],orientation='h',
        marker=dict(color=ranked['Thermal capacity MWh'],colorscale=[[0,'#275369'],[0.5,'#65b9ba'],[1,'#f3b379']],showscale=False),
        hovertemplate='%{y}<br>Stored heat: %{x:.2f} MWhth<extra>Assumed model</extra>'))
    fig.update_layout(template='plotly_dark',height=600,xaxis_title='Sensible heat capacity · MWh(th)',margin=dict(l=5,r=5,t=30,b=45),showlegend=False)
    st.plotly_chart(fig,width='stretch',key='atlas_mwh_fig')
with col2:st.dataframe(df,height=600,hide_index=True,width='stretch')
st.divider()
st.subheader('Explore temperature-dependent specific heat assumptions')
selected=st.multiselect('Compare media',list(all_materials),default=['Silica sand','Crushed basalt'],key='atlas_selected')
temps=np.linspace(25,850,150)
f=go.Figure()
for k in selected[:10]:f.add_trace(go.Scatter(x=temps,y=all_materials[k].cp(temps),name=k,mode='lines'))
f.add_vline(x=573,line_dash='dash',annotation_text='Quartz inversion (~573°C), absent from cp model',line_color='#f1ae66')
f.update_layout(template='plotly_dark',height=420,xaxis_title='Temperature °C',yaxis_title='Assumed cp(T), J/kgK')
st.plotly_chart(f,width='stretch',key='atlas_cp_fig')
st.subheader('Capacity response to maximum temperature')
st.caption('A temperature-sweep of the same illustrative property models; it does not imply safe operation at those temperatures.')
heat_options=st.multiselect('Choose materials for the heatmap',list(all_materials),default=['Silica sand','Crushed basalt','Crushed refractory brick'],max_selections=8,key='atlas_heatmap_mats')
if heat_options:
    # Every heatmap temperature must remain inside the selected range.
    tgrid = temperature_sweep(low, high, n=8)
    z=[[all_materials[label].bulk_density*vol*(all_materials[label].enthalpy(t)-all_materials[label].enthalpy(low))/3.6e9 for t in tgrid] for label in heat_options]
    fg=go.Figure(go.Heatmap(z=z,x=[round(t) for t in tgrid],y=heat_options,colorscale='YlOrRd',colorbar=dict(title='MWhth'),hovertemplate='%{y}<br>Maximum: %{x} °C<br>Storage: %{z:.1f} MWhth<extra>Scenario</extra>'))
    fg.update_layout(template='plotly_dark',height=max(260,64*len(heat_options)+110),xaxis_title='Maximum storage temperature (°C)',margin=dict(l=10,r=10,t=15,b=55))
    st.plotly_chart(fg,width='stretch',key='atlas_capacity_heatmap')
st.divider()
st.subheader('Idealized two-medium mixture')
x,y=st.columns(2)
with x:first=st.selectbox('Medium A',list(all_materials),key='atlas_first')
with y:second=st.selectbox('Medium B',[z for z in all_materials if z!=first],key='atlas_second')
frac=st.slider('Medium A: volume fraction (%)',0,100,50,5,key='atlas_fraction')/100
mix=blend(all_materials[first],all_materials[second],frac)
q=mix.bulk_density*vol*(mix.enthalpy(high)-mix.enthalpy(low))/3.6e9
st.metric('Ideal volume-average composite thermal capacity',f'{q:.1f} MWhth')
st.caption(mix.provenance)
st.info('Unknown packing, thermal expansion, quartz transition, chemical durability and recycled-material environmental safety can invalidate these illustrative comparisons.')
st.markdown('Research basis: [Bošnjaković & Santa (2026)](https://doi.org/10.3390/cleantechnol8050165) and [NREL report 84728](https://www.nrel.gov/docs/fy23osti/84728.pdf). Cite actual tested material sources separately from assumed curves.')

footer()

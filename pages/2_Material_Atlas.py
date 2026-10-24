"""Extended material database and sensitivity explorer (not certified data)."""
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from engine.materials import MATERIALS,blend
from engine.material_scenarios_v2 import SCENARIOS
from engine.research_v2 import exergy_mwh
st.set_page_config(page_title='Material Atlas | Sand Battery Studio',page_icon='🧱',layout='wide')
st.caption('IZTECH / ESE101 GROUP 8 · SAND BATTERY MATERIAL ATLAS')
st.title('Materials, Density & Capacity')
st.warning("Additional granular media are hypothetical screening inputs. Do not use material curves or maximum temperatures for engineering specification without testing.")
all_materials={**MATERIALS,**SCENARIOS}
a,b,c=st.columns(3)
with a:vol=st.number_input('Packed bulk volume (m³)',100.,10000.,1000.,step=100.,key='atlas_volume')
with b:low=st.number_input('Minimum temperature (°C)',20.,250.,60.,step=10.,key='atlas_low')
with c:high=st.number_input('Maximum temperature (°C)',250.,850.,550.,step=10.,key='atlas_high')
rows=[]
for m in all_materials.values():
    heat=m.bulk_density*vol*(m.enthalpy(high)-m.enthalpy(low))/3.6e9
    rows.append({'Medium':m.name,'Thermal capacity MWh':heat,'Exergy upper bound MWh':exergy_mwh(m,vol,low,high,15),
                 'Packed density kg/m3':m.bulk_density,'cp 25°C J/kgK':m.cp_25,'Property status':m.provenance})
df=pd.DataFrame(rows).sort_values('Thermal capacity MWh',ascending=False)
st.caption(f'{len(df)} material scenarios. Capacity ranking is NOT a safety, durability, price or validated performance ranking.')
col1,col2=st.columns([1.1,1])
with col1:
    fig=go.Figure()
    for idx,row in df.head(15).sort_values('Thermal capacity MWh').iterrows():
        fig.add_trace(go.Bar(x=[row['Thermal capacity MWh']],y=[row['Medium']],orientation='h',name=row['Medium'],showlegend=False))
    fig.update_layout(template='plotly_dark',height=600,xaxis_title='Sensible storage MWhth',margin=dict(l=5,r=5,t=30,b=45))
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

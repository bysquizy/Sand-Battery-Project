"""Plotly visuals for the compact sand-battery studio; no external assets."""
import numpy as np
import plotly.graph_objects as go

BG = '#08111d'
PANEL = '#0f1d2a'
MUTED = '#92a8b9'
GRID = '#243746'
COPPER = '#eeb37e'
TEAL = '#58dfc3'
BLUE = '#64a8f6'


def polish(fig, *, height=360, legend=True):
    fig.update_layout(
        template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter, Segoe UI, Arial', color='#dae6ee', size=12),
        margin=dict(l=22, r=22, t=25, b=22), height=height,
        hoverlabel=dict(bgcolor='#182b3b', font_color='#f8fafc'),
        legend=dict(orientation='h',y=-.25,x=0,font=dict(size=11)) if legend else dict(),
        hovermode='x unified',
    )
    fig.update_xaxes(gridcolor=GRID, zeroline=False, linecolor=GRID)
    fig.update_yaxes(gridcolor=GRID, zeroline=False, linecolor=GRID)
    return fig


def timeline(res):
    fig=go.Figure()
    for ts,vals,name,color in [
        (res['charge_trace_h'],res['charge_trace_c'],tr(tr("Charging","Şarj"),"Şarj"),TEAL),
        (res['hold_trace_h'],res['hold_trace_c'],tr(tr("Standby","Bekleme"),"Bekleme"),BLUE),
        (res['discharge_trace_h'],res['discharge_trace_c'],tr(tr("Discharging","Deşarj"),"Deşarj"),COPPER)]:
        fig.add_trace(go.Scatter(x=ts,y=vals,mode='lines',name=name,
                                 line=dict(color=color,width=3),fill='tozeroy',
                                 fillcolor='rgba(100,168,246,.035)'))
    fig.update_layout(xaxis_title=tr(tr("Elapsed time · hours","Geçen süre · saat"),"Geçen süre · saat"), yaxis_title=tr(tr("Mean storage temperature · °C","Ortalama depo sıcaklığı · °C"),"Ortalama depo sıcaklığı · °C"))
    return polish(fig,height=410)


def ledger(res):
    if res['ending_relative_energy_mwh'] < -1e-6: return None
    parts = [
        (tr(tr("Heater loss","Isıtıcı kaybı"),"Isıtıcı kaybı"),res['heater_loss_mwh'],'#8d7891'),
        (tr(tr("Charging loss","Şarj kaybı"),"Şarj kaybı"),res['charge_loss_mwh'],'#a26c6c'),
        (tr(tr("Standby loss","Bekleme kaybı"),"Bekleme kaybı"),res['standby_loss_mwh'],'#4d82ac'),
        (tr(tr("Discharge loss","Deşarj kaybı"),"Deşarj kaybı"),res['discharge_loss_mwh'],'#d18d67'),
        (tr(tr("Useful heat","Kullanılabilir ısı"),"Kullanılabilir ısı"),res['useful_heat_mwh'],TEAL),
        (tr(tr("Remaining heat","Kalan ısı"),"Kalan ısı"),max(0.,res['ending_relative_energy_mwh']),'#d2b65d'),
    ]
    label=[tr(tr("Source input","Kaynak girişi"),"Kaynak girişi")]+[x[0] for x in parts]
    fig=go.Figure(go.Sankey(
        arrangement='fixed', node=dict(pad=18,thickness=16,label=label,
        color=[BLUE]+[x[2] for x in parts],line=dict(color=BG,width=.4)),
        link=dict(source=[0]*len(parts),target=list(range(1,len(parts)+1)),
                  value=[max(0.,v) for _,v,_ in parts],
                  color=['rgba(170,175,190,.23)','rgba(229,128,110,.25)',
                         'rgba(100,168,246,.25)','rgba(238,179,126,.25)',
                         'rgba(88,223,195,.35)','rgba(210,182,93,.23)'])) )
    fig.update_layout(title=dict(text=tr(tr("Energy allocation · MWh","Enerji dağılımı · MWh"),"Enerji dağılımı · MWh"),font=dict(size=13)),
        margin=dict(l=12,r=12,t=55,b=0),paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',font=dict(color='#dce7ef',size=11),height=335)
    return fig


def plant_3d(res,d):
    """Animated illustrative silo colors; uniform cylindrical temperature fields.

    Does not claim measured vertical/radial gradients. 
    """
    r,h=res['radius_m'],res['height_m']
    theta=np.linspace(0,2*np.pi,56)
    z=np.linspace(0,h,24)
    Z,Theta=np.meshgrid(z,theta,indexing='ij')
    X=r*np.cos(Theta);Y=r*np.sin(Theta)
    levels=[d.minimum_c,(d.minimum_c+d.maximum_c)/2,d.maximum_c,
            res['hold_end_c'],max(d.minimum_c,res['hold_end_c']-.2*(d.maximum_c-d.minimum_c))]
    names=[tr(tr("Initial","Başlangıç"),"Başlangıç"),tr(tr("Mid-charge","Şarj ortası"),"Şarj ortası"),tr(tr("Charged","Şarj tamamlandı"),"Şarj tamamlandı"),tr(tr("After standby","Bekleme sonrası"),"Bekleme sonrası"),tr(tr("During discharge","Deşarj sırasında"),"Deşarj sırasında")]
    scale=[[0,'#325e86'],[.35,'#48b7bd'],[.65,'#e4b063'],[1,'#f46b42']]
    def surface(t):
        return go.Surface(x=X,y=Y,z=Z,opacity=.93,showscale=False,
                          surfacecolor=np.full_like(Z,t,dtype=float),
                          colorscale=scale,cmin=d.minimum_c,cmax=d.maximum_c,
                          lighting=dict(ambient=.72,diffuse=.65,specular=.30,roughness=.65),
                          hovertemplate=f'Temperature: {t:.1f} °C<extra></extra>')
    fig=go.Figure(data=[surface(levels[0])],frames=[go.Frame(data=[surface(t)],name=n) for n,t in zip(names,levels)])
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', margin=dict(l=0,r=0,b=0,t=8),height=420,
        font=dict(color='#e1e9f0',size=11),
        scene=dict(bgcolor='rgba(0,0,0,0)',aspectmode='manual',
             aspectratio=dict(x=1,y=1,z=min(2.1,max(.8,h/(2*r)))),
             xaxis=dict(visible=False),yaxis=dict(visible=False),zaxis=dict(visible=False),
             camera=dict(eye=dict(x=1.8,y=1.7,z=1.35))),
        updatemenus=[dict(type='buttons',showactive=False,x=.0,y=.04,
            buttons=[dict(label=tr(tr("▶  Animate","▶  Oynat"),"▶  Oynat"),method='animate',
               args=[None,dict(frame=dict(duration=680,redraw=True),
                                    transition=dict(duration=300),fromcurrent=True)]),
                     dict(label=tr(tr("❚❚  Pause","❚❚  Duraklat"),"❚❚  Duraklat"),method='animate',
               args=[[None],dict(frame=dict(duration=0,redraw=False),mode='immediate')])])],
        sliders=[dict(active=0,y=-.04,len=.9,x=.05,pad=dict(t=5,b=0),
                      steps=[dict(method='animate',label=n,args=[[n],
                           dict(frame=dict(duration=0,redraw=True),mode='immediate')]) for n in names])],
    )
    return fig


def material_comparison(df):
    fig=go.Figure(go.Bar(x=df['Theoretical MWh'],y=df[tr(tr("Material","Malzeme"),"Malzeme")],orientation='h',
               marker=dict(color=[TEAL if i==0 else BLUE for i in range(len(df))],
                           line=dict(width=0)),
               hovertemplate='%{y}: %{x:.2f} MWh<extra></extra>'))
    fig.update_layout(xaxis_title=tr(tr("Theoretical stored heat · MWh","Teorik depolanan ısı · MWh"),"Teorik depolanan ısı · MWh"),yaxis_title='')
    fig.update_yaxes(autorange='reversed',showgrid=False)
    return polish(fig,height=335,legend=False)


def thermocline_plot(tc,design):
    profiles=[('Post charging',tc['charge_profile_c'],TEAL),
              (tr(tr("After standby","Bekleme sonrası"),"Bekleme sonrası"),tc['hold_profile_c'],BLUE),
              ('After discharge',tc['discharge_profile_c'],COPPER)]
    fig=go.Figure()
    for name,values,color in profiles:
        fig.add_trace(go.Scatter(x=values,y=tc['z_m'],mode='lines+markers',
                                 name=name,line=dict(color=color,width=3),marker=dict(size=3)))
    fig.update_layout(xaxis_title=tr(tr("Local temperature · °C","Yerel sıcaklık · °C"),"Yerel sıcaklık · °C"),yaxis_title=tr(tr("Vertical position · m","Dikey konum · m"),"Dikey konum · m"))
    return polish(fig,height=435)


def optimization_scatter(df):
    fig=go.Figure(go.Scatter(x=df['initial_loss_kw'],y=df['usable_mwh'],mode='markers',
         marker=dict(size=14,color=df['volume_m3'],colorscale=[[0,BLUE],[1,COPPER]],
                     showscale=True,colorbar=dict(title='m³'),line=dict(color='#c6e4ec',width=.3)),
         customdata=np.stack([df['volume_m3'],df['insulation_m']],axis=1),
         hovertemplate='Useful heat %{y:.1f} MWh<br>Initial loss %{x:.1f} kW'
                       '<br>Volume %{customdata[0]:.0f} m³<br>Insulation %{customdata[1]:.2f} m<extra></extra>'))
    fig.update_layout(xaxis_title=tr(tr("Initial thermal loss · kW","Başlangıç ısı kaybı · kW"),"Başlangıç ısı kaybı · kW"),yaxis_title=tr(tr("Useful heat · MWh","Kullanılabilir ısı · MWh"),"Kullanılabilir ısı · MWh"))
    return polish(fig,height=350,legend=False)

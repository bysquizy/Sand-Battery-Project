"""Plotly visuals for the compact sand-battery studio; no external assets."""
import numpy as np
import plotly.graph_objects as go
from localization import tr

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
        (res['charge_trace_h'],res['charge_trace_c'],tr("Charging","Şarj"),TEAL),
        (res['hold_trace_h'],res['hold_trace_c'],tr("Standby","Bekleme"),BLUE),
        (res['discharge_trace_h'],res['discharge_trace_c'],tr("Discharging","Deşarj"),COPPER)]:
        fig.add_trace(go.Scatter(x=ts,y=vals,mode='lines',name=name,
                                 line=dict(color=color,width=3),fill='tozeroy',
                                 fillcolor='rgba(100,168,246,.035)'))
    fig.update_layout(xaxis_title=tr("Elapsed time · hours","Geçen süre · saat"), yaxis_title=tr("Mean storage temperature · °C","Ortalama depo sıcaklığı · °C"))
    fig = polish(fig,height=410)
    series = [(res['charge_trace_h'],res['charge_trace_c']),
              (res['hold_trace_h'],res['hold_trace_c']),
              (res['discharge_trace_h'],res['discharge_trace_c'])]
    frames = []
    for step in range(1, 26):
        partial = []
        for xs, ys in series:
            stop = max(2, min(len(xs), int(len(xs)*step/25)))
            partial.append(go.Scatter(x=xs[:stop],y=ys[:stop]))
        frames.append(go.Frame(data=partial,traces=[0,1,2],name=str(step)))
    fig.frames = frames
    fig.update_layout(updatemenus=[dict(type="buttons",direction="left",
        x=1,y=1.13,xanchor="right",yanchor="bottom",showactive=False,
        bgcolor="#1a3947",bordercolor="#426979",font=dict(color="#e8f7f8",size=11),
        buttons=[
            dict(label=tr("▶ Play","▶ Oynat"),method="animate",
                 args=[None,dict(frame=dict(duration=65,redraw=False),
                                 transition=dict(duration=25),mode="immediate")]),
            dict(label=tr("↺ Reset","↺ Sıfırla"),method="animate",
                 args=[[str(25)],dict(frame=dict(duration=0,redraw=False),
                                      transition=dict(duration=0),mode="immediate")])
        ])])
    return fig


def ledger(res):
    if res['ending_relative_energy_mwh'] < -1e-6: return None
    parts = [
        (tr("Heater loss","Isıtıcı kaybı"),res['heater_loss_mwh'],'#8d7891'),
        (tr("Charging loss","Şarj kaybı"),res['charge_loss_mwh'],'#a26c6c'),
        (tr("Standby loss","Bekleme kaybı"),res['standby_loss_mwh'],'#4d82ac'),
        (tr("Discharge loss","Deşarj kaybı"),res['discharge_loss_mwh'],'#d18d67'),
        (tr("Useful heat","Kullanılabilir ısı"),res['useful_heat_mwh'],TEAL),
        (tr("Remaining heat","Kalan ısı"),max(0.,res['ending_relative_energy_mwh']),'#d2b65d'),
    ]
    label=[tr("Source input","Kaynak girişi")]+[x[0] for x in parts]
    fig=go.Figure(go.Sankey(
        arrangement='fixed', node=dict(pad=18,thickness=16,label=label,
        color=[BLUE]+[x[2] for x in parts],line=dict(color=BG,width=.4)),
        link=dict(source=[0]*len(parts),target=list(range(1,len(parts)+1)),
                  value=[max(0.,v) for _,v,_ in parts],
                  color=['rgba(170,175,190,.23)','rgba(229,128,110,.25)',
                         'rgba(100,168,246,.25)','rgba(238,179,126,.25)',
                         'rgba(88,223,195,.35)','rgba(210,182,93,.23)'])) )
    fig.update_layout(title=dict(text=tr("Energy allocation · MWh","Enerji dağılımı · MWh"),font=dict(size=13)),
        margin=dict(l=12,r=12,t=55,b=0),paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',font=dict(color='#dce7ef',size=11),height=335)
    return fig


def plant_3d(res, d, material=None, *, cutaway=True):
    """Layered schematic, using selected samples from the actual 0-D cycle."""
    from silo_visual import layered_silo
    return layered_silo(res, d, material, cutaway=cutaway)



def material_comparison(df):
    fig=go.Figure(go.Bar(x=df['Theoretical MWh'],y=df['Material'],orientation='h',
               marker=dict(color=[TEAL if i==0 else BLUE for i in range(len(df))],
                           line=dict(width=0)),
               hovertemplate='%{y}: %{x:.2f} MWh<extra></extra>'))
    fig.update_layout(xaxis_title=tr("Theoretical stored heat · MWh","Teorik depolanan ısı · MWh"),yaxis_title='')
    fig.update_yaxes(autorange='reversed',showgrid=False)
    return polish(fig,height=335,legend=False)


def thermocline_plot(tc,design):
    profiles=[('Post charging',tc['charge_profile_c'],TEAL),
              (tr("After standby","Bekleme sonrası"),tc['hold_profile_c'],BLUE),
              ('After discharge',tc['discharge_profile_c'],COPPER)]
    fig=go.Figure()
    for name,values,color in profiles:
        fig.add_trace(go.Scatter(x=values,y=tc['z_m'],mode='lines+markers',
                                 name=name,line=dict(color=color,width=3),marker=dict(size=3)))
    fig.update_layout(xaxis_title=tr("Local temperature · °C","Yerel sıcaklık · °C"),yaxis_title=tr("Vertical position · m","Dikey konum · m"))
    return polish(fig,height=435)


def optimization_scatter(df):
    fig=go.Figure(go.Scatter(x=df['initial_loss_kw'],y=df['usable_mwh'],mode='markers',
         marker=dict(size=14,color=df['volume_m3'],colorscale=[[0,BLUE],[1,COPPER]],
                     showscale=True,colorbar=dict(title='m³'),line=dict(color='#c6e4ec',width=.3)),
         customdata=np.stack([df['volume_m3'],df['insulation_m']],axis=1),
         hovertemplate='Useful heat %{y:.1f} MWh<br>Initial loss %{x:.1f} kW'
                       '<br>Volume %{customdata[0]:.0f} m³<br>Insulation %{customdata[1]:.2f} m<extra></extra>'))
    fig.update_layout(xaxis_title=tr("Initial thermal loss · kW","Başlangıç ısı kaybı · kW"),yaxis_title=tr("Useful heat · MWh","Kullanılabilir ısı · MWh"))
    return polish(fig,height=350,legend=False)

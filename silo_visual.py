"""Layered, schematic silo rendering driven by actual 0-D solver snapshots.

Cladding, seams, fasteners and footing are visual context, not a structural
specification. The model has one bulk temperature; no spatial gradient or
outer steel temperature is inferred from the illustrative surface materials.
"""
from __future__ import annotations

import numpy as np
import plotly.graph_objects as go

from localization import tr

STEEL = [[0, '#788796'], [.45, '#c3ccd3'], [1, '#e9eef1']]
INSULATION = [[0, '#c3bda9'], [1, '#e7dfcc']]
SAND = [[0, '#b9b098'], [.30, '#c6b17e'], [.6, '#d4a65c'], [1, '#d68a40']]


def cycle_snapshots(result, design, material=None):
    """Select at most 36 original solver samples, preserving phase endpoints."""
    snapshots = []
    phases = [('charge', tr('Charging', 'Şarj')),
              ('hold', tr('Standby', 'Bekleme')),
              ('discharge', tr('Discharging', 'Deşarj'))]
    for key, phase in phases:
        times = np.asarray(result[f'{key}_trace_h'], dtype=float)
        temperatures = np.asarray(result[f'{key}_trace_c'], dtype=float)
        if (times.ndim != 1 or times.shape != temperatures.shape or not len(times)
                or not np.all(np.isfinite(times))
                or not np.all(np.isfinite(temperatures)) or np.any(np.diff(times) < 0)):
            raise ValueError('Invalid solver time/temperature trace')
        for index in np.unique(np.linspace(0, len(times)-1, min(12, len(times))).astype(int)):
            time, temperature = float(times[index]), float(temperatures[index])
            if snapshots and time < snapshots[-1]['time_h'] - 1e-9:
                raise ValueError('Solver phases must be chronological')
            # Retain phase boundary samples even when timestamps coincide.
            energy = None if material is None else max(0.0, result['mass_t']*1000*
                (material.enthalpy(temperature)-material.enthalpy(design.minimum_c))/3.6e9)
            snapshots.append(dict(time_h=time, temperature_c=temperature,
                                  usable_stored_mwh=energy, phase=phase))
    return snapshots


def _surface(x, y, z, color, name, *, temperature=None, design=None):
    z = np.asarray(z, dtype=float)
    values = np.zeros_like(z) if temperature is None else np.full_like(z, temperature)
    thermal = temperature is not None
    return go.Surface(
        x=x, y=y, z=z, surfacecolor=values, colorscale=SAND if thermal else color,
        cmin=design.ambient_c if thermal else 0,
        cmax=design.maximum_c if thermal else 1,
        showscale=False, showlegend=False, name=name,
        lighting=dict(ambient=.55, diffuse=.82, specular=.3 if thermal else .85,
                      roughness=.95 if thermal else .28, fresnel=.14),
        lightposition=dict(x=120, y=-180, z=250),
        hovertemplate=(name + (f'<br>{temperature:.1f} °C' if thermal else '')
                       + '<extra></extra>'),
    )


def layered_silo(result, design, material=None, *, cutaway=True):
    """Interactive layered cylinder; only the core uses the thermal colorscale."""
    snapshots = cycle_snapshots(result, design, material)
    r, h = float(result['radius_m']), float(result['height_m'])
    insulation = design.insulation_m
    outer = r + insulation
    if not np.all(np.isfinite([r, h, outer])) or min(r, h, insulation) <= 0:
        raise ValueError('Invalid silo dimensions')
    # Missing front-right quarter exposes the core along two radial planes.
    angles = np.linspace(0, 1.5*np.pi if cutaway else 2*np.pi, 65)
    vertical = np.linspace(0, h, 12)
    theta, zz = np.meshgrid(angles, vertical)
    traces = []
    core_indices = []
    bulk_label = tr('Storage medium · uniform model temperature',
                    'İç dolgu · modelin ortalama sıcaklığı')
    if material is not None:
        bulk_label += ' · ' + material.name
    def add(x, y, z, color, name, thermal=False):
        if thermal:
            core_indices.append(len(traces))
        traces.append(_surface(x, y, z, color, name,
                               temperature=snapshots[0]['temperature_c'] if thermal else None,
                               design=design))
    # Opaque cladding stays metallic in every frame. Inner core is revealed only
    # through the cutout, avoiding a misleading transparent glowing steel shell.
    add(outer*np.cos(theta), outer*np.sin(theta), zz, STEEL,
        tr('Steel cladding · schematic', 'Çelik gövde · şematik'))
    if cutaway:
        add(r*np.cos(theta), r*np.sin(theta), zz, SAND, bulk_label, True)
        for angle in [0, 1.5*np.pi]:
            rr, zface = np.meshgrid(np.linspace(0, r, 24), vertical)
            add(rr*np.cos(angle), rr*np.sin(angle), zface, SAND, bulk_label, True)
            rr, zface = np.meshgrid(np.linspace(r, outer, 5), vertical)
            add(rr*np.cos(angle), rr*np.sin(angle), zface, INSULATION,
                tr('Insulation', 'Yalıtım'))
        # Exposed insulation ring at the top and bottom of the cutaway.
        aa, rr = np.meshgrid(angles, np.linspace(r, outer, 5))
        for level in (0, h):
            add(rr*np.cos(aa), rr*np.sin(aa), np.full_like(rr, level),
                INSULATION, tr('Insulation', 'Yalıtım'))
        aa, rr = np.meshgrid(angles, np.linspace(0, r, 16))
        add(rr*np.cos(aa), rr*np.sin(aa), np.full_like(rr, h), SAND, bulk_label, True)
    if cutaway:
        # Fixed light flecks suggest granular material; they encode no thermal
        # measurement and do not introduce a spatial temperature gradient.
        rng = np.random.default_rng(8)
        grain_x, grain_y, grain_z = [], [], []
        for angle in (0, 1.5*np.pi):
            radial = rng.uniform(.015*r, .99*r, 420)
            height = rng.uniform(.005*h, .995*h, 420)
            grain_x.extend(radial*np.cos(angle)+outer*.0008)
            grain_y.extend(radial*np.sin(angle)-outer*.0008)
            grain_z.extend(height)
        traces.append(go.Scatter3d(
            x=grain_x, y=grain_y, z=grain_z, mode='markers',
            marker=dict(size=1, color='#eadbb9', opacity=.25),
            hoverinfo='skip', showlegend=False))
    # A stepped metallic lid and circular footing give the body physical depth.
    # Their small offsets are rendering details, not dimensions used by physics.
    lid_h, base_h = outer*.025, outer*.07
    for radius, bottom, top, name in [
        (outer*1.025, h, h+lid_h, tr('Lid · schematic', 'Kapak · şematik')),
        (outer*1.10, -base_h, 0, tr('Base · schematic', 'Taban · şematik')),
    ]:
        aa, zbody = np.meshgrid(angles if bottom >= h else np.linspace(0, 2*np.pi, 65),
                               [bottom, top])
        add(radius*np.cos(aa), radius*np.sin(aa), zbody, STEEL, name)
        aa, rr = np.meshgrid(angles if bottom >= h else np.linspace(0, 2*np.pi, 65),
                             np.linspace(0, radius, 12))
        add(rr*np.cos(aa), rr*np.sin(aa), np.full_like(rr, top), STEEL, name)
    # Circumferential bands and vertical sheet seams are intentionally neutral.
    line_x, line_y, line_z = [], [], []
    for level in np.linspace(0, h, 5):
        line_x.extend((outer*1.003*np.cos(angles)).tolist()+[None])
        line_y.extend((outer*1.003*np.sin(angles)).tolist()+[None])
        line_z.extend([float(level)]*len(angles)+[None])
    for angle in np.linspace(angles[0], angles[-1], 9):
        line_x.extend([outer*1.004*np.cos(angle)]*2+[None])
        line_y.extend([outer*1.004*np.sin(angle)]*2+[None])
        line_z.extend([0, h, None])
    traces.append(go.Scatter3d(x=line_x, y=line_y, z=line_z, mode='lines',
                               line=dict(color='#596a78', width=2),
                               hoverinfo='skip', showlegend=False))
    bolt_angles = np.linspace(angles[0], angles[-1], 22)
    traces.append(go.Scatter3d(
        x=outer*1.01*np.cos(bolt_angles), y=outer*1.01*np.sin(bolt_angles),
        z=np.full_like(bolt_angles, h+lid_h), mode='markers',
        marker=dict(size=2.5, color='#e8edf0', line=dict(color='#596a78', width=1)),
        hoverinfo='skip', showlegend=False))
    # Ground stays below the footing and cannot be confused with thermal data.
    xx, yy = np.meshgrid(np.linspace(-outer*1.8, outer*1.8, 3),
                         np.linspace(-outer*1.8, outer*1.8, 3))
    add(xx, yy, np.full_like(xx, -base_h*1.03),
        [[0, '#142b38'], [1, '#142b38']], tr('Ground · schematic', 'Zemin · şematik'))

    def readout(sample):
        heat = '—' if sample['usable_stored_mwh'] is None else f"{sample['usable_stored_mwh']:.1f}"
        labels = [(tr('Mean temperature', 'Ortalama sıcaklık'), f"{sample['temperature_c']:.1f} °C"),
                  (tr('Heat above Tmin', 'Tmin üzeri ısı'), f'{heat} MWh'),
                  (tr('Elapsed time', 'Geçen süre'), f"{sample['time_h']:.1f} h")]
        notes = [dict(x=x, y=.13, xref='paper', yref='paper', showarrow=False,
                      text=f'<span style="color:#9eb3bf;font-size:10px">{label}</span><br><b>{value}</b>',
                      xanchor=anchor, font=dict(size=15, color='#edf6f7'))
                 for x, anchor, (label, value) in zip([0, .5, 1], ['left', 'center', 'right'], labels)]
        notes.append(dict(x=.5, y=.22, xref='paper', yref='paper', showarrow=False,
                          text=sample['phase'], font=dict(size=11, color='#68e5cf')))
        return notes
    frames = []
    for index, sample in enumerate(snapshots):
        # Only update thermal colors/hover values; never resend steel geometry.
        updates = [go.Surface(surfacecolor=np.full_like(np.asarray(traces[i].z), sample['temperature_c']),
                              hovertemplate=bulk_label+f"<br>{sample['temperature_c']:.1f} °C<extra></extra>")
                   for i in core_indices]
        frames.append(go.Frame(name=str(index), data=updates, traces=core_indices,
                               layout=dict(annotations=readout(sample))))
    fig = go.Figure(data=traces, frames=frames)
    animation = dict(frame=dict(duration=180, redraw=True), transition=dict(duration=0),
                     mode='immediate', fromcurrent=True)
    jump = dict(frame=dict(duration=0, redraw=True), transition=dict(duration=0), mode='immediate')
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#e1e9f0', size=11),
        margin=dict(l=12, r=12, t=0, b=70), height=650,
        annotations=readout(snapshots[0]), uirevision=f'silo-{r}-{h}-{insulation}-{cutaway}',
        scene=dict(domain=dict(x=[0, 1], y=[.27, 1]), bgcolor='rgba(0,0,0,0)',
                   aspectmode='data',
                   xaxis=dict(visible=False, range=[-outer*1.22, outer*1.22]),
                   yaxis=dict(visible=False, range=[-outer*1.22, outer*1.22]),
                   zaxis=dict(visible=False, range=[-base_h*1.1, h+lid_h*2]),
                   camera=dict(eye=dict(x=1.55, y=-1.9, z=1.25),
                               projection=dict(type='orthographic'))),
        updatemenus=[dict(type='buttons', direction='left', showactive=False,
                         x=0, y=.035, xanchor='left', yanchor='top',
                         bgcolor='#183944', bordercolor='#416774',
                         font=dict(size=11, color='#e7f8f6'),
                         buttons=[dict(label=tr('▶ Play', '▶ Oynat'), method='animate', args=[None, animation]),
                                  dict(label=tr('Ⅱ Pause', 'Ⅱ Duraklat'), method='animate',
                                       args=[[None], dict(frame=dict(duration=0, redraw=False), mode='immediate')]),
                                  dict(label=tr('↺ Reset', '↺ Sıfırla'), method='animate', args=[['0'], jump])])],
        sliders=[dict(x=0, y=-.05, len=1, xanchor='left', pad=dict(t=8, b=0),
                      currentvalue=dict(visible=False), active=0, ticklen=0,
                      steps=[dict(method='animate', label='', args=[[str(index)], jump])
                             for index in range(len(snapshots))])],
        meta=dict(model='0-D uniform bulk temperature', cutaway=cutaway,
                  samples=snapshots, thermal_trace_indices=core_indices,
                  schematic_parts=['cladding', 'lid', 'base', 'seams', 'fasteners']),
    )
    return fig

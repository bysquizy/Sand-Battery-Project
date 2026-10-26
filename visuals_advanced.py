"""Lightweight, data-grounded Plotly engineering visualizations.

Only axial profiles solved by engine.thermocline are mapped around a cylinder.
No interpolated radial gradient, live sensor observations or CFD field exists.
No network, images or extra runtime dependencies.
"""
from __future__ import annotations

import numpy as np
import plotly.graph_objects as go

THERMAL_COLORS = [
    [0.0, "#264d84"], [0.28, "#398bb3"],
    [0.53, "#59cbb5"], [0.74, "#f4bf73"], [1.0, "#e56850"],
]
BG = "rgba(0,0,0,0)"


def _snapshot_array(tc: dict) -> tuple[np.ndarray, np.ndarray, tuple[str, ...]]:
    z = np.asarray(tc["z_m"], dtype=float)
    profiles = np.asarray(tc["animation_profiles_c"], dtype=float)
    times = np.asarray(tc["animation_times_h"], dtype=float)
    phases = tuple(tc["animation_phases"])
    if (profiles.ndim != 2 or z.ndim != 1 or times.ndim != 1
            or profiles.shape[1] != z.size or profiles.shape[0] != times.size
            or len(phases) != times.size or not 2 <= z.size <= 200
            or not 2 <= len(times) <= 120
            or not np.all(np.isfinite(profiles))
            or not np.all(np.isfinite(times))
            or np.any(np.diff(times) < 0)):
        raise ValueError("Finite, ordered computed axial snapshots are required.")
    return profiles, times, phases


def axial_cylinder_animation(tc: dict, radius_m: float,
                             tmin_c: float, tmax_c: float,
                             max_frames: int = 28) -> go.Figure:
    """Animated cylindrical *mapping* of actual 1-D cell temperatures.

    Angular symmetry is an illustration. Simulation resolves z only;
    its radial/surface thermocouple temperatures are NOT calculated.
    """
    profiles, times, phases = _snapshot_array(tc)
    if not np.isfinite(radius_m) or radius_m <= 0 or tmax_c <= tmin_c:
        raise ValueError("Invalid cylinder radius or temperature bounds.")
    indices = np.unique(np.r_[np.linspace(0, len(times)-1,
                                         min(max_frames, len(times)), dtype=int),
                               len(times)-1])
    theta = np.linspace(0, 2*np.pi, 32)
    z = np.asarray(tc["z_m"], dtype=float)
    mesh_z, mesh_a = np.meshgrid(z, theta, indexing="ij")
    xx = radius_m*np.cos(mesh_a)
    yy = radius_m*np.sin(mesh_a)

    def surface(profile):
        return go.Surface(
            x=xx, y=yy, z=mesh_z,
            surfacecolor=np.broadcast_to(profile[:, None], xx.shape),
            cmin=tmin_c, cmax=tmax_c, colorscale=THERMAL_COLORS,
            showscale=True, colorbar=dict(title="°C", len=.70, thickness=12),
            opacity=.96,
            hovertemplate="Axial height %{z:.2f} m<br>Mapped 1-D temperature %{surfacecolor:.1f} °C<extra></extra>",
            lighting=dict(ambient=.74, diffuse=.6, specular=.16),
        )

    names = [f"t{int(i)}" for i in indices]
    fig = go.Figure(data=[surface(profiles[indices[0]])])
    fig.frames = tuple(go.Frame(name=name, data=[surface(profiles[i])],
                                traces=[0]) for name, i in zip(names, indices))
    labels = [f"{phases[i]} · {times[i]:.1f} h" for i in indices]
    fig.update_layout(
        template="plotly_dark", paper_bgcolor=BG, margin=dict(l=0,r=15,b=10,t=38),
        height=495, title=dict(text="Axial thermal front · 1-D mapped onto a silo",
                               font=dict(size=15)),
        scene=dict(bgcolor=BG, aspectmode="manual",
                   aspectratio=dict(x=1,y=1,z=min(2.4,max(.8,
                       float(np.max(z))/max(2*radius_m, .01)))),
                   xaxis=dict(visible=False), yaxis=dict(visible=False),
                   zaxis=dict(visible=False),
                   camera=dict(eye=dict(x=1.8,y=1.65,z=1.3))),
        updatemenus=[dict(type="buttons", direction="left", x=0.01, y=0.02,
                          showactive=False, buttons=[
            dict(label="▶ Play", method="animate",
                 args=[None, dict(frame=dict(duration=230, redraw=True),
                                  transition=dict(duration=0),fromcurrent=True)]),
            dict(label="❚❚ Pause", method="animate",
                 args=[[None], dict(frame=dict(duration=0, redraw=False),
                                    mode="immediate")]),
        ])],
        sliders=[dict(active=0,x=.08,y=-.05,len=.85,
                      currentvalue=dict(prefix="Computed snapshot: ",font=dict(size=12)),
                      steps=[dict(label=labels[j],method="animate",
                                  args=[[name],dict(mode="immediate",
                                      frame=dict(duration=0,redraw=True),
                                      transition=dict(duration=0))])
                             for j,name in enumerate(names)])],
    )
    return fig


def axial_history_heatmap(tc: dict) -> go.Figure:
    """Actual finite-volume samples vs elapsed simulation time (no synthetic frames)."""
    profiles, times, phases = _snapshot_array(tc)
    z = np.asarray(tc["z_m"], dtype=float)
    fig = go.Figure(go.Heatmap(
        x=z, y=times, z=profiles, colorscale=THERMAL_COLORS,
        colorbar=dict(title="°C"), hovertemplate=(
            "Axial position: %{x:.2f} m<br>"
            "Elapsed time: %{y:.2f} h<br>"
            "Modeled temperature: %{z:.1f} °C<extra></extra>"
        ),
    ))
    fig.update_layout(template="plotly_dark",paper_bgcolor=BG,plot_bgcolor=BG,
                      height=380, margin=dict(l=15,r=10,t=18,b=35),
                      xaxis_title="Axial height (m)",
                      yaxis_title="Elapsed model time (h)")
    return fig


def design_frontier_chart(rows: list[dict]) -> go.Figure:
    """Calculated standby-loss / useful-heat tradeoff, no optimized claim."""
    if not rows:
        raise ValueError("At least one computed design is required.")
    fig = go.Figure()
    categories = sorted({r["insulation_m"] for r in rows})
    for thickness in categories:
        sample = [r for r in rows if r["insulation_m"] == thickness]
        fig.add_trace(go.Scatter(
            x=[r["initial_loss_kw"] for r in sample],
            y=[r["useful_heat_mwh"] for r in sample],
            mode="markers",
            name=f"{thickness:g} m insulation",
            marker=dict(size=[max(7,min(22,r["volume_m3"]/110)) for r in sample],
                        opacity=.86),
            customdata=[[r["volume_m3"],r["modules"]] for r in sample],
            hovertemplate=("Initial heat loss: %{x:.1f} kW<br>"
                           "Useful heat: %{y:.1f} MWhth<br>"
                           "Volume: %{customdata[0]:.0f} m³<br>"
                           "Modules: %{customdata[1]:.0f}<extra></extra>"),
        ))
    fig.update_layout(template="plotly_dark",paper_bgcolor=BG,plot_bgcolor=BG,
                      height=390,margin=dict(l=20,r=20,t=20,b=45),
                      xaxis_title="Initial envelope thermal loss (kW)",
                      yaxis_title="Modeled useful heat (MWhth)")
    return fig


def sensitivity_tornado(base_mwh: float, changes: list[dict]) -> go.Figure:
    """Impact of explicit ± perturbations around the same validated design."""
    labels = [v["parameter"] for v in changes]
    lower = [v["low_mwh"]-base_mwh for v in changes]
    upper = [v["high_mwh"]-base_mwh for v in changes]
    fig = go.Figure()
    fig.add_trace(go.Bar(y=labels,x=lower,name="−10% input",orientation="h",
                         marker_color="#5ab8c6"))
    fig.add_trace(go.Bar(y=labels,x=upper,name="+10% input",orientation="h",
                         marker_color="#eeb37e"))
    fig.update_layout(template="plotly_dark",barmode="relative",
                      paper_bgcolor=BG,plot_bgcolor=BG,
                      height=350,margin=dict(l=20,r=20,t=20,b=45),
                      xaxis_title="Change in modeled useful heat from baseline (MWhth)")
    fig.add_vline(x=0,line_color="#b7c6d2",line_width=1)
    return fig

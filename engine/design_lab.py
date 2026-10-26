"""Educational design methods independently reimplemented from first principles.

The uploaded legacy Streamlit ZIP inspired these questions but code is not copied.
These simplified functions are not validated construction design or CFD.
"""
from __future__ import annotations

from dataclasses import replace
import math
import numpy as np
from scipy.integrate import solve_ivp
from .materials import Material
from .physics import Design, J_PER_MWH, geometry, summarize


def volume_for_target_mwh(material: Material, tmin_c: float, tmax_c: float,
                          target_mwh: float) -> float:
    """V = E / [rho * (h(Tmax)-h(Tmin))], theoretical sensible heat only."""
    dh = material.enthalpy(tmax_c) - material.enthalpy(tmin_c)
    if not (math.isfinite(target_mwh) and 0 < target_mwh <= 100000):
        raise ValueError("Target storage energy must be positive and finite.")
    if not (math.isfinite(dh) and dh > 0 and material.bulk_density > 0):
        raise ValueError("Material temperature interval has no physical capacity.")
    return target_mwh * J_PER_MWH / (material.bulk_density * dh)


def insulation_shell_m3(d: Design) -> float:
    """Simple cylindrical jacket INCLUDING top and bottom insulation."""
    d.validate()
    r, h = geometry(d.volume_m3 / d.modules, d.height_over_radius)
    t = d.insulation_m
    return d.modules * math.pi * ((r + t)**2 * (h + 2*t) - r*r*h)


def module_comparison(d: Design, m: Material, counts=(1, 2, 4, 8, 12)):
    """Capacity held constant: module size and heat-leak geometry vary."""
    d.validate()
    rows = []
    for n in counts:
        if not isinstance(n, int) or not 1 <= n <= 50:
            raise ValueError("Module count must be an integer from 1 to 50.")
        candidate = replace(d, modules=n)
        s = summarize(candidate, m)
        rows.append({
            "Modules": n,
            "Individual radius (m)": s["radius_m"],
            "Individual height (m)": s["height_m"],
            "Individual outer diameter (m)": s["outer_diameter_m"],
            "Theoretical energy (MWh)": s["capacity_mwh"],
            "Total UA (W/K)": s["ua_w_k"],
            "Initial heat loss (kW)": s["initial_loss_kw"],
            "Illustrative insulation volume (m³)": insulation_shell_m3(candidate),
        })
    return rows


def cooling_profile(d: Design, m: Material, days: float,
                    samples: int = 81, initial_c: float | None = None):
    """0-D ambient-only cooling, including temperature-dependent cp(T).

    Solves m cp(T) dT/dt = -UA(T-Ta), with no discharge extraction or heating.
    This is a bulk-average numerical trajectory, NOT axial CFD or measured data.
    """
    d.validate()
    if not (math.isfinite(days) and 0 <= days <= 120):
        raise ValueError("Cooling window must be between 0 and 120 days.")
    if not isinstance(samples, int) or not 2 <= samples <= 500:
        raise ValueError("Samples must be between 2 and 500.")
    t0 = d.maximum_c if initial_c is None else float(initial_c)
    if not math.isfinite(t0) or not d.ambient_c <= t0 <= d.maximum_c:
        raise ValueError("Initial temperature must lie between ambient and Tmax.")
    s = summarize(d, m)
    mass = m.bulk_density * d.volume_m3
    total_sec = days*86400.0
    tsec = np.linspace(0., total_sec, samples)
    if days == 0:
        temp = np.full(samples, t0)
    else:
        def rhs(_t, y):
            cp = float(m.cp(y[0]))
            if cp <= 0: raise ValueError("Nonpositive heat capacity.")
            return [-s["ua_w_k"]*(y[0]-d.ambient_c)/(mass*cp)]
        result = solve_ivp(rhs, (0.,total_sec), [t0], t_eval=tsec,
                           rtol=1e-9, atol=1e-9, method="RK45")
        if not result.success or not np.all(np.isfinite(result.y)):
            raise RuntimeError("Cooling integration failed.")
        temp = result.y[0]
    e0 = mass*m.enthalpy(t0)
    remaining = mass*(m.enthalpy(temp)-m.enthalpy(d.ambient_c))/J_PER_MWH
    loss = (e0-mass*m.enthalpy(temp))/J_PER_MWH
    return {"days": tsec/86400.,
            "temperature_c": np.asarray(temp),
            "loss_mwh": np.asarray(loss),
            "remaining_above_ambient_mwh": np.asarray(remaining),
            "heat_loss_kw": s["ua_w_k"]*(np.asarray(temp)-d.ambient_c)/1000.}


def radial_insulation_profile(d: Design, inner_temp_c: float, nodes: int = 51):
    """Steady radial sidewall conduction, neglecting ends and bridges.

    The inside of insulation is fixed at the user-selected mean temperature.
    Side heat flow is determined by series conduction and ambient convection.
    Not a transient radial temperature solution for the storage medium.
    """
    d.validate()
    if not isinstance(nodes,int) or not 10 <= nodes <= 250:
        raise ValueError("Radial grid should contain 10–250 nodes.")
    if not d.ambient_c <= inner_temp_c <= d.maximum_c:
        raise ValueError("Inner temperature outside design bounds.")
    r, h = geometry(d.volume_m3/d.modules, d.height_over_radius)
    outer = r + d.insulation_m
    r_cond = math.log(outer/r)/(2*math.pi*d.conductivity_w_mk*h)
    r_conv = 1/(d.external_convection_w_m2k*2*math.pi*outer*h)
    watts = (inner_temp_c-d.ambient_c)/(r_cond+r_conv)
    positions = np.linspace(r, outer, nodes)
    t = inner_temp_c - watts*np.log(positions/r)/(2*math.pi*d.conductivity_w_mk*h)
    return {"radius_m":positions,"temperature_c":t,
            "surface_c":float(t[-1]),"side_heat_kw_per_module":watts/1000.}


def bounded_geometry_candidates(d: Design, m: Material,
                                max_height_m: float, max_diameter_m: float,
                                thickness_options=(0.25, 0.5, 0.75, 1.0),
                                ratios=(1.5, 2., 3., 4.)):
    """Illustrative geometry screening; does not guarantee structural feasibility."""
    d.validate()
    if not 0 < max_height_m <= 500 or not 0 < max_diameter_m <= 500:
        raise ValueError("Positive facility dimension limits required.")
    data = []
    for ratio in ratios:
        for thick in thickness_options:
            cand = replace(d, height_over_radius=float(ratio), insulation_m=float(thick))
            s = summarize(cand,m)
            if s["height_m"] > max_height_m or s["outer_diameter_m"] > max_diameter_m:
                continue
            data.append({
                "H/R":float(ratio),"Insulation (m)":float(thick),
                "Outer diameter (m)":s["outer_diameter_m"],
                "Module height (m)":s["height_m"],
                "UA (W/K)":s["ua_w_k"],
                "Initial loss (kW)":s["initial_loss_kw"],
                "Insulation volume (m³)":insulation_shell_m3(cand),
                "Stored energy (MWh)":s["capacity_mwh"],
            })
    return sorted(data,key=lambda x:x["Initial loss (kW)"])

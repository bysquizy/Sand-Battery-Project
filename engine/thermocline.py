"""Exploratory 1-D LTE packed-bed surrogate with direct axial advection.

IMPORTANT: Not the closed-loop pipe heat exchanger design used by Polar Night
Energy. The air/solid local equilibrium simplification is unvalidated at scale.
Finite-volume upwind advection, Fourier axial conduction and surface losses.
"""
from dataclasses import replace

import numpy as np

from .materials import Material
from .physics import Design, J_PER_MWH, geometry


def _setup(d: Design, m: Material, n):
    radius, height = geometry(d.volume_m3, d.height_over_radius)
    area = np.pi * radius ** 2
    dz = height / n
    # Calculate side-wall and each end-cap heat transfer conductance separately.
    ro = radius + d.insulation_m
    r_side = np.log(ro / radius) / (2 * np.pi * d.conductivity_w_mk * height)
    r_side += 1 / (d.external_convection_w_m2k * 2 * np.pi * ro * height)
    r_cap = d.insulation_m / (d.conductivity_w_mk * np.pi * radius ** 2)
    r_cap += 1 / (d.external_convection_w_m2k * np.pi * ro ** 2)
    loss_coeff = np.full(n, 1 / r_side / n)
    loss_coeff[0] += 1 / r_cap
    loss_coeff[-1] += 1 / r_cap
    return area, dz, m.bulk_density * area * dz, loss_coeff


def _advance(T, dt, c_flow, T_in, d, m, cell_mass, ua_cells, conductance, k_eff):
    # Flow coordinates: cell 0 is inlet and cell -1 is outlet.
    incoming = np.r_[T_in, T[:-1]]
    adv = c_flow * (incoming - T)
    gradient = np.diff(T) * conductance
    conductive = np.zeros(T.size)
    conductive[:-1] += gradient
    conductive[1:] -= gradient
    losses = ua_cells * (T - d.ambient_c)
    return T + dt * (adv + conductive - losses) / (cell_mass * m.cp(T))


def simulate_thermocline(d: Design, m: Material, n_cells: int = 40,
                          effective_k: float = 0.8, charge_cutoff_pct: float = 10,
                          discharge_cutoff_pct: float = 70):
    d.validate()
    if not 12 <= n_cells <= 200 or not 0 < effective_k <= 10:
        raise ValueError("Invalid discretization or effective conductivity")
    if not 0 < charge_cutoff_pct < 100 or not 0 < discharge_cutoff_pct < 100:
        raise ValueError("Invalid cutoff percentages")
    if d.modules > 1:
        one = replace(d, volume_m3=d.volume_m3/d.modules,
                      charge_mw=d.charge_mw/d.modules,
                      thermal_output_mw=d.thermal_output_mw/d.modules, modules=1)
        result = simulate_thermocline(one, m, n_cells, effective_k, charge_cutoff_pct, discharge_cutoff_pct)
        result["electric_input_mwh"] *= d.modules
        result["charge_loss_mwh"] *= d.modules
        result["standby_loss_mwh"] *= d.modules
        result["discharge_loss_mwh"] *= d.modules
        result["energy_balance_residual_mwh"] *= d.modules
        result["final_relative_energy_mwh"] *= d.modules
        result["useful_heat_mwh"] *= d.modules
        result["nominal_capacity_mwh"] *= d.modules
        return result
    area, dz, cell_mass, ua = _setup(d, m, n_cells)
    axial_k = effective_k * area / dz
    min_t, max_t = d.minimum_c, d.maximum_c
    span = max_t - min_t
    nominal = d.volume_m3 * m.bulk_density * (m.enthalpy(max_t) - m.enthalpy(min_t))
    C_charge = d.charge_mw * 1e6 * d.charge_efficiency / span
    C_discharge = d.thermal_output_mw * 1e6 / span

    def timestep(profile, C):
        capacity = cell_mass * np.min(m.cp(profile))
        return min(900., 0.35 * capacity / (C + 2 * axial_k + np.max(ua)))

    T = np.full(n_cells, min_t)
    # Actual computed finite-volume snapshots for Plotly playback; max ~40
    # small profiles. Never imply a solved radial/3D temperature field.
    snapshots = [T.copy()]
    snapshot_hours = [0.0]
    snapshot_phase = ["Initial"]
    last_capture_s = 0.0

    def capture(profile, elapsed_s, phase, interval_s, force=False):
        nonlocal last_capture_s
        if force or elapsed_s - last_capture_s >= interval_s:
            snapshots.append(profile.copy())
            snapshot_hours.append(elapsed_s / 3600)
            snapshot_phase.append(phase)
            last_capture_s = elapsed_s

    charging_s, input_j = 0., 0.
    charge_loss_j = 0.0
    charge_limit_s = 8 * nominal / (d.charge_mw * 1e6 * d.charge_efficiency) + 86400
    cutoff_charge = min_t + span * charge_cutoff_pct / 100
    for _ in range(100000):
        if T[-1] >= cutoff_charge or charging_s >= charge_limit_s:
            break
        dt = timestep(T, C_charge)
        e_to_bed_w = C_charge * (max_t - T[-1])
        charge_loss_j += float(np.sum(ua * (T - d.ambient_c))) * dt
        T = _advance(T, dt, C_charge, max_t, d, m, cell_mass, ua, axial_k, effective_k)
        input_j += e_to_bed_w * dt / d.charge_efficiency
        charging_s += dt
        capture(T, charging_s, "Charging", charge_limit_s / 16)
    else:
        raise RuntimeError("1-D charge integration step limit exceeded")
    charging_profile = T.copy()
    capture(T, charging_s, "Charged", 0, force=True)
    # Hold phase: explicit conduction/ambient loss with stable steps.
    hold_s = d.hold_days * 86400
    standby_loss_j = 0.0
    if hold_s:
        n_hold = int(np.ceil(hold_s / timestep(T, 0)))
        if n_hold > 100000:
            raise RuntimeError("1-D standby integration step limit exceeded")
        dt = hold_s / n_hold
        for step in range(n_hold):
            standby_loss_j += float(np.sum(ua * (T - d.ambient_c))) * dt
            T = _advance(T, dt, 0, 0, d, m, cell_mass, ua, axial_k, effective_k)
            capture(T, charging_s + (step + 1) * dt, "Standby", hold_s / 6)
    hold_profile = T.copy()
    capture(T, charging_s + hold_s, "After standby", 0, force=True)
    T = T[::-1].copy()
    ua = ua[::-1].copy()
    discharging_s, output_j = 0., 0.
    discharge_loss_j = 0.0
    cutoff_discharge = min_t + span * discharge_cutoff_pct / 100
    discharge_limit_s = 8 * nominal / (d.thermal_output_mw * 1e6) + 86400
    history_h, history_out = [], []
    for _ in range(100000):
        if T[-1] < cutoff_discharge or discharging_s >= discharge_limit_s:
            break
        dt = timestep(T, C_discharge)
        p_useful_w = max(0., C_discharge * (T[-1] - min_t))
        output_j += p_useful_w * dt
        discharge_loss_j += float(np.sum(ua * (T - d.ambient_c))) * dt
        T = _advance(T, dt, C_discharge, min_t, d, m, cell_mass, ua, axial_k, effective_k)
        discharging_s += dt
        # Physical z axis runs bottom-to-top as in charge/hold.
        capture(T[::-1], charging_s + hold_s + discharging_s,
                "Discharging", discharge_limit_s / 16)
        history_h.append(discharging_s / 3600)
        history_out.append(T[-1])
    else:
        raise RuntimeError("1-D discharge integration step limit exceeded")
    capture(T[::-1], charging_s + hold_s + discharging_s,
            "After discharge", 0, force=True)
    final_relative_j = cell_mass * float(np.sum(m.enthalpy(T) - m.enthalpy(min_t)))
    thermal_input_j = input_j * d.charge_efficiency
    residual_j = (thermal_input_j - output_j - charge_loss_j -
                  standby_loss_j - discharge_loss_j - final_relative_j)
    return {
        "charge_cutoff_pct": charge_cutoff_pct,
        "discharge_cutoff_pct": discharge_cutoff_pct,
        "charge_loss_mwh": charge_loss_j / J_PER_MWH,
        "standby_loss_mwh": standby_loss_j / J_PER_MWH,
        "discharge_loss_mwh": discharge_loss_j / J_PER_MWH,
        "final_relative_energy_mwh": final_relative_j / J_PER_MWH,
        "energy_balance_residual_mwh": residual_j / J_PER_MWH,
        "z_m": (np.arange(n_cells) + .5) * dz,
        "animation_profiles_c": np.asarray(snapshots),
        "animation_times_h": np.asarray(snapshot_hours),
        "animation_phases": tuple(snapshot_phase),
        "charge_profile_c": charging_profile,
        "hold_profile_c": hold_profile,
        "discharge_profile_c": T[::-1],
        "charge_h": charging_s/3600, "discharge_h": discharging_s/3600,
        "electric_input_mwh": input_j / J_PER_MWH,
        "useful_heat_mwh": output_j / J_PER_MWH,
        "nominal_capacity_mwh": nominal / J_PER_MWH,
        "outlet_time_h": np.asarray(history_h),
        "outlet_temperature_c": np.asarray(history_out),
        "note": "Exploratory LTE direct-contact packed-bed model; not a validated pipe-in-sand system.",
    }

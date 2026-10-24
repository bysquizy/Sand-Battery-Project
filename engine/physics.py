"""Lumped sensible-heat store with strictly accounted 0-D thermal energy balance.

Important: The model assumes a single average solid temperature, time-independent
ambient/charging powers and constant deliverable output power down to Tmin.
It does *not* resolve a closed-loop heat-exchanger's approach temperature.
"""
from __future__ import annotations
from dataclasses import dataclass
import math
import numpy as np
from scipy.integrate import solve_ivp
from .materials import Material

J_PER_MWH = 3.6e9


@dataclass(frozen=True)
class Design:
    volume_m3: float = 1000.0
    height_over_radius: float = 3.0
    modules: int = 1
    insulation_m: float = 0.5
    conductivity_w_mk: float = 0.06
    external_convection_w_m2k: float = 10.0
    ambient_c: float = 15.0
    minimum_c: float = 50.0
    maximum_c: float = 550.0
    charge_mw: float = 5.0
    charge_efficiency: float = 0.99
    thermal_output_mw: float = 2.0
    hold_days: float = 2.0
    source_kind: str = "electricity"  # electricity or post-optics solar_thermal

    def validate(self) -> None:
        vals = [self.volume_m3, self.height_over_radius, self.insulation_m,
                self.conductivity_w_mk, self.external_convection_w_m2k,
                self.charge_mw, self.thermal_output_mw, self.hold_days,
                self.minimum_c, self.maximum_c, self.ambient_c, self.charge_efficiency]
        if not all(math.isfinite(x) for x in vals):
            raise ValueError("Every design input must be finite")
        if min(self.volume_m3, self.height_over_radius, self.insulation_m,
               self.conductivity_w_mk, self.external_convection_w_m2k,
               self.charge_mw, self.thermal_output_mw) <= 0:
            raise ValueError("Volume, geometry, insulation, conductance and power must be positive")
        if type(self.modules) is not int or not 1 <= self.modules <= 50:
            raise ValueError("Modules must be an integer from 1 to 50")
        if self.hold_days < 0 or self.hold_days > 365:
            raise ValueError("Hold days must be between 0 and 365")
        if not (self.ambient_c <= self.minimum_c < self.maximum_c):
            raise ValueError("Require ambient <= Tmin < Tmax")
        if self.source_kind not in ("electricity", "solar_thermal"):
            raise ValueError("Unsupported source energy kind")
        if not 0 < self.charge_efficiency <= 1:
            raise ValueError("Charging efficiency must be in (0, 1]")


def geometry(volume_m3: float, height_over_radius: float):
    if volume_m3 <= 0 or height_over_radius <= 0:
        raise ValueError("Invalid cylinder parameters")
    radius = (volume_m3 / (math.pi * height_over_radius)) ** (1 / 3)
    return radius, height_over_radius * radius


def thermal_ua(radius, height, thickness, conductivity, convection):
    """Cylindrical wall + simplified plane-cap conduction and surface convection.

    Assumes identical caps and wall insulation, no thermal bridging or contact
    resistances. Does not constitute a full construction heat-loss calculation.
    """
    if min(radius, height, thickness, conductivity, convection) <= 0:
        raise ValueError("Non-positive thermal geometry")
    outer_radius = radius + thickness
    side_r = math.log(outer_radius / radius) / (2 * math.pi * conductivity * height)
    side_r += 1 / (convection * 2 * math.pi * outer_radius * height)
    cap_r = thickness / (conductivity * math.pi * radius**2)
    cap_r += 1 / (convection * math.pi * outer_radius**2)
    return 1 / side_r + 2 / cap_r


def _enthalpy_j(material: Material, mass_kg: float, temperature_c: float) -> float:
    return mass_kg * material.enthalpy(temperature_c)


def summarize(design: Design, material: Material):
    design.validate()
    r, h = geometry(design.volume_m3 / design.modules, design.height_over_radius)
    ua = design.modules * thermal_ua(r, h, design.insulation_m,
                        design.conductivity_w_mk, design.external_convection_w_m2k)
    mass = design.volume_m3 * material.bulk_density
    if min(material.cp(design.minimum_c), material.cp(design.maximum_c)) <= 0:
        raise ValueError("Heat capacity must stay positive over the temperature interval")
    cap = (_enthalpy_j(material, mass, design.maximum_c)
          -_enthalpy_j(material, mass, design.minimum_c)) / J_PER_MWH
    return dict(radius_m=r, height_m=h, outer_diameter_m=2*(r+design.insulation_m),
                mass_t=mass/1000, ua_w_k=ua, capacity_mwh=cap,
                initial_loss_kw=ua*(design.maximum_c-design.ambient_c)/1000,
                ideal_discharge_h=cap/design.thermal_output_mw)


def simulate_cycle(d: Design, m: Material, max_step_s: float=1200):
    """Charge at constant P, hold, then deliver constant heat until Tmin.

    Energy ledger separates heater inefficiency, ambient heat loss and final
    stored-energy state. Energy residual should be close to solver tolerance.
    """
    s = summarize(d, m)
    mass = d.volume_m3 * m.bulk_density
    ua = s['ua_w_k']
    p_charge = d.charge_mw * 1e6 * d.charge_efficiency
    p_out = d.thermal_output_mw * 1e6
    if p_charge <= ua*(d.maximum_c-d.ambient_c):
        raise ValueError("Charge power cannot reach Tmax against heat losses")
    def rhs(power):
        def f(_time, y):
            return [(power-ua*(y[0]-d.ambient_c))/(mass*m.cp(y[0])),
                    ua*(y[0]-d.ambient_c)]
        return f
    def event_at(T_target, direction):
        def event(_time,y): return y[0]-T_target
        event.terminal=True
        event.direction=direction
        return event
    initial_j = _enthalpy_j(m,mass,d.minimum_c)
    target_j = _enthalpy_j(m,mass,d.maximum_c)
    cap_j = target_j-initial_j
    charge = solve_ivp(rhs(p_charge),(0,10*cap_j/p_charge+86400),[d.minimum_c,0.0],
                       events=event_at(d.maximum_c,1),max_step=max_step_s,rtol=1e-9,atol=1e-9)
    if not charge.success or len(charge.t_events[0])==0:
        raise RuntimeError("Charging did not reach setpoint")
    charged_s=float(charge.t[-1])
    hold_s=d.hold_days*86400
    hold=solve_ivp(rhs(0),(0,hold_s),[d.maximum_c,0.0],
                   max_step=max(max_step_s,hold_s/1500) if hold_s else max_step_s,
                   rtol=1e-9,atol=1e-9)
    if not hold.success:
        raise RuntimeError("Standby solver failed")
    after_hold=float(hold.y[0,-1])
    if after_hold <= d.minimum_c:
        discharge_t=np.array([0.]);discharge_T=np.array([after_hold]);tdis=0.;discharge_loss=0.0
    else:
        discharge=solve_ivp(rhs(-p_out),(0,10*cap_j/p_out+86400),[after_hold,0.0],
                            events=event_at(d.minimum_c,-1),max_step=max_step_s,
                            rtol=1e-9,atol=1e-9)
        if not discharge.success or not len(discharge.t_events[0]):
            raise RuntimeError("Discharge event not reached")
        discharge_t=discharge.t;discharge_T=discharge.y[0];tdis=float(discharge.t[-1])
        discharge_loss=float(discharge.y[1,-1])/J_PER_MWH
    e_in=d.charge_mw*1e6*charged_s/J_PER_MWH
    e_del=p_out*tdis/J_PER_MWH
    heater_loss=e_in*(1-d.charge_efficiency)
    e_after_hold=(_enthalpy_j(m,mass,after_hold)-initial_j)/J_PER_MWH
    e_final=(_enthalpy_j(m,mass,float(discharge_T[-1]))-initial_j)/J_PER_MWH
    charge_loss=float(charge.y[1,-1])/J_PER_MWH
    standby_loss=float(hold.y[1,-1])/J_PER_MWH
    residual=e_in-e_del-heater_loss-charge_loss-standby_loss-discharge_loss-e_final
    return dict(**s, charge_hours=charged_s/3600,hold_end_c=after_hold,
        discharge_hours=tdis/3600,electric_input_mwh=(e_in if d.source_kind=="electricity" else None),useful_heat_mwh=e_del,
        source_input_mwh=e_in,source_kind=d.source_kind,
        source_to_useful_heat_pct=100*e_del/e_in,
        electricity_to_useful_heat_pct=(100*e_del/e_in if d.source_kind=="electricity" else None),
        charge_loss_mwh=charge_loss,heater_loss_mwh=heater_loss,
        standby_loss_mwh=standby_loss,discharge_loss_mwh=discharge_loss,
        ending_relative_energy_mwh=e_final,energy_balance_residual_mwh=residual,
        charge_trace_h=charge.t/3600,charge_trace_c=charge.y[0],
        hold_trace_h=charged_s/3600+hold.t/3600,hold_trace_c=hold.y[0],
        discharge_trace_h=(charged_s+hold_s+discharge_t)/3600,
        discharge_trace_c=discharge_T)

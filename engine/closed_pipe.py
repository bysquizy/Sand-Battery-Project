"""Lumped solid / closed-loop pipe thermal-transfer research model.

This is a deliberately simplified *separate* plant topology: no axial pipe
temperature field, CFD, structural rating, measured exchanger geometry or
real-fluid property variation. Fluid-side transfer uses an effectiveness model
for a constant-temperature solid reservoir; a concentric resistance network
approximates solid-side conduction. Its results are NOT Polar Night Energy
equipment performance or a calibrated commercial heat-exchanger prediction.
"""
from __future__ import annotations

from dataclasses import dataclass
import math

from scipy.integrate import solve_ivp

from .materials import Material
from .physics import Design, J_PER_MWH, summarize


@dataclass(frozen=True)
class PipeLoop:
    """Assumed closed-loop geometry and *constant* fluid properties."""
    tubes: int = 40
    length_m: float = 25.0
    inner_diameter_m: float = 0.08
    wall_m: float = 0.006
    pitch_m: float = 0.40
    fluid_h_w_m2k: float = 40.0
    pipe_k_w_mk: float = 18.0
    effective_solid_k_w_mk: float = 1.0
    mass_flow_kg_s: float = 6.0
    fluid_cp_j_kgk: float = 1100.0
    hot_inlet_c: float = 650.0
    return_inlet_c: float = 30.0
    useful_outlet_c: float = 50.0

    def validate(self, design: Design) -> None:
        design.validate()
        if type(self.tubes) is not int or not 1 <= self.tubes <= 2000:
            raise ValueError("Tube count must be an integer between 1 and 2,000.")
        positive = (
            self.length_m, self.inner_diameter_m, self.wall_m, self.pitch_m,
            self.fluid_h_w_m2k, self.pipe_k_w_mk,
            self.effective_solid_k_w_mk, self.mass_flow_kg_s,
            self.fluid_cp_j_kgk,
        )
        if not all(math.isfinite(x) and x > 0 for x in positive):
            raise ValueError("All loop dimensions and transport parameters must be positive finite numbers.")
        if (not all(math.isfinite(x) for x in
                    (self.hot_inlet_c, self.return_inlet_c, self.useful_outlet_c))
            or self.length_m > 150 or self.inner_diameter_m > 0.5
            or self.mass_flow_kg_s > 300 or self.fluid_h_w_m2k > 3000):
            raise ValueError("Loop input exceeds the bounded research-domain limits.")
        outer_radius = self.inner_diameter_m / 2 + self.wall_m
        if self.pitch_m <= 2 * outer_radius:
            raise ValueError("Pipe pitch must exceed the outer tube diameter.")
        if not (self.hot_inlet_c > design.maximum_c
                and self.return_inlet_c < self.useful_outlet_c <= design.maximum_c
                and self.return_inlet_c >= design.ambient_c - 25):
            raise ValueError("Inlet temperatures must supply charge driving force and a valid delivery threshold.")
        # Representative conduction cells are allowed to cover <= bed volume,
        # but are NOT a full thermal coverage or mechanical layout calculation.
        influence_volume = math.pi * (self.pitch_m / 2) ** 2 * self.length_m * self.tubes
        if influence_volume > design.volume_m3:
            raise ValueError("Pipe pitch/length/count imply more representative cell volume than storage volume.")


def pipe_transfer(loop: PipeLoop, design: Design) -> dict[str, float]:
    """Constant-temperature-reservoir effectiveness; resistances in K/W."""
    loop.validate(design)
    ri = loop.inner_diameter_m / 2
    ro = ri + loop.wall_m
    far = loop.pitch_m / 2
    length_total = loop.length_m * loop.tubes
    resistance_fluid = 1 / (loop.fluid_h_w_m2k * 2 * math.pi * ri * length_total)
    resistance_pipe = math.log(ro / ri) / (2 * math.pi * loop.pipe_k_w_mk * length_total)
    resistance_solid = math.log(far / ro) / (
        2 * math.pi * loop.effective_solid_k_w_mk * length_total
    )
    ua = 1 / (resistance_fluid + resistance_pipe + resistance_solid)
    capacity_rate = loop.mass_flow_kg_s * loop.fluid_cp_j_kgk
    ntu = ua / capacity_rate
    effectiveness = -math.expm1(-ntu)
    cutoff_solid = loop.return_inlet_c + (
        loop.useful_outlet_c - loop.return_inlet_c
    ) / effectiveness
    return {
        "ua_w_k": ua,
        "ntu": ntu,
        "effectiveness": effectiveness,
        "fluid_capacity_w_k": capacity_rate,
        "minimum_solid_for_delivery_c": cutoff_solid,
        "representative_volume_fraction": (
            math.pi * far * far * length_total / design.volume_m3
        ),
        "r_fluid_k_w": resistance_fluid,
        "r_wall_k_w": resistance_pipe,
        "r_solid_k_w": resistance_solid,
    }


def simulate_closed_pipe(
    design: Design,
    material: Material,
    loop: PipeLoop | None = None,
    *,
    max_step_s: float = 3600.0,
    maximum_days: float = 180.0,
) -> dict[str, object]:
    """Charge -> standby -> temperature-grade-limited thermal discharge.

    Outlet temperature for a uniform bed: Tout = Ts + (Tin-Ts)*exp(-NTU).
    The ODE integrates source heat into the pipe, ambient loss and useful
    discharge using the *same* enthalpy balance; no electrical conversion,
    fan/pump or heater loss is modeled here. The delivery cap assumes ideal
    modulation/bypass and is not a measured pump-control response.
    """
    if loop is None:
        loop = PipeLoop(
            useful_outlet_c=design.minimum_c,
            return_inlet_c=design.minimum_c - 20,
            hot_inlet_c=design.maximum_c + 100,
        )
    info = pipe_transfer(loop, design)
    if not (math.isfinite(max_step_s) and 60 <= max_step_s <= 86400
            and math.isfinite(maximum_days) and 1 <= maximum_days <= 365):
        raise ValueError("Require positive bounded integration windows.")
    storage = summarize(design, material)
    mass_kg = material.bulk_density * design.volume_m3
    ua_ambient = storage["ua_w_k"]
    c_flow = info["fluid_capacity_w_k"]
    efficacy = info["effectiveness"]
    cutoff = max(design.minimum_c, info["minimum_solid_for_delivery_c"])
    if cutoff >= design.maximum_c:
        raise ValueError("Requested outlet grade cannot be delivered within the storage temperature range.")

    def heat_from_hot(t: float) -> float:
        return max(0.0, c_flow * efficacy * (loop.hot_inlet_c - t))

    def heat_to_cold(t: float) -> float:
        return max(0.0, c_flow * efficacy * (t - loop.return_inlet_c))

    if heat_from_hot(design.maximum_c) <= ua_ambient * (
        design.maximum_c - design.ambient_c
    ):
        raise ValueError("Hot-fluid transfer cannot overcome ambient loss at Tmax.")

    def rhs(mode: str):
        def f(_time, state):
            temp = state[0]
            qhot = heat_from_hot(temp) if mode == "charge" else 0.0
            qout = (min(design.thermal_output_mw * 1e6, heat_to_cold(temp))
                    if mode == "discharge" else 0.0)
            loss = ua_ambient * (temp - design.ambient_c)
            cp = material.cp(temp)
            if cp <= 0:
                raise ValueError("Material cp must remain positive.")
            return [
                (qhot - qout - loss) / (mass_kg * cp),
                qhot, qout, loss,
            ]
        return f

    def threshold(target, direction):
        def event(_time, state):
            return state[0] - target
        event.terminal = True
        event.direction = direction
        return event

    initial = [design.minimum_c, 0.0, 0.0, 0.0]
    tlimit = maximum_days * 86400
    kwargs = dict(max_step=max_step_s, rtol=1e-8, atol=1e-7)
    charge = solve_ivp(
        rhs("charge"), (0, tlimit), initial,
        events=threshold(design.maximum_c, 1), **kwargs,
    )
    if not charge.success or not len(charge.t_events[0]):
        raise RuntimeError("Closed-pipe charging did not reach Tmax within the time limit.")

    after_charge = charge.y[:, -1]
    hold_seconds = design.hold_days * 86400
    if hold_seconds > 0:
        hold = solve_ivp(
            rhs("hold"), (0, hold_seconds), after_charge,
            **kwargs,
        )
        if not hold.success:
            raise RuntimeError("Closed-pipe standby integration failed.")
        state = hold.y[:, -1]
    else:
        state = after_charge

    after_hold_c = float(state[0])
    if after_hold_c <= cutoff:
        ended = state
        discharge_hours = 0.0
        delivery_start_c = after_hold_c
    else:
        discharge = solve_ivp(
            rhs("discharge"), (0, tlimit), state,
            events=threshold(cutoff, -1), **kwargs,
        )
        if not discharge.success or not len(discharge.t_events[0]):
            raise RuntimeError("Closed-pipe discharge failed to reach its outlet-temperature threshold.")
        ended = discharge.y[:, -1]
        discharge_hours = float(discharge.t[-1]) / 3600
        delivery_start_c = loop.return_inlet_c + efficacy * (
            after_hold_c - loop.return_inlet_c
        )

    e_in = float(ended[1]) / J_PER_MWH
    e_del = float(ended[2]) / J_PER_MWH
    e_loss = float(ended[3]) / J_PER_MWH
    e_final = (mass_kg * (material.enthalpy(float(ended[0])) -
               material.enthalpy(design.minimum_c))) / J_PER_MWH
    residual = e_in - e_del - e_loss - e_final
    return {
        **info,
        "charge_hours": float(charge.t[-1]) / 3600,
        "standby_end_c": after_hold_c,
        "discharge_hours": discharge_hours,
        "initial_delivery_outlet_c": delivery_start_c,
        "final_solid_c": float(ended[0]),
        "loop_input_mwhth": e_in,
        "useful_heat_mwhth": e_del,
        "ambient_loss_mwhth": e_loss,
        "final_relative_energy_mwhth": e_final,
        "energy_balance_residual_mwhth": residual,
        "theoretical_capacity_mwhth": storage["capacity_mwh"],
        "thermal_delivery_fraction_pct": (100 * e_del / e_in if e_in else 0),
        "note": "Lumped single-temperature solid and idealized pipe heat transfer; no 2-D field, electrical efficiency, measured fluid properties, structural validation or fan power.",
    }

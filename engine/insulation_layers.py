"""Independent multilayer cylinder insulation study with fixed conductivities.

Assumes conduction through sidewall and two plane caps, and convection from
the outside. Values supplied by users are illustrative assumptions and
temperature-dependent conductivity, pipe penetrations, bridges and ground
contact are not represented.
"""
from __future__ import annotations

from dataclasses import dataclass
import math


@dataclass(frozen=True)
class InsulationLayer:
    thickness_m: float
    conductivity_w_mk: float
    label: str = "Assumed insulation"

    def validate(self):
        if (not math.isfinite(self.thickness_m) or self.thickness_m <= 0
                or not math.isfinite(self.conductivity_w_mk)
                or self.conductivity_w_mk <= 0):
            raise ValueError("Insulation layer thickness and conductivity must be positive and finite.")
        if not self.label.strip():
            raise ValueError("Every insulation layer requires a name.")


def layered_cylinder(
    inner_radius_m: float,
    height_m: float,
    layers: tuple[InsulationLayer, ...],
    outside_h_w_m2k: float,
    inner_c: float,
    ambient_c: float,
) -> dict[str, object]:
    """Compute sidewall and cap UA plus steady side layer interface temperatures."""
    vals = (inner_radius_m, height_m, outside_h_w_m2k, inner_c, ambient_c)
    if not all(math.isfinite(x) for x in vals):
        raise ValueError("Geometry, film coefficient and temperatures must be finite.")
    if min(inner_radius_m, height_m, outside_h_w_m2k) <= 0 or inner_c < ambient_c:
        raise ValueError("Require positive geometry and a hot inner surface.")
    if not 1 <= len(layers) <= 5:
        raise ValueError("Use 1–5 concentric insulation layers.")
    for layer in layers:
        layer.validate()
    radius = inner_radius_m
    r_parts = []
    radii = [radius]
    for layer in layers:
        outer = radius + layer.thickness_m
        r_parts.append(
            math.log(outer / radius) /
            (2 * math.pi * layer.conductivity_w_mk * height_m)
        )
        radius = outer
        radii.append(radius)
    outer_film = 1 / (outside_h_w_m2k * 2 * math.pi * radius * height_m)
    side_r_total = sum(r_parts) + outer_film
    q_side_w = (inner_c - ambient_c) / side_r_total
    interfaces_c = [inner_c]
    for resist in r_parts:
        interfaces_c.append(interfaces_c[-1] - q_side_w * resist)
    cap_area = math.pi * inner_radius_m ** 2
    cap_r = sum(
        layer.thickness_m / (layer.conductivity_w_mk * cap_area)
        for layer in layers
    ) + 1 / (outside_h_w_m2k * math.pi * radius ** 2)
    ua_side = 1 / side_r_total
    ua_two_caps = 2 / cap_r
    return {
        "ua_total_w_k": ua_side + ua_two_caps,
        "ua_side_w_k": ua_side,
        "ua_two_caps_w_k": ua_two_caps,
        "total_loss_w": (ua_side + ua_two_caps) * (inner_c - ambient_c),
        "side_loss_w": q_side_w,
        "outer_radius_m": radius,
        "radial_positions_m": tuple(radii),
        "interface_temperatures_c": tuple(interfaces_c),
        "outer_surface_c": interfaces_c[-1],
        "note": "Illustrative steady layered conduction; not thermal bridging, ground loss or code compliance.",
    }

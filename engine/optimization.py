"""Bounded multi-variable design screening; not a structural or safety certification."""
from dataclasses import replace

from .physics import Design, simulate_cycle
from .materials import Material


def screen_designs(base: Design, material: Material, volumes, ratios, thicknesses,
                   max_height_m: float, max_diameter_m: float):
    """Maximize delivered thermal MWh under explicit geometry constraints.

    Input arrays should remain small for interactive deployments; all candidates
    are evaluated with the same numerical model and operating assumptions.
    """
    records = []
    for volume in volumes:
        for ratio in ratios:
            for insulation in thicknesses:
                cfg = replace(base, volume_m3=float(volume), height_over_radius=float(ratio),
                              insulation_m=float(insulation))
                try:
                    from .physics import geometry
                    r, h = geometry(cfg.volume_m3 / cfg.modules, cfg.height_over_radius)
                    if h > max_height_m or 2 * (r + cfg.insulation_m) > max_diameter_m:
                        continue
                    result = simulate_cycle(cfg, material, max_step_s=3600)
                    records.append({"volume_m3": volume, "height_radius_ratio": ratio,
                                    "insulation_m": insulation, "module_height_m": h,
                                    "module_outer_diameter_m": 2 * (r + insulation),
                                    "stored_mwh": result["capacity_mwh"],
                                    "usable_mwh": result["useful_heat_mwh"],
                                    "initial_loss_kw": result["initial_loss_kw"],
                                    "electric_to_heat_pct": result["electricity_to_useful_heat_pct"]})
                except (ValueError, RuntimeError):
                    continue
    return sorted(records, key=lambda item: item["usable_mwh"], reverse=True)

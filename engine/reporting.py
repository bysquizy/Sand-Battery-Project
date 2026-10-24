"""Deterministic and non-AI scenario summary export."""
from dataclasses import asdict
from .physics import Design
from .materials import Material
from project_info import PROJECT

def scenario_markdown(d: Design, m: Material, output: dict) -> str:
    lines=[
        f"# {PROJECT['product']} — Scenario Summary",
        "", "**Status:** unvalidated research simulation; NOT for construction.",
        f"**Project:** {PROJECT['institution']}, {PROJECT['department']}, ESE101 Group 8.",
        f"**Maintainer:** {PROJECT['lead_github']}", "",
        "## Model boundary",
        "Lumped, time-dependent sensible-heat balance with approximate insulation losses.",
        "Useful heat is computed at fixed draw until Tmin, not measured plant delivery.",
        "", "## Inputs",
        f"- Material: {m.name} ({m.provenance})",
    ]
    for key,value in asdict(d).items():
        lines.append(f"- {key}: {value}")
    lines += ["", "## Model results"]
    for label,key,unit in (
        ("Theoretical thermal capacity","capacity_mwh","MWh"),
        ("Useful heat","useful_heat_mwh","MWh"),
        ("Input source energy","source_input_mwh","MWh"),
        ("Source-to-useful-heat ratio","source_to_useful_heat_pct","%"),
        ("Charge time","charge_hours","h"),
        ("Discharge time","discharge_hours","h"),
        ("Energy-balance residual","energy_balance_residual_mwh","MWh"),
    ):
        lines.append(f"- {label}: {output[key]:.6g} {unit}")
    lines += ["", "## Limitations",
              "Illustrative material data; simplified geometry, heat exchanger and weather assumptions.",
              "No field dataset used for calibration; models cannot certify structural safety.",
              "No electricity-to-electricity round-trip result or CAPEX estimate.",
              "", "## Citations",
              "See the in-app Evidence Library and docs/SOURCE_REGISTER.md."]
    return "\n".join(lines)+"\n"

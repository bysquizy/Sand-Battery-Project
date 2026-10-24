"""Illustrative packed-bed materials; property values are NOT certified measurements.

The original project supplied sand, basalt and crushed firebrick defaults. Values
for other media require laboratory characterization before engineering use.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class Material:
    name: str
    bulk_density: float  # kg/m3, including pores
    cp_25: float  # J/(kg K)
    cp_slope: float  # J/(kg K2) in linear demonstration model
    provenance: str = "Illustrative assumption; verify against material-specific data"

    def cp(self, temp_c):
        return self.cp_25 + self.cp_slope * (temp_c - 25.0)

    def enthalpy(self, temp_c):
        delta = temp_c - 25.0
        return self.cp_25 * delta + 0.5 * self.cp_slope * delta * delta


MATERIALS = {
    "Silica sand": Material("Silica sand", 1600, 740, 0.90, "Legacy v4 example; not a laboratory certificate"),
    "Crushed basalt": Material("Crushed basalt", 1750, 850, 0.42, "Legacy v4 example; not a laboratory certificate"),
    "Crushed refractory brick": Material("Crushed refractory brick", 1900, 840, 0.35, "Legacy v4 example; not a laboratory certificate"),
    "Crushed soapstone (illustrative)": Material("Crushed soapstone (illustrative)", 1850, 850, 0.40),
    "Industrial by-product (illustrative)": Material("Industrial by-product (illustrative)", 1500, 800, 0.45),
}


def blend(first: Material, second: Material, fraction_first: float, basis: str = "volume") -> Material:
    """Ideal mixture: additive volumes and mass-weighted heat capacities."""
    if not 0.0 <= fraction_first <= 1.0:
        raise ValueError("Blend fraction must be between 0 and 1")
    if basis == "volume":
        rho = fraction_first * first.bulk_density + (1 - fraction_first) * second.bulk_density
        w = fraction_first * first.bulk_density / rho
    elif basis == "mass":
        w = fraction_first
        rho = 1.0 / (w / first.bulk_density + (1 - w) / second.bulk_density)
    else:
        raise ValueError("Blend basis must be 'volume' or 'mass'")
    return Material(
        f"{first.name} / {second.name} ideal blend", rho,
        w * first.cp_25 + (1 - w) * second.cp_25,
        w * first.cp_slope + (1 - w) * second.cp_slope,
        "Ideal mixing estimate only; interactions, porosity changes and stability unverified",
    )

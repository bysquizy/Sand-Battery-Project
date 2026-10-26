"""Versioned, bounded, browser-session scenario data for the Sand Battery Studio.

Only human-readable, strictly validated JSON is accepted. There is no pickle,
eval, external database, authentication or server-side persistent user storage.
All models continue to use the existing engine/materials and engine/physics.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, fields
import json
import math

from engine.materials import MATERIALS
from engine.physics import Design
from engine.solar import csp_thermal_mw, electrical_renewables_mw

SCHEMA_VERSION = 1
MAX_IMPORT_BYTES = 40_000
SLOTS = ("A", "B", "C")
SOURCES = ("Electric heater", "CSP thermal", "PV + wind")
MAX_SCENARIO_NAME = 48


@dataclass(frozen=True)
class Scenario:
    name: str = "Industrial thermal store"
    material_name: str = "Silica sand"
    volume_m3: float = 1000.0
    modules: int = 1
    height_over_radius: float = 3.0
    insulation_m: float = 0.5
    minimum_c: float = 50.0
    maximum_c: float = 550.0
    ambient_c: float = 15.0
    hold_days: float = 2.0
    thermal_output_mw: float = 2.0
    source: str = "Electric heater"
    electric_mw: float = 5.0
    csp_aperture_m2: float = 10000.0
    csp_dni_w_m2: float = 850.0
    csp_efficiency: float = 0.70
    pv_mwp: float = 10.0
    pv_capacity_factor: float = 0.20
    wind_mw: float = 8.0
    wind_capacity_factor: float = 0.35

    def validate(self) -> None:
        if not isinstance(self.name, str) or not 1 <= len(self.name.strip()) <= MAX_SCENARIO_NAME:
            raise ValueError("Scenario name must contain 1–48 characters.")
        if self.material_name not in MATERIALS:
            raise ValueError("Select a supported material from the Material Atlas.")
        if self.source not in SOURCES:
            raise ValueError("Unsupported charging-source mode.")
        bounds = {
            "volume_m3": (50, 20000),
            "height_over_radius": (1, 6),
            "insulation_m": (0.1, 1.5),
            "minimum_c": (20, 200),
            "maximum_c": (250, 800),
            "ambient_c": (-25, 45),
            "hold_days": (0, 30),
            "thermal_output_mw": (0.1, 40),
            "electric_mw": (0.2, 100),
            "csp_aperture_m2": (100, 150000),
            "csp_dni_w_m2": (100, 1400),
            "csp_efficiency": (0.1, 0.95),
            "pv_mwp": (0, 200),
            "pv_capacity_factor": (0, 0.6),
            "wind_mw": (0, 200),
            "wind_capacity_factor": (0, 0.75),
        }
        if type(self.modules) is not int or not 1 <= self.modules <= 16:
            raise ValueError("Identical modules must be an integer from 1 to 16.")
        for field, (low, high) in bounds.items():
            value = getattr(self, field)
            if type(value) not in (int, float) or not math.isfinite(value):
                raise ValueError(f"{field} must be a finite number.")
            if not low <= value <= high:
                raise ValueError(f"{field} must be between {low} and {high}.")
        if not self.ambient_c <= self.minimum_c < self.maximum_c:
            raise ValueError("Require ambient temperature <= Tmin < Tmax.")
        power = self.charge_power_mw()
        if not math.isfinite(power) or power <= 0:
            raise ValueError("Charging source must provide positive modeled power.")
        # This also checks the physical constraints of the existing Design.
        self.make_design().validate()

    def charge_power_mw(self) -> float:
        if self.source == "Electric heater":
            return self.electric_mw
        if self.source == "CSP thermal":
            return csp_thermal_mw(
                self.csp_aperture_m2, self.csp_dni_w_m2, self.csp_efficiency
            )
        return electrical_renewables_mw(
            self.pv_mwp, self.pv_capacity_factor,
            self.wind_mw, self.wind_capacity_factor,
        )

    def make_design(self) -> Design:
        return Design(
            volume_m3=self.volume_m3,
            modules=self.modules,
            height_over_radius=self.height_over_radius,
            insulation_m=self.insulation_m,
            minimum_c=self.minimum_c,
            maximum_c=self.maximum_c,
            ambient_c=self.ambient_c,
            hold_days=self.hold_days,
            thermal_output_mw=self.thermal_output_mw,
            charge_mw=self.charge_power_mw(),
            charge_efficiency=1.0 if self.source == "CSP thermal" else 0.99,
            source_kind="solar_thermal" if self.source == "CSP thermal" else "electricity",
        )


PRESETS = {
    "Industrial thermal store": Scenario(),
    "Compact research study": Scenario(
        name="Compact research study", volume_m3=250.0, maximum_c=450.0,
        hold_days=0.5, thermal_output_mw=1.0, electric_mw=2.0,
    ),
    "CSP-assisted thermal storage": Scenario(
        name="CSP-assisted thermal storage", volume_m3=1500.0, modules=2,
        maximum_c=500.0, hold_days=1.5, thermal_output_mw=3.0,
        source="CSP thermal",
    ),
}


def from_mapping(data: object) -> Scenario:
    if not isinstance(data, dict):
        raise ValueError("Scenario entry must be a JSON object.")
    keys = {f.name for f in fields(Scenario)}
    if set(data) != keys:
        raise ValueError("Scenario has unknown or missing field names.")
    if type(data.get("modules")) is not int:
        raise ValueError("Modules must be an integer, not a boolean or decimal.")
    try:
        scenario = Scenario(**data)
        scenario.validate()
    except (TypeError, ValueError, AttributeError) as exc:
        raise ValueError(f"Invalid scenario: {exc}") from exc
    return scenario


def to_json(active: Scenario, saved: dict[str, Scenario | None]) -> str:
    active.validate()
    if set(saved) != set(SLOTS):
        raise ValueError("Expected exactly A, B and C scenario slots.")
    for item in saved.values():
        if item is not None:
            item.validate()
    return json.dumps(
        {"schema_version": SCHEMA_VERSION,
         "active": asdict(active),
         "saved": {k: asdict(saved[k]) if saved[k] else None for k in SLOTS}},
        ensure_ascii=False, indent=2, allow_nan=False,
    )


def _no_duplicate_keys(pairs: list[tuple[str, object]]) -> dict[str, object]:
    """Reject ambiguous JSON objects instead of silently keeping last fields."""
    data: dict[str, object] = {}
    for key, value in pairs:
        if key in data:
            raise ValueError(f"Duplicate JSON field: {key}")
        data[key] = value
    return data


def from_json(blob: bytes) -> tuple[Scenario, dict[str, Scenario | None]]:
    if not isinstance(blob, bytes) or not 0 < len(blob) <= MAX_IMPORT_BYTES:
        raise ValueError("Scenario JSON must be nonempty and no larger than 40 kB.")
    try:
        data = json.loads(blob.decode("utf-8-sig"),
                          object_pairs_hook=_no_duplicate_keys,
                          parse_constant=lambda x: (_ for _ in ()).throw(
                              ValueError(f"Non-finite JSON constant: {x}")))
    except (UnicodeError, json.JSONDecodeError, ValueError) as exc:
        raise ValueError("Invalid UTF-8 scenario JSON.") from exc
    if not isinstance(data, dict) or set(data) != {"schema_version", "active", "saved"}:
        raise ValueError("Scenario bundle has missing or unexpected fields.")
    if type(data["schema_version"]) is not int or data["schema_version"] != SCHEMA_VERSION:
        raise ValueError("Unsupported scenario schema version.")
    saved = data["saved"]
    if not isinstance(saved, dict) or set(saved) != set(SLOTS):
        raise ValueError("JSON must contain scenario slots A, B and C.")
    return (
        from_mapping(data["active"]),
        {slot: from_mapping(saved[slot]) if saved[slot] is not None else None
         for slot in SLOTS},
    )

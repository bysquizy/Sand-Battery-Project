"""Measured-or-user-supplied tabulated heat capacity interface.

Piecewise-linear cp(T) yields an exactly integrated, continuous sensible-heat
enthalpy within the supplied interval; it does NOT invent quartz transition
latent heat or extrapolate outside the data range. Data origin must be declared.
"""
from __future__ import annotations
from dataclasses import dataclass
import math

import numpy as np


@dataclass(frozen=True)
class TabulatedMaterial:
    name: str
    bulk_density: float
    temperatures_c: tuple[float, ...]
    cp_j_kgk: tuple[float, ...]
    provenance: str

    def __post_init__(self):
        if not self.name.strip() or not self.provenance.strip():
            raise ValueError("A material name and provenance label are required.")
        if not math.isfinite(self.bulk_density) or self.bulk_density <= 0:
            raise ValueError("Bulk density must be positive and finite.")
        if len(self.temperatures_c) != len(self.cp_j_kgk) or not 2 <= len(self.temperatures_c) <= 500:
            raise ValueError("Provide 2–500 ordered cp(T) measurements.")
        temp = np.asarray(self.temperatures_c, dtype=float)
        cp = np.asarray(self.cp_j_kgk, dtype=float)
        if (not np.all(np.isfinite(temp)) or not np.all(np.isfinite(cp))
                or np.any(np.diff(temp) <= 0) or np.any(cp <= 0)):
            raise ValueError("Temperatures must rise strictly; cp(T) must be finite and positive.")

    def _range_check(self, temp_c):
        ts = np.asarray(temp_c, dtype=float)
        if not np.all(np.isfinite(ts)) or np.any(ts < self.temperatures_c[0]) or np.any(ts > self.temperatures_c[-1]):
            raise ValueError("cp(T) cannot be evaluated outside the supplied measured/assumed range.")
        return ts

    def cp(self, temp_c):
        x = self._range_check(temp_c)
        y = np.interp(x, self.temperatures_c, self.cp_j_kgk)
        return float(y) if x.ndim == 0 else y

    def enthalpy(self, temp_c):
        """J/kg above first tabulated temperature, exactly integrated in segments."""
        x = self._range_check(temp_c)
        t = np.asarray(self.temperatures_c, dtype=float)
        c = np.asarray(self.cp_j_kgk, dtype=float)
        partial = (c[:-1] + c[1:]) * np.diff(t) / 2
        offsets = np.r_[0., np.cumsum(partial)]
        index = np.clip(np.searchsorted(t, x, side="right") - 1, 0, len(t) - 2)
        dx = x - t[index]
        slope = (c[index + 1] - c[index]) / (t[index + 1] - t[index])
        enthalpy = offsets[index] + c[index] * dx + slope * dx * dx / 2
        return float(enthalpy) if x.ndim == 0 else enthalpy

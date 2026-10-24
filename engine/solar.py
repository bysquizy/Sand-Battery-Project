"""Source-power models; constant irradiance is scenario input, not a weather forecast."""


def csp_thermal_mw(aperture_m2: float, dni_w_m2: float, optical_thermal_efficiency: float) -> float:
    if aperture_m2 < 0 or not 0 <= dni_w_m2 <= 1500 or not 0 <= optical_thermal_efficiency <= 1:
        raise ValueError("Invalid CSP source inputs")
    return aperture_m2 * dni_w_m2 * optical_thermal_efficiency / 1e6


def electrical_renewables_mw(pv_capacity_mwp: float, pv_capacity_factor: float,
                             wind_capacity_mw: float, wind_capacity_factor: float) -> float:
    """Scenario-average available electricity, not simultaneous rated production."""
    if min(pv_capacity_mwp, wind_capacity_mw) < 0 or not all(
        0 <= x <= 1 for x in (pv_capacity_factor, wind_capacity_factor)
    ):
        raise ValueError("Invalid renewable source inputs")
    return pv_capacity_mwp * pv_capacity_factor + wind_capacity_mw * wind_capacity_factor

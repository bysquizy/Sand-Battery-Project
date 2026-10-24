"""Thermal design laboratory: independent analytical and numerical verification."""
from dataclasses import replace
import math
import numpy as np
import pytest
from engine.materials import MATERIALS, Material
from engine.physics import Design, summarize
from engine.design_lab import (
    cooling_profile, volume_for_target_mwh, module_comparison,
    radial_insulation_profile, insulation_shell_m3, bounded_geometry_candidates,
)

M = MATERIALS["Silica sand"]
D = Design(volume_m3=800.,modules=2,insulation_m=.5)


def test_reverse_capacity_sizing_returns_exact_target():
    target = 200.
    volume = volume_for_target_mwh(M, 50., 550., target)
    check = summarize(replace(D,volume_m3=volume),M)
    assert check["capacity_mwh"] == pytest.approx(target,rel=1e-11)


def test_reverse_capacity_rejects_bad_input():
    with pytest.raises(ValueError):
        volume_for_target_mwh(M, 550, 50, 200.)
    with pytest.raises(ValueError):
        volume_for_target_mwh(M, 50, 550, -1.)


def test_cooling_zero_days_is_identity():
    r = cooling_profile(D, M, 0)
    assert np.allclose(r["temperature_c"], D.maximum_c)
    assert np.allclose(r["loss_mwh"],0)


def test_cooling_monotonic_and_energy_ledger():
    r = cooling_profile(D, M, 10.,121)
    assert np.all(np.diff(r["temperature_c"])<=1e-9)
    assert np.all(np.diff(r["loss_mwh"])>=-1e-8)
    mass = D.volume_m3*M.bulk_density
    lost_enthalpy = mass*(M.enthalpy(D.maximum_c)-M.enthalpy(r["temperature_c"][-1]))/3.6e9
    assert r["loss_mwh"][-1] == pytest.approx(lost_enthalpy,rel=1e-10)


def test_constant_cp_reduces_to_newton_cooling():
    m = Material("constant cp test",1600.,900.,0., "synthetic")
    d = replace(D, volume_m3=300., modules=1)
    r = cooling_profile(d,m,3.,81)
    s = summarize(d,m)
    tau = m.bulk_density*d.volume_m3*m.cp(25.)/s["ua_w_k"]
    expected = d.ambient_c+(d.maximum_c-d.ambient_c)*math.exp(-3*86400/tau)
    assert r["temperature_c"][-1] == pytest.approx(expected,rel=1e-7)


def test_module_tradeoff_preserves_total_storage_and_increases_shell_volume():
    rows = module_comparison(D,M,(1,2,4,8))
    assert len(rows)==4
    for r in rows:
        assert r["Theoretical energy (MWh)"]==pytest.approx(rows[0]["Theoretical energy (MWh)"])
    assert rows[-1]["Initial heat loss (kW)"] > rows[0]["Initial heat loss (kW)"]


def test_insulation_shell_positive_and_wider_jacket_grows():
    assert insulation_shell_m3(D) > 0
    assert insulation_shell_m3(replace(D,insulation_m=.8)) > insulation_shell_m3(D)


def test_radial_insulation_profile_and_surface_heat():
    p=radial_insulation_profile(D,D.maximum_c)
    assert p["temperature_c"][0]==pytest.approx(D.maximum_c)
    assert np.all(np.diff(p["temperature_c"])<=1e-9)
    assert D.ambient_c < p["surface_c"] < D.maximum_c
    assert p["side_heat_kw_per_module"] > 0


def test_radial_profile_zero_delta_temperature():
    p=radial_insulation_profile(D,D.ambient_c)
    assert np.allclose(p["temperature_c"],D.ambient_c)
    assert p["side_heat_kw_per_module"]==pytest.approx(0)


def test_geometry_candidates_obey_height_and_diameter():
    results=bounded_geometry_candidates(D,M,max_height_m=30.,max_diameter_m=20.)
    assert len(results)>0
    assert all(x["Module height (m)"]<=30 for x in results)
    assert all(x["Outer diameter (m)"]<=20 for x in results)
    assert all(x["Initial loss (kW)"]>0 for x in results)


def test_geometry_screen_impossible_is_empty():
    assert bounded_geometry_candidates(D,M,2.,3.)==[]


def test_design_lab_page_starts_and_router_registers_new_pages():
    from streamlit.testing.v1 import AppTest
    from pathlib import Path
    root=Path(__file__).resolve().parents[1]
    app=AppTest.from_file(str(root/"streamlit_app.py"),default_timeout=75).run(timeout=75)
    assert not app.exception, [str(e.message) for e in app.exception]
    for path in ["pages/4_Thermal_Design_Studio.py","pages/5_Project_Research_Library.py"]:
        app.switch_page(path).run(timeout=75)
        assert not app.exception, [str(e.message) for e in app.exception]


def test_reference_page_contains_study_and_provenance_distinctions():
    from pathlib import Path
    root=Path(__file__).resolve().parents[1]
    content=(root/"pages/5_Project_Research_Library.py").read_text(encoding="utf-8")
    for marker in ("Bošnjaković","Vatajankoski","APA","no measured","not a calibration"):
        assert marker.lower() in content.lower()

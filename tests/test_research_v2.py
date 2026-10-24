"""v2 mathematical limits, energy closure and optional multipage startup."""
from dataclasses import replace
import numpy as np
import pytest
from engine.materials import MATERIALS
from engine.physics import Design
from engine.material_scenarios_v2 import SCENARIOS
from engine.research_v2 import (exergy_mwh,invert_energy,illustrative_renewables,dispatch,
    Exchanger,exchanger,ergun,uncertainty,levelized_heat,LTNE,ltne)
M=MATERIALS["Silica sand"];D=Design()

def test_exergy_less_than_thermal_energy():
    q=M.bulk_density*D.volume_m3*(M.enthalpy(550)-M.enthalpy(50))/3.6e9
    assert 0<exergy_mwh(M,1000,50,550,15)<q

def test_inverse_enthalpy():
    for temp in [50,150,500]:
        e=1000*(M.enthalpy(temp)-M.enthalpy(50))/3.6e9
        assert invert_energy(M,1000,e,50)==pytest.approx(temp)

def test_renewables_seed():
    assert np.array_equal(illustrative_renewables(48,seed=4),illustrative_renewables(48,seed=4))

def test_dispatch_energy_conservation_and_bounds():
    r=dispatch(D,M,illustrative_renewables(168),2)
    assert abs(r["balance_residual_mwh"])<1e-7
    assert np.min(r["soc_pct"])>=0
    assert np.max(r["soc_pct"])<=100+1e-8

def test_dispatch_no_source():
    r=dispatch(D,M,[0]*24,[2]*24)
    assert sum(r["delivered_mwh"])==0

def test_exchanger_energy_balance():
    p=Exchanger();r=exchanger(p)
    assert r["q_mw"]*1000==pytest.approx(p.ch_kw_k*(p.hot_in_c-r["hot_out_c"]))
    assert r["q_mw"]*1000==pytest.approx(p.cc_kw_k*(r["cold_out_c"]-p.cold_in_c))

def test_parallel_lower_than_counterflow():
    assert exchanger(Exchanger(kind="parallel"))["q_mw"]<exchanger(Exchanger(kind="counterflow"))["q_mw"]

def test_zero_ergun_drop():
    assert ergun(12,15,.42,.016,0)["delta_p_pa"]==0

def test_pressure_increases_with_flow():
    assert ergun(12,15,.42,.016,.02)["delta_p_pa"]<ergun(12,15,.42,.016,.06)["delta_p_pa"]

def test_sensitivity_repeatability():
    a=uncertainty(D,M,100,.1,seed=4)
    b=uncertainty(D,M,100,.1,seed=4)
    assert np.array_equal(a["capacity_samples_mwh"],b["capacity_samples_mwh"])

def test_lcoh_discount_zero():
    assert levelized_heat(1000,10,0,100,1,1,0,0)==pytest.approx(1.)

def test_ltne_conservation():
    r=ltne(replace(D,volume_m3=300),M,LTNE(cells=12,hours=1.5))
    assert abs(r["residual_mwh"])<.001
    assert np.std(r["solid_c"][-1])>0

def test_material_library_has_explicit_provenance():
    assert len(SCENARIOS)>=10
    assert all(x.provenance for x in SCENARIOS.values())

@pytest.mark.parametrize("filename",["pages/1_Engineering_Research_Lab.py","pages/2_Material_Atlas.py","pages/3_Virtual_Experiments.py"])
def test_optional_streamlit_pages_start(filename):
    from pathlib import Path
    from streamlit.testing.v1 import AppTest
    path=Path(__file__).resolve().parents[1]/filename
    app=AppTest.from_file(str(path),default_timeout=75).run(timeout=75)
    assert not app.exception,[(str(x.message)[:800]) for x in app.exception]

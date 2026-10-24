import math
from dataclasses import replace
import numpy as np
import pytest
from engine.materials import Material, MATERIALS, blend
from engine.physics import Design, geometry, thermal_ua, summarize, simulate_cycle
from engine.solar import csp_thermal_mw,electrical_renewables_mw
from engine.thermocline import simulate_thermocline
from engine.optimization import screen_designs
from visuals import timeline,ledger,plant_3d,material_comparison
import pandas as pd

SAND=MATERIALS['Silica sand']

def test_geometry_preserves_volume():
    for vol in [100,1000,10000]:
        r,h=geometry(vol,3)
        assert math.pi*r*r*h==pytest.approx(vol,rel=1e-12)

def test_negative_geometry_rejected():
    with pytest.raises(ValueError):geometry(0,2)

def test_temperature_enthalpy_integral_constant_cp():
    m=Material('Reference',1600,1000,0)
    d=Design(volume_m3=100,minimum_c=50,maximum_c=550)
    assert summarize(d,m)['capacity_mwh']==pytest.approx(100*1600*1000*500/3.6e9)

def test_temperature_enthalpy_derivative():
    T=350
    h=1e-3
    assert (SAND.enthalpy(T+h)-SAND.enthalpy(T-h))/(2*h)==pytest.approx(SAND.cp(T),rel=1e-9)

def test_insulation_reduces_ua():
    assert thermal_ua(5,15,1,.06,10)<thermal_ua(5,15,.2,.06,10)

def test_more_modules_increase_surface_losses():
    d=Design()
    assert summarize(replace(d,modules=4),SAND)['ua_w_k']>summarize(d,SAND)['ua_w_k']

def test_volume_blend_conserves_rho_cp():
    basalt=MATERIALS['Crushed basalt']
    x=.25
    b=blend(SAND,basalt,x,'volume')
    assert b.bulk_density*b.cp(300)==pytest.approx(x*SAND.bulk_density*SAND.cp(300)+(1-x)*basalt.bulk_density*basalt.cp(300))

def test_mass_blend_preserves_fraction_endpoints():
    b=blend(SAND,MATERIALS['Crushed basalt'],1,'mass')
    assert b.bulk_density==pytest.approx(SAND.bulk_density)
    assert b.cp(400)==pytest.approx(SAND.cp(400))

def test_invalid_blend_rejected():
    with pytest.raises(ValueError):blend(SAND,SAND,1.2)

def test_csp_conversion():
    assert csp_thermal_mw(10000,850,.7)==pytest.approx(5.95)

def test_renewable_conversion():
    assert electrical_renewables_mw(10,.2,8,.4)==pytest.approx(5.2)

def test_nominal_cycle_energy_conservation():
    r=simulate_cycle(Design(),SAND)
    assert 0 <r['useful_heat_mwh']<r['capacity_mwh']<r['electric_input_mwh']
    assert abs(r['energy_balance_residual_mwh'])<1e-7
    assert 0 <r['electricity_to_useful_heat_pct']<100
    assert r['hold_end_c']<550

def test_energy_conservation_multi_module():
    r=simulate_cycle(Design(modules=4),SAND)
    assert abs(r['energy_balance_residual_mwh'])<1e-7

def test_standby_lowers_delivery():
    a=simulate_cycle(Design(hold_days=0),SAND)
    b=simulate_cycle(Design(hold_days=3),SAND)
    assert a['useful_heat_mwh']>b['useful_heat_mwh']

def test_high_insulation_approaches_heater_efficiency():
    d=Design(volume_m3=100,insulation_m=30,conductivity_w_mk=.001,
             charge_mw=1,thermal_output_mw=.5,hold_days=0)
    assert simulate_cycle(d,SAND)['electricity_to_useful_heat_pct']==pytest.approx(99,abs=.02)

def test_unreachable_charge_rejected():
    with pytest.raises(ValueError):simulate_cycle(Design(volume_m3=100,insulation_m=.05,conductivity_w_mk=1,charge_mw=.001),SAND)

def test_invalid_max_temp_rejected():
    with pytest.raises(ValueError):simulate_cycle(Design(minimum_c=500,maximum_c=300),SAND)

def test_1d_finite_responses():
    d=Design(volume_m3=100,charge_mw=1,thermal_output_mw=.5,hold_days=.1)
    tc=simulate_thermocline(d,SAND,n_cells=24)
    assert 0<tc['useful_heat_mwh']<tc['nominal_capacity_mwh']
    assert np.isfinite(tc['hold_profile_c']).all()
    assert tc['electric_input_mwh']>tc['useful_heat_mwh']

def test_screening_respects_constraints():
    d=Design(volume_m3=100,charge_mw=1,thermal_output_mw=.5)
    rows=screen_designs(d,SAND,[100,200],[2,3],[.3],14,12)
    assert rows
    assert all(x['module_height_m']<=14 and x['module_outer_diameter_m']<=12 for x in rows)
    assert rows==sorted(rows,key=lambda row:row['usable_mwh'],reverse=True)

def test_chart_construction():
    d=Design(volume_m3=100,charge_mw=1,thermal_output_mw=.5)
    r=simulate_cycle(d,SAND)
    assert len(timeline(r).data)==3
    assert len(plant_3d(r,d).frames)==5
    assert ledger(r) is not None
    sample=pd.DataFrame([{'Theoretical MWh':10.0,'Material':'Silica sand'}])
    assert len(material_comparison(sample).data)==1


def test_charge_time_agrees_with_independent_temperature_integral():
    from scipy.integrate import quad
    d=Design(volume_m3=100, charge_mw=1, thermal_output_mw=.5,hold_days=0)
    s=summarize(d,SAND)
    mass=d.volume_m3*SAND.bulk_density
    ua=s['ua_w_k']
    p_heat=d.charge_mw*1e6*d.charge_efficiency
    reference_s=quad(lambda T: mass*SAND.cp(T)/(p_heat-ua*(T-d.ambient_c)),
                     d.minimum_c,d.maximum_c,epsabs=1e-7)[0]
    res=simulate_cycle(d,SAND)
    assert res['charge_hours']*3600==pytest.approx(reference_s,rel=2e-7)


def test_discharge_time_agrees_with_independent_temperature_integral():
    from scipy.integrate import quad
    d=Design(volume_m3=100, charge_mw=1, thermal_output_mw=.5,hold_days=2)
    res=simulate_cycle(d,SAND)
    mass=d.volume_m3*SAND.bulk_density
    ua=res['ua_w_k'];p_out=d.thermal_output_mw*1e6
    reference_s=quad(lambda T:mass*SAND.cp(T)/(p_out+ua*(T-d.ambient_c)),
                     d.minimum_c,res['hold_end_c'],epsabs=1e-7)[0]
    assert res['discharge_hours']*3600==pytest.approx(reference_s,rel=2e-7)


def test_solar_thermal_input_is_not_mislabeled_electricity():
    d=Design(volume_m3=100,charge_mw=1,thermal_output_mw=.5,source_kind='solar_thermal',charge_efficiency=1)
    r=simulate_cycle(d,SAND)
    assert r['source_kind']=='solar_thermal'
    assert r['electricity_to_useful_heat_pct'] is None
    assert r['electric_input_mwh'] is None
    assert r['source_to_useful_heat_pct']>0
    assert abs(r['energy_balance_residual_mwh'])<1e-7

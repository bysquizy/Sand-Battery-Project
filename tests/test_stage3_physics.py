"""Stage 3: independent physics, model-domain and regression checks."""
from dataclasses import replace
from pathlib import Path

import numpy as np
import pytest

from engine.closed_pipe import PipeLoop, pipe_transfer, simulate_closed_pipe
from engine.materials import MATERIALS
from engine.physics import Design
from engine.property_curves import TabulatedMaterial
from engine.thermocline import simulate_thermocline

ROOT = Path(__file__).resolve().parents[1]
M = MATERIALS["Silica sand"]
D = Design()


def test_pipe_model_has_positive_finite_resistances():
    p = pipe_transfer(PipeLoop(), D)
    assert p["ua_w_k"] > 0
    assert p["r_fluid_k_w"] > 0
    assert p["r_wall_k_w"] > 0
    assert p["r_solid_k_w"] > 0
    assert p["ntu"] > 0
    assert 0 < p["effectiveness"] < 1
    assert p["representative_volume_fraction"] < 1
    assert p["ua_w_k"] == pytest.approx(
        1 / (p["r_fluid_k_w"]+p["r_wall_k_w"]+p["r_solid_k_w"])
    )


def test_pipe_heat_transfer_rises_with_more_pipes_and_better_solid_conductivity():
    default = pipe_transfer(PipeLoop(),D)["ua_w_k"]
    more = pipe_transfer(PipeLoop(tubes=60),D)["ua_w_k"]
    improved = pipe_transfer(PipeLoop(effective_solid_k_w_mk=2),D)["ua_w_k"]
    assert more > default
    assert improved > default


def test_closed_pipe_energy_balance_and_useful_grade():
    model = simulate_closed_pipe(D,M)
    assert model["charge_hours"] > 0
    assert model["useful_heat_mwhth"] > 0
    assert model["ambient_loss_mwhth"] > 0
    assert model["discharge_hours"] > 0
    assert model["loop_input_mwhth"] > model["useful_heat_mwhth"]
    assert model["initial_delivery_outlet_c"] >= D.minimum_c
    assert abs(model["energy_balance_residual_mwhth"]) < 0.001
    assert model["thermal_delivery_fraction_pct"] <= 100


def test_closed_pipe_low_ua_reduces_effectiveness():
    weak = pipe_transfer(PipeLoop(effective_solid_k_w_mk=.2),D)
    strong = pipe_transfer(PipeLoop(effective_solid_k_w_mk=2),D)
    assert weak["effectiveness"] < strong["effectiveness"]
    assert weak["minimum_solid_for_delivery_c"] > strong["minimum_solid_for_delivery_c"]


@pytest.mark.parametrize("parameters",[
    PipeLoop(tubes=0),
    PipeLoop(tubes=True),
    PipeLoop(length_m=-1),
    PipeLoop(pitch_m=.01),
    PipeLoop(tubes=1500,pitch_m=.5),
    PipeLoop(mass_flow_kg_s=float("nan")),
    PipeLoop(fluid_h_w_m2k=50000),
    PipeLoop(hot_inlet_c=540),
    PipeLoop(return_inlet_c=200,useful_outlet_c=100),
])
def test_pipe_rejects_invalid_or_unphysical_inputs(parameters):
    with pytest.raises(ValueError):
        pipe_transfer(parameters,D)


def test_closed_pipe_lumped_solid_can_use_other_assumed_medium():
    out=simulate_closed_pipe(D,MATERIALS["Crushed basalt"])
    assert np.isfinite(out["energy_balance_residual_mwhth"])
    assert abs(out["energy_balance_residual_mwhth"]) < 0.001


def test_tabulated_cp_integrates_constant_cp_exactly():
    t=TabulatedMaterial("Test",1600,(25.,250.,500.),(900.,900.,900.),"synthetic")
    assert t.cp(400) == 900
    assert t.enthalpy(500)-t.enthalpy(25) == pytest.approx(900*475)
    assert t.enthalpy(25) == 0
    assert t.cp(np.array([25,250,500])).tolist() == [900,900,900]


def test_tabulated_cp_integrates_linearly_varying_cp_exactly():
    t=TabulatedMaterial("Test",1600,(25.,525.),(700.,1200.),"synthetic")
    assert t.cp(275) == pytest.approx(950)
    assert t.enthalpy(525) == pytest.approx((700+1200)*500/2)
    x=np.linspace(25,525,101)
    assert np.all(np.diff(t.enthalpy(x)) > 0)


@pytest.mark.parametrize("change",[
    {"temperatures_c":(25.,25.)},
    {"temperatures_c":(25.,500.),"cp_j_kgk":(1.,)},
    {"cp_j_kgk":(900.,float("nan"))},
    {"cp_j_kgk":(900.,-1.)},
    {"bulk_density":float("inf")},
    {"provenance":""},
])
def test_tabulated_cp_rejects_unreliable_data(change):
    args={"name":"Test","bulk_density":1600,"temperatures_c":(25.,500.),
          "cp_j_kgk":(900.,1000.),"provenance":"synthetic"}
    args.update(change)
    with pytest.raises(ValueError):
        TabulatedMaterial(**args)


def test_tabulated_cp_fails_closed_outside_supported_temperatures():
    t=TabulatedMaterial("Test",1600,(25.,500.),(900.,1000.),"synthetic")
    with pytest.raises(ValueError):
        t.cp(505)
    with pytest.raises(ValueError):
        t.enthalpy(20)


def test_axial_model_energy_ledger_and_cutoffs_are_explicit():
    result=simulate_thermocline(D,M,n_cells=24,
            charge_cutoff_pct=10,discharge_cutoff_pct=70)
    for key in ("charge_loss_mwh","standby_loss_mwh","discharge_loss_mwh",
                "energy_balance_residual_mwh","final_relative_energy_mwh"):
        assert np.isfinite(result[key])
    assert result["charge_cutoff_pct"] == 10
    assert result["discharge_cutoff_pct"] == 70
    # Explicit finite-volume update with cp(T) produces a discretization
    # residual; require it to be small relative to source input, not exactly 0.
    assert abs(result["energy_balance_residual_mwh"]) < .02*max(
        1.0, result["electric_input_mwh"])


def test_axial_multiple_modules_scale_energy_and_residual():
    base=simulate_thermocline(replace(D,volume_m3=500,modules=1,
                                     charge_mw=2.5,thermal_output_mw=1),M,16)
    double=simulate_thermocline(replace(D,modules=2),M,16)
    assert double["nominal_capacity_mwh"] == pytest.approx(2*base["nominal_capacity_mwh"])
    assert double["electric_input_mwh"] == pytest.approx(2*base["electric_input_mwh"])
    assert double["energy_balance_residual_mwh"] == pytest.approx(2*base["energy_balance_residual_mwh"])


def test_model_verification_page_starts_from_router():
    from streamlit.testing.v1 import AppTest
    app=AppTest.from_file(str(ROOT/"streamlit_app.py"),default_timeout=75).run(timeout=75)
    assert not app.exception, [str(e.message) for e in app.exception]
    app.switch_page("pages/7_Model_Verification.py").run(timeout=75)
    assert not app.exception, [str(e.message) for e in app.exception]

def test_stage_1_2_json_safety_rejects_duplicate_fields():
    from engine.scenarios import Scenario, SLOTS, to_json, from_json
    bundle=to_json(Scenario(),{slot: None for slot in SLOTS})
    # A duplicate top-level key is ambiguous and must not silently override.
    with pytest.raises(ValueError):
        from_json(bundle.replace('"schema_version": 1,',
                                  '"schema_version": 1, "schema_version": 1,').encode())


def test_stage_1_2_research_is_lazily_rendered():
    text=(ROOT/"pages/1_Engineering_Research_Lab.py").read_text(encoding="utf-8")
    assert 'study = st.radio(' in text
    assert "elif study == 'Cost Lab':" in text
    assert 'energy,renewable,transport,exchanger_tab,risk,cost=st.tabs' not in text

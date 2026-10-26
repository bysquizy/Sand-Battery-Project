"""Stage 4/5: grounded visuals, reproducible exports and source integrity."""
from __future__ import annotations

from dataclasses import replace
from pathlib import Path
import re

import numpy as np
import pytest

from engine.materials import MATERIALS
from engine.physics import Design, simulate_cycle
from engine.scenarios import Scenario
from engine.report_exports import html_report, pdf_report
from engine.thermocline import simulate_thermocline
from project_info import PROJECT, MODEL_EVIDENCE
from visuals_advanced import (
    axial_cylinder_animation, axial_history_heatmap,
    design_frontier_chart, sensitivity_tornado,
)

ROOT=Path(__file__).resolve().parents[1]
D=Design()
M=MATERIALS["Silica sand"]


def test_thermocline_history_is_computed_and_physically_bounded():
    result=simulate_thermocline(D,M,n_cells=16)
    t=result["animation_times_h"]
    snap=result["animation_profiles_c"]
    phases=result["animation_phases"]
    assert snap.shape[1] == 16
    assert snap.shape[0] == len(t) == len(phases)
    assert 4 <= len(t) <= 120
    assert np.all(np.isfinite(snap))
    assert np.all(np.diff(t) >= -1e-10)
    assert np.allclose(snap[0],D.minimum_c)
    assert np.allclose(snap[-1],result["discharge_profile_c"])
    assert np.allclose(snap[np.where(np.array(phases)=="Charged")[0][-1]],
                       result["charge_profile_c"])


def test_thermocline_history_inherits_selected_geometry():
    d=replace(D,volume_m3=500,modules=2,charge_mw=4,thermal_output_mw=2)
    result=simulate_thermocline(d,M,n_cells=16)
    assert result["animation_profiles_c"].shape[1] == 16
    assert result["nominal_capacity_mwh"] > 0


def test_3d_animation_uses_computed_profiles_and_finite_axes():
    result=simulate_thermocline(D,M,n_cells=16)
    fig=axial_cylinder_animation(result,2.5,D.minimum_c,D.maximum_c)
    assert len(fig.frames) >= 3
    assert len(fig.frames) <= 28
    assert len(fig.data) == 1
    assert len(fig.frames[0].data) == 1
    assert np.isclose(fig.data[0].surfacecolor[0,0],
                      result["animation_profiles_c"][0,0])
    heatmap=axial_history_heatmap(result)
    assert heatmap.data[0].z.shape==result["animation_profiles_c"].shape


def test_visualization_rejects_fake_or_nonfinite_snapshots():
    result=simulate_thermocline(D,M,n_cells=16)
    broken=dict(result,animation_profiles_c=np.array([[float("nan")]*16]*2))
    with pytest.raises(ValueError):
        axial_history_heatmap(broken)
    with pytest.raises(ValueError):
        axial_cylinder_animation(result,0,50,550)


def test_trades_and_tornado_are_pure_data_figures():
    rows=[
        {"insulation_m":.4,"volume_m3":1000,"modules":1,
         "initial_loss_kw":20,"useful_heat_mwh":130},
        {"insulation_m":.6,"volume_m3":1200,"modules":2,
         "initial_loss_kw":16,"useful_heat_mwh":150},
    ]
    fig=design_frontier_chart(rows)
    assert len(fig.data)==2
    fig=sensitivity_tornado(150,[{"parameter":"Packed volume",
        "low_mwh":130,"high_mwh":170}])
    assert len(fig.data)==2


def test_offline_html_report_contains_actual_numerical_ledger_and_provenance():
    s=Scenario()
    r=simulate_cycle(s.make_design(),M,max_step_s=3600)
    html=html_report(s,r).decode("utf-8")
    assert "<!DOCTYPE html>" in html
    assert "<svg" in html and "<polyline" in html
    assert "Group 8" in html and "Yağız Topaç" in html
    assert "Fatma Ovacık" in html and "Semih Cenk" in html
    assert "Energy ledger residual" in html
    assert "NOT experimental validation" in html
    assert "https://doi.org/10.3390/cleantechnol8050165" in html
    assert "fonts.googleapis.com" not in html and "<script" not in html


def test_html_report_escapes_untrusted_scenario_title():
    s=replace(Scenario(),name="<svg onload=bad()>")
    r=simulate_cycle(s.make_design(),M,max_step_s=3600)
    text=html_report(s,r).decode("utf-8")
    assert "&lt;svg onload=bad()&gt;" in text
    assert "<svg onload=bad()>" not in text


def test_compact_pdf_has_valid_structure_and_multiple_pages():
    s=Scenario()
    r=simulate_cycle(s.make_design(),M,max_step_s=3600)
    pdf=pdf_report(s,r)
    assert pdf.startswith(b"%PDF-1.4")
    assert pdf.rstrip().endswith(b"%%EOF")
    assert b"/Type /Catalog" in pdf
    assert b"/Type /Pages" in pdf
    assert b"/Type /Page " in pdf
    assert re.search(rb"xref\n0 [0-9]+\n0000000000 65535 f",pdf)
    assert len(pdf) > 1200


def test_invalid_results_are_not_accepted_in_exports():
    s=Scenario()
    r=simulate_cycle(s.make_design(),M,max_step_s=3600)
    broken=dict(r,capacity_mwh=float("nan"))
    with pytest.raises(ValueError):
        pdf_report(s,broken)
    with pytest.raises(ValueError):
        html_report(s,broken)


def test_model_evidence_includes_new_methods_and_its_limits():
    methods={row["method"] for row in MODEL_EVIDENCE}
    for name in ("Closed-pipe lumped heat-transfer study",
                 "Multilayer cylindrical insulation",
                 "Tabulated material enthalpy",
                 "Mapped 1-D axial visualization",
                 "Offline scenario report"):
        assert name in methods
    assert PROJECT["members"]==("Yağız Topaç","Semih Cenk","Fatma Ovacık")


def test_visual_story_router_opens_and_switches_workspace():
    from streamlit.testing.v1 import AppTest
    app=AppTest.from_file(str(ROOT/"streamlit_app.py"),default_timeout=75).run(timeout=75)
    assert not app.exception,[str(e.message) for e in app.exception]
    app.switch_page("pages/8_Visual_Story_Studio.py").run(timeout=75)
    assert not app.exception,[str(e.message) for e in app.exception]
    app.radio(key="visual_workspace").set_value("Engineering report").run(timeout=75)
    assert not app.exception,[str(e.message) for e in app.exception]


def test_publication_files_and_dependencies_remain_light():
    assert (ROOT/"assets/architecture.svg").exists()
    for path in ("docs/EQUATION_TRACEABILITY.md","docs/RELEASE_2_0_QA.md"):
        assert (ROOT/path).exists()
    req=(ROOT/"requirements.txt").read_text(encoding="utf-8").strip().splitlines()
    assert len(req)==5
    assert all(not key in "\n".join(req) for key in
               ("kaleido","reportlab","selenium","matplotlib"))

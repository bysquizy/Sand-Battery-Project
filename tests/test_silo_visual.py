"""Source-grounded layered rendering and functional controls."""
from dataclasses import replace
from pathlib import Path

import numpy as np
import pytest
from streamlit.testing.v1 import AppTest

from engine.materials import MATERIALS
from engine.physics import Design, simulate_cycle
from silo_visual import cycle_snapshots, layered_silo

SAND = MATERIALS['Silica sand']
ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope='module')
def cycle():
    design = Design()
    return design, simulate_cycle(design, SAND)


def test_playback_selects_actual_solver_samples_and_exact_enthalpy(cycle):
    design, result = cycle
    samples = cycle_snapshots(result, design, SAND)
    source = {(float(t), float(temp)) for phase in ('charge', 'hold', 'discharge')
              for t, temp in zip(result[f'{phase}_trace_h'], result[f'{phase}_trace_c'])}
    assert 3 <= len(samples) <= 36
    assert all((p['time_h'], p['temperature_c']) in source for p in samples)
    assert all(b['time_h'] >= a['time_h'] for a, b in zip(samples, samples[1:]))
    assert samples[0]['time_h'] == 0
    assert samples[-1]['time_h'] == result['discharge_trace_h'][-1]
    assert samples[-1]['temperature_c'] == result['discharge_trace_c'][-1]
    assert max(p['usable_stored_mwh'] for p in samples) == pytest.approx(result['capacity_mwh'])
    assert samples[-1]['usable_stored_mwh'] == pytest.approx(max(0, result['ending_relative_energy_mwh']), abs=1e-6)


def test_cutaway_updates_core_only_and_preserves_actual_dimensions(cycle):
    design, result = cycle
    fig = layered_silo(result, design, SAND)
    thermal = fig.layout.meta['thermal_trace_indices']
    assert thermal
    assert fig.layout.scene.aspectmode == 'data'
    assert max(np.hypot(fig.data[0].x, fig.data[0].y).ravel()) == pytest.approx(result['outer_diameter_m']/2)
    assert np.max(fig.data[0].z) == pytest.approx(result['height_m'])
    for frame, sample in zip(fig.frames, fig.layout.meta['samples']):
        assert list(frame.traces) == thermal
        for trace in frame.data:
            assert np.all(np.asarray(trace.surfacecolor) == sample['temperature_c'])
            assert trace.x is None and trace.y is None and trace.z is None
        assert len(frame.layout.annotations) == 4
    assert len(fig.to_json()) < 2_000_000


def test_exterior_never_colors_steel_as_bulk_temperature(cycle):
    design, result = cycle
    fig = layered_silo(result, design, SAND, cutaway=False)
    assert not fig.layout.meta['thermal_trace_indices']
    assert all(len(frame.data) == 0 for frame in fig.frames)
    assert fig.data[0].hovertemplate.find('°C') == -1
    assert all(step.label == '' for step in fig.layout.sliders[0].steps)
    assert fig.layout.updatemenus[0].direction == 'left'
    assert fig.layout.scene.domain.y[0] > fig.layout.updatemenus[0].y


def test_zero_hold_and_cooled_below_tmin_are_supported():
    for design in [Design(hold_days=0), Design(volume_m3=50, hold_days=30, insulation_m=.1)]:
        result = simulate_cycle(design, SAND)
        samples = cycle_snapshots(result, design, SAND)
        assert np.all(np.isfinite([p['temperature_c'] for p in samples]))
        assert all(p['usable_stored_mwh'] >= 0 for p in samples)
        assert samples[-1]['temperature_c'] == result['discharge_trace_c'][-1]


def test_material_and_module_selection_remain_part_of_the_model():
    design = replace(Design(), modules=4)
    basalt = MATERIALS['Crushed basalt']
    result = simulate_cycle(design, basalt)
    samples = cycle_snapshots(result, design, basalt)
    assert max(p['usable_stored_mwh'] for p in samples) == pytest.approx(result['capacity_mwh'])
    fig = layered_silo(result, design, basalt)
    assert any('Crushed basalt' in trace.hovertemplate for trace in fig.data if trace.type == 'surface')


def test_invalid_trace_is_rejected(cycle):
    design, result = cycle
    for change in [dict(charge_trace_c=[float('nan')]), dict(hold_trace_h=[-1, -2])]:
        with pytest.raises(ValueError):
            cycle_snapshots(dict(result, **change), design, SAND)


def test_dashboard_cutaway_exterior_language_and_light_mode():
    ui = AppTest.from_file(str(ROOT/'streamlit_app.py'), default_timeout=75).run()
    ui.radio(key='home_workspace').set_value('3D Plant Explorer').run()
    assert not ui.exception
    assert ui.radio(key='silo_presentation').value == 'cutaway'
    ui.radio(key='silo_presentation').set_value('exterior').run()
    ui.selectbox(key='sb_language_select').set_value('Türkçe').run()
    assert not ui.exception
    assert ui.radio(key='silo_presentation').value == 'exterior'
    assert len(ui.get('plotly_chart')) == 1
    ui.toggle(key='low_power_mode').set_value(True).run()
    assert not ui.exception
    assert len(ui.get('plotly_chart')) == 0

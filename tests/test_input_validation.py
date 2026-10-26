"""Stage 1: malicious/invalid upload boundaries and temperature-sweep regression."""
import numpy as np
import pytest

from engine.input_validation import (
    MAX_CSV_BYTES,
    MAX_HOURLY_ROWS,
    parse_hourly_dispatch_csv,
    temperature_sweep,
)


def test_csv_accepts_valid_hourly_power():
    supply, demand = parse_hourly_dispatch_csv(
        b"available_mw,demand_mw\n0,2.5\n3.25,0\n"
    )
    assert supply.tolist() == [0.0, 3.25]
    assert demand.tolist() == [2.5, 0.0]


@pytest.mark.parametrize(
    "payload",
    [
        b"",
        b"wrong,fields\n1,2\n",
        b"available_mw,available_mw,demand_mw\n1,2,3\n",
        b"available_mw,demand_mw\nhello,2\n",
        b"available_mw,demand_mw\nNaN,2\n",
        b"available_mw,demand_mw\n1,inf\n",
        b"available_mw,demand_mw\n-1,2\n",
        b"available_mw,demand_mw\n1001,2\n",
        b"available_mw,demand_mw\n1,\n",
        b"available_mw,demand_mw\n",
        b"available_mw,demand_mw\n1,2,3\n",
        b"\xff\xfe",
        b"available_mw,demand_mw\n" + b"1,2\n" * (MAX_HOURLY_ROWS + 1),
        b"available_mw,demand_mw\n1,2\n" + b" " * MAX_CSV_BYTES,
    ],
)
def test_csv_rejects_bad_or_unbounded_payload(payload):
    with pytest.raises(ValueError):
        parse_hourly_dispatch_csv(payload)


def test_csv_accepts_full_year_at_resource_limit():
    blob = b"available_mw,demand_mw\n" + b"1,2\n" * MAX_HOURLY_ROWS
    source, demand = parse_hourly_dispatch_csv(blob)
    assert len(source) == MAX_HOURLY_ROWS
    assert np.isclose(source.sum(), MAX_HOURLY_ROWS)
    assert np.all(demand == 2)


def test_heatmap_grid_never_exceeds_selected_maximum():
    for low, high in ((60, 250), (60, 270), (60, 330), (60, 550), (200, 850)):
        grid = temperature_sweep(low, high)
        assert len(grid) == 8
        assert grid[0] == low and grid[-1] == high
        assert np.all(grid >= low)
        assert np.all(grid <= high)
        assert np.all(np.diff(grid) > 0)


@pytest.mark.parametrize(
    "low,high,n",
    [
        (100, 100, 8),
        (200, 150, 8),
        (float("nan"), 500, 8),
        (50, float("inf"), 8),
        (50, 500, 1),
        (50, 500, 251),
    ],
)
def test_heatmap_grid_rejects_invalid_boundaries(low, high, n):
    with pytest.raises(ValueError):
        temperature_sweep(low, high, n)


def test_atlas_renders_with_user_high_below_300():
    from pathlib import Path
    from streamlit.testing.v1 import AppTest

    page = Path(__file__).resolve().parents[1] / "pages/2_Material_Atlas.py"
    app = AppTest.from_file(str(page), default_timeout=75).run(timeout=75)
    app.number_input(key="atlas_high").set_value(250.0).run(timeout=75)
    assert not app.exception, [str(error.message) for error in app.exception]

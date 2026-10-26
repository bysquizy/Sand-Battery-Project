"""Small, testable input-boundary checks for the hosted research app.

This module validates user files BEFORE running a numerical solver. It does not
modify the thermodynamic models or manufacture measurement-quality input data.
"""
from __future__ import annotations

import csv
import io

import numpy as np
import pandas as pd

MAX_CSV_BYTES = 1_000_000
MAX_HOURLY_ROWS = 8_760
MAX_HOURLY_MW = 1_000.0
MAX_CSV_COLUMNS = 16
HOURLY_COLUMNS = ("available_mw", "demand_mw")


def parse_hourly_dispatch_csv(blob: bytes) -> tuple[np.ndarray, np.ndarray]:
    """Return validated hourly MW source and demand arrays, without interpolation.

    Unit: megawatts (MW) per hourly row. Maximum 8,760 rows (one 365-day
    year), 1 MB uploaded data, and 1,000 MW per field. The cap is a server
    resource limit, NOT a claim about realistic project plant ratings.
    """
    if not isinstance(blob, bytes) or not blob:
        raise ValueError("Upload a non-empty CSV file.")
    if len(blob) > MAX_CSV_BYTES:
        raise ValueError("CSV must not exceed 1 MB.")
    try:
        decoded = blob.decode("utf-8-sig")
        if "\x00" in decoded:
            raise ValueError("CSV must not contain NUL bytes.")
        reader = csv.reader(io.StringIO(decoded), strict=True)
        columns = [name.strip() for name in next(reader)]
        if len(columns) != len(set(columns)):
            raise ValueError("Duplicate CSV column names are not permitted.")
        if not columns or len(columns) > MAX_CSV_COLUMNS:
            raise ValueError("CSV has an invalid number of columns.")
        if any(column not in columns for column in HOURLY_COLUMNS):
            raise ValueError("CSV requires available_mw and demand_mw columns.")
        rows = 0
        for row in reader:
            rows += 1
            if rows > MAX_HOURLY_ROWS:
                raise ValueError("CSV must not exceed 8,760 hourly rows.")
            if len(row) != len(columns):
                raise ValueError("Every CSV row must match the header width.")
        data = pd.read_csv(io.StringIO(decoded), on_bad_lines="error")
        data.columns = [str(name).strip() for name in data.columns]
    except (UnicodeError, csv.Error, pd.errors.ParserError, StopIteration) as exc:
        raise ValueError("CSV must contain UTF-8 text and valid rows.") from exc

    if not 1 <= len(data) <= MAX_HOURLY_ROWS:
        raise ValueError("CSV must contain between 1 and 8,760 hourly rows.")

    series = []
    for column in HOURLY_COLUMNS:
        try:
            values = pd.to_numeric(data[column], errors="raise").to_numpy(dtype=float)
        except (TypeError, ValueError) as exc:
            raise ValueError(f"{column} contains nonnumeric values.") from exc
        if not np.all(np.isfinite(values)):
            raise ValueError(f"{column} contains missing, NaN or infinite values.")
        if np.any(values < 0) or np.any(values > MAX_HOURLY_MW):
            raise ValueError(f"{column} must be between 0 and 1,000 MW.")
        series.append(values)
    return series[0], series[1]


def temperature_sweep(minimum_c: float, maximum_c: float, n: int = 8) -> np.ndarray:
    """Return a temperature grid constrained to the user-selected interval.

    No temperature above maximum_c or below minimum_c is ever sampled.
    """
    if (
        not np.isfinite(minimum_c)
        or not np.isfinite(maximum_c)
        or maximum_c <= minimum_c
    ):
        raise ValueError("Require finite temperatures with Tmin below Tmax.")
    if type(n) is not int or not 2 <= n <= 250:
        raise ValueError("Grid samples must be between 2 and 250.")
    return np.linspace(float(minimum_c), float(maximum_c), n)

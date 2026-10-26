"""Safe spreadsheet-friendly CSV serialization for user-provided labels.

Protect against CSV/spreadsheet formula injection in downloaded files. Numeric
model values stay numeric and no CSV dialect or external package is required
beyond the pandas dependency already used by the app.
"""
from __future__ import annotations

import io
import re

import pandas as pd

# Spreadsheet applications may ignore leading whitespace before formula chars.
_DANGEROUS = re.compile(r"^[\s\uFEFF]*[=+@\-]")


def csv_cell(value: object) -> object:
    """Prevent user-entered labels from becoming spreadsheet formulas."""
    if isinstance(value, str) and _DANGEROUS.match(value):
        return "'" + value
    return value


def safe_csv(frame: pd.DataFrame) -> str:
    """CSV text with formula-escaped string cells, UTF-8 compatible."""
    clean = frame.copy(deep=True)
    for name in clean.columns:
        if (pd.api.types.is_object_dtype(clean[name])
                or pd.api.types.is_string_dtype(clean[name])):
            clean[name] = clean[name].map(csv_cell)
    return clean.to_csv(index=False)

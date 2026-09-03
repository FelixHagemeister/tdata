"""Loader for hand-curated indicator rows.

Some sources publish key figures only inside PDF reports. Rather than
brittle PDF table parsing, those figures are transcribed into
``sources/<source_id>/curated.csv`` with a page reference. This module
loads such files into the harmonized schema.
"""
from __future__ import annotations

import pathlib

import pandas as pd

from .schema import finalize

_ROOT = pathlib.Path(__file__).parent.parent


def load_curated(source_id: str) -> pd.DataFrame:
    path = _ROOT / "sources" / source_id / "curated.csv"
    if not path.exists():
        raise FileNotFoundError(path)
    df = pd.read_csv(path, dtype=str, keep_default_na=False)
    for col in ["value", "ci_lower", "ci_upper", "n"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col].replace("", pd.NA), errors="coerce")
    df["year"] = df["year"].astype(int)
    df["source_id"] = source_id
    return finalize(df)

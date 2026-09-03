"""Fetch the RKI Diabetes-Surveillance indicator set (open data).

The Diabetes Surveillance publishes smoking as a diabetes risk factor with a
long time series for adults (GEDA/GSTel surveys 2003–2019) and for children
and adolescents (KiGGS waves), including Bundesland values for 2019.
Access: free, CC BY 4.0, published on GitHub and Zenodo.
"""
from __future__ import annotations
import pathlib

import pandas as pd
import requests

_SOURCE_ID = "rki_diabetes_surveillance"
_FILE = "Diabetes-Surveillance_Indikatoren.tsv"
_URL = "https://raw.githubusercontent.com/robert-koch-institut/Diabetes-Surveillance/main/" + _FILE
LANDING_URL = "https://github.com/robert-koch-institut/Diabetes-Surveillance"


def fetch(cache_dir: str = "data/", tobacco_only: bool = True,
          refresh: bool = False) -> pd.DataFrame:
    """Return the Diabetes-Surveillance indicator table (smoking rows by default)."""
    cache = pathlib.Path(cache_dir) / _SOURCE_ID
    cache.mkdir(parents=True, exist_ok=True)
    path = cache / _FILE
    if refresh or not path.exists():
        resp = requests.get(_URL, timeout=120)
        resp.raise_for_status()
        path.write_bytes(resp.content)
    df = pd.read_csv(path, sep="\t", low_memory=False)
    if tobacco_only:
        df = df[df["Indikator_Name"].astype(str).str.contains("Rauchen|Tabak", regex=True)].copy()
    return df.reset_index(drop=True)


if __name__ == "__main__":
    result = fetch()
    print(result.head(10).to_string())
    print(f"\n{len(result)} rows, {len(result.columns)} columns")

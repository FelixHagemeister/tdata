"""Fetch RKI GEDA (Gesundheit in Deutschland aktuell) results.

Free path (default): the RKI publishes aggregated GEDA 2019/2020-EHIS results as
open data on GitHub (CC BY 4.0) — prevalences by Bundesland, sex, age group and
education for every indicator, including smoking (RCstatE_k3) and passive
smoking (RCpass4B_k2). This is downloaded automatically.

Microdata (all waves) require a data-use agreement with the RKI FDZ; see the
error message raised by ``fetch(microdata=True)``.
"""
from __future__ import annotations
import pathlib

import pandas as pd
import requests

_SOURCE_ID = "rki_geda"
_CSV_URL = ("https://raw.githubusercontent.com/robert-koch-institut/Gesundheit_in_Deutschland_Aktuell/"
            "main/Gesundheit_in_Deutschland_aktuell_-_2019-2020-EHIS.csv")
LANDING_URL = "https://github.com/robert-koch-institut/Gesundheit_in_Deutschland_Aktuell"
FDZ_URL = "https://www.rki.de/DE/Content/Forsch/FDZ/fdz_node.html"

TOBACCO_VARIABLES = {
    "RCstatE_k3": "Aktuell Raucher/-in (täglich oder gelegentlich), Anteil in %",
    "RCpass4B_k2": "Passivrauchbelastung (Nichtrauchende), Anteil in %",
}


def fetch(cache_dir: str = "data/", tobacco_only: bool = True, microdata: bool = False,
          refresh: bool = False) -> pd.DataFrame:
    """Return GEDA 2019/2020 aggregated results as a DataFrame.

    Columns: Altersgruppe, Bildungsgruppe, Gender, Frequency, Freq_ges, Percent,
    LowerCL, UpperCL, Bundesland, Standard (0 observed / 1 age-standardized),
    Variable, BundeslandId, Bundesland_Klassifikation.
    """
    cache = pathlib.Path(cache_dir) / _SOURCE_ID
    cache.mkdir(parents=True, exist_ok=True)
    if microdata:
        raise RuntimeError(
            "GEDA microdata require a data-use agreement with the RKI research data centre.\n"
            f"  1. Apply at {FDZ_URL}\n"
            "  2. Analyse via remote access / on site (no file transfer)\n"
            "  3. Aggregated open-data results are available without agreement: fetch('rki_geda')"
        )
    path = cache / "geda_2019_2020_ehis_open_data.csv"
    if refresh or not path.exists():
        resp = requests.get(_CSV_URL, timeout=120)
        resp.raise_for_status()
        path.write_bytes(resp.content)
    df = pd.read_csv(path, sep=None, engine="python")
    if tobacco_only:
        df = df[df["Variable"].isin(TOBACCO_VARIABLES)].copy()
        df["Variable_Label"] = df["Variable"].map(TOBACCO_VARIABLES)
    df["source_id"] = _SOURCE_ID
    return df.reset_index(drop=True)


if __name__ == "__main__":
    result = fetch()
    print(result.head(10).to_string())
    print(f"\n{len(result)} rows, {len(result.columns)} columns")

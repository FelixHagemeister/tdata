"""Fetch the RKI open-data indicator set on non-communicable diseases (GBE).

Data: 'Gesundheitsberichterstattung - Daten zu nichtübertragbaren Erkrankungen'
      (Robert Koch-Institut). One TSV with ~64,000 indicator rows, of which the
      tobacco-related indicators are extracted by ``extract.py``.
Access: free, CC BY 4.0, published on GitHub and Zenodo.
"""
from __future__ import annotations
import pathlib

import pandas as pd
import requests

_SOURCE_ID = "rki_gbe_ncd"
_FILE = "GBE_Indikatoren_nichtuebertragbarer_Erkrankungen.tsv"
_URL = ("https://raw.githubusercontent.com/robert-koch-institut/"
        "Gesundheitsberichterstattung_-_Daten_zu_nichtuebertragbaren_Erkrankungen/main/" + _FILE)
LANDING_URL = ("https://github.com/robert-koch-institut/"
               "Gesundheitsberichterstattung_-_Daten_zu_nichtuebertragbaren_Erkrankungen")

TOBACCO_INDICATOR_IDS = [1020501, 1020502, 2020306, 2020309, 2020310, 4010101]


def fetch(cache_dir: str = "data/", tobacco_only: bool = True,
          refresh: bool = False) -> pd.DataFrame:
    """Return the RKI GBE indicator table as a DataFrame.

    Downloads the ~20 MB TSV once into ``cache_dir`` and reuses it afterwards
    (pass ``refresh=True`` to re-download). With ``tobacco_only`` (default)
    only smoking, passive smoking, lung cancer and tobacco-control rows are
    returned.
    """
    cache = pathlib.Path(cache_dir) / _SOURCE_ID
    cache.mkdir(parents=True, exist_ok=True)
    path = cache / _FILE
    if refresh or not path.exists():
        resp = requests.get(_URL, timeout=120)
        resp.raise_for_status()
        path.write_bytes(resp.content)
    df = pd.read_csv(path, sep="\t", low_memory=False)
    if tobacco_only:
        df = df[df["Indikator_ID"].isin(TOBACCO_INDICATOR_IDS)].copy()
    return df.reset_index(drop=True)


if __name__ == "__main__":
    result = fetch()
    print(result.head(10).to_string())
    print(f"\n{len(result)} rows, {len(result.columns)} columns")

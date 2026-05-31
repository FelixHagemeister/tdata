"""Fetch RKI GEDA aggregate results from the Journal of Health Monitoring.

Two access tiers:
  1. Aggregate tables — freely available as PDF/HTML from RKI (no DUA).
     fetch() returns these aggregate statistics as a DataFrame.
  2. Microdata — requires RKI FDZ data-use agreement.
     Place downloaded .sav files in data/rki_geda/ and fetch() loads them.

FDZ application: https://www.rki.de/DE/Content/Forsch/FDZ/fdz_node.html
"""
from __future__ import annotations
import pathlib

import pandas as pd


_SOURCE_ID = "rki_geda"

# Journal of Health Monitoring — most recent GEDA smoking article
# RKI 2025: URL structure changed from /EN/Content/ to /DE/Aktuelles/Publikationen/
# Articles no longer embed HTML tables; scraping not possible from these URLs.
_FACT_SHEET_URLS = {
    "2025": (
        "https://www.rki.de/DE/Aktuelles/Publikationen/Journal-of-Health-Monitoring/"
        "GBEDownloadsJ/Focus/JHealthMonit_2025_01_Adipositas_Rauchen.html"
    ),
}

_FDZ_INSTRUCTIONS = """\
GEDA microdata requires a data-use agreement with the RKI FDZ.

Steps:
  1. Apply at: https://www.rki.de/DE/Content/Forsch/FDZ/fdz_node.html
  2. Download SPSS (.sav) files for desired wave(s)
  3. Place in: {cache_dir}/
     e.g. {cache_dir}/geda_2022_2023.sav
  4. Re-run fetch("rki_geda")

Aggregate fact sheets (no DUA) are available at:
  https://www.rki.de/EN/Content/Health_Monitoring/Journal_of_Health_Monitoring/Journal_node.html
"""


def fetch(cache_dir: str = "data/", tier: str = "auto") -> pd.DataFrame:
    """Return GEDA smoking data.

    tier="auto"  — load microdata if present, else fall back to aggregates
    tier="micro" — load microdata only (raise if not found)
    tier="agg"   — load aggregate fact-sheet tables only
    """
    cache = pathlib.Path(cache_dir) / _SOURCE_ID
    cache.mkdir(parents=True, exist_ok=True)

    sav_files = sorted(cache.glob("*.sav"))

    if tier in ("auto", "micro") and sav_files:
        return _load_microdata(sav_files)

    if tier == "micro" and not sav_files:
        raise FileNotFoundError(
            _FDZ_INSTRUCTIONS.format(cache_dir=cache)
        )

    # Aggregate tier
    return _fetch_aggregates(cache)


def _load_microdata(sav_files: list[pathlib.Path]) -> pd.DataFrame:
    import pyreadstat
    frames = []
    for f in sav_files:
        df, _meta = pyreadstat.read_sav(str(f), apply_value_formats=True)
        df["source_id"] = _SOURCE_ID
        df["geographic_level"] = "germany"
        df["wave_file"] = f.stem
        frames.append(df)
    return pd.concat(frames, ignore_index=True)


def _fetch_aggregates(cache: pathlib.Path) -> pd.DataFrame:
    import io
    import requests
    frames = []
    for year, url in _FACT_SHEET_URLS.items():
        try:
            resp = requests.get(url, timeout=30)
            resp.raise_for_status()
            tables = pd.read_html(io.StringIO(resp.text), decimal=",")
            if tables:
                df = max(tables, key=len)
                df["source_id"] = _SOURCE_ID
                df["geographic_level"] = "germany"
                df["wave_year"] = year
                frames.append(df)
        except Exception:
            continue
    if frames:
        return pd.concat(frames, ignore_index=True)

    # RKI articles no longer embed HTML tables — point to microdata and GBE portal
    raise RuntimeError(
        "GEDA aggregate tables cannot be scraped from the current RKI website.\n\n"
        "Options:\n"
        "  A. Microdata (DUA required):\n"
        + _FDZ_INSTRUCTIONS.format(cache_dir=cache)
        + "\n  B. GBE portal (interactive):\n"
        "     https://www.gbe.rki.de/DE/Themen/EinflussfaktorenAufDieGesundheit/"
        "GesundheitsUndRisikoverhalten/Tabakkonsum/Rauchen/rauchen_node.html\n"
        "\n  C. Latest article (2003–2023 trends):\n"
        + list(_FACT_SHEET_URLS.values())[-1]
    )


if __name__ == "__main__":
    result = fetch()
    print(result.head(5).to_string())
    print(f"\n{len(result)} rows")

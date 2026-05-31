"""Fetch Mikrozensus smoking tables from GENESIS Bayern (StaBa).

Data: aggregated smoking prevalence for Bavaria, 2009–2017.
Access: free account required at GENESIS Bayern — no anonymous API access.
"""
from __future__ import annotations
import pathlib

import pandas as pd


# GENESIS Bayern no longer allows anonymous (GUEST) API access.
# Table 12211 (Rauchgewohnheiten) must be exported manually via the web interface.
_GENESIS_URL = "https://www.statistikdaten.bayern.de/genesis/"
_SOURCE_ID = "staba_mikrozensus"


def fetch(cache_dir: str = "data/") -> pd.DataFrame:
    """Return Bavarian smoking prevalence table (Mikrozensus 2009–2017).

    Load from a locally cached CSV exported from GENESIS Bayern.
    """
    cache = pathlib.Path(cache_dir) / _SOURCE_ID
    cache.mkdir(parents=True, exist_ok=True)
    cached_file = cache / "rauchverhalten_bayern.csv"

    if cached_file.exists():
        return pd.read_csv(cached_file)

    raise RuntimeError(
        "GENESIS Bayern no longer allows anonymous downloads.\n\n"
        "Manual steps:\n"
        f"  1. Go to {_GENESIS_URL}\n"
        "  2. Log in (free account) and search for table '12211' (Rauchgewohnheiten)\n"
        "  3. Select Bayern, filter for smoking years (2009, 2013, 2017)\n"
        "  4. Export as CSV (semicolon-separated)\n"
        f"  5. Save to {cached_file}\n"
        "  6. Re-run fetch('staba_mikrozensus')"
    )


if __name__ == "__main__":
    result = fetch()
    print(result.head(10).to_string())
    print(f"\n{len(result)} rows, {len(result.columns)} columns")

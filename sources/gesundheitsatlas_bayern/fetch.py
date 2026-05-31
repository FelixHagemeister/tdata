"""Load Gesundheitsatlas Bayern smoking data from a manually exported Excel file.

Data: district-level smoking prevalence for all 96 Bavarian Landkreise,
      including Munich — the only free source at this geographic resolution.
Access: manual export from interactive web tool required.

Manual export steps:
  1. Go to https://www.gesundheitsatlas.bayern.de
  2. Select "Gesundheitsprofile" → "Sucht" → "Rauchen"
  3. Select indicator: "Raucherstatus — aktuell Rauchende"
  4. Click the Excel export button
  5. Save to  data/gesundheitsatlas_bayern/raucherstatus.xlsx
"""
from __future__ import annotations
import pathlib

import pandas as pd


_SOURCE_ID = "gesundheitsatlas_bayern"

_EXPORT_INSTRUCTIONS = """\
Gesundheitsatlas Bayern uses an interactive map tool with no bulk download API.

Manual export steps:
  1. Visit: https://www.gesundheitsatlas.bayern.de
  2. Navigate to: Gesundheitsprofile → Sucht → Rauchen
  3. Select indicator: "Raucherstatus — aktuell Rauchende"
  4. Click the Excel/CSV export button in the toolbar
  5. Save the file to:  {cache_file}
  6. Re-run fetch("gesundheitsatlas_bayern")
"""


def fetch(cache_dir: str = "data/") -> pd.DataFrame:
    """Return district-level smoking prevalence for Bavaria (all 96 Landkreise).

    Reads from data/gesundheitsatlas_bayern/raucherstatus.xlsx.
    Raises with download instructions if the file is not present.
    """
    cache = pathlib.Path(cache_dir) / _SOURCE_ID
    cache.mkdir(parents=True, exist_ok=True)

    # Accept both xlsx and csv exports
    for ext in ("raucherstatus.xlsx", "raucherstatus.csv", "export.xlsx", "export.csv"):
        candidate = cache / ext
        if candidate.exists():
            return _load(candidate)

    # Nothing found
    raise FileNotFoundError(
        _EXPORT_INSTRUCTIONS.format(cache_file=cache / "raucherstatus.xlsx")
    )


def _load(path: pathlib.Path) -> pd.DataFrame:
    if path.suffix == ".xlsx":
        # Skip metadata rows that GENESIS/Atlas exports often prepend
        df = pd.read_excel(path, skiprows=_detect_header_row(path))
    else:
        df = pd.read_csv(path, sep=None, engine="python", decimal=",")

    df = df.dropna(how="all")
    df["source_id"] = _SOURCE_ID
    df["geographic_level"] = "bavaria"

    # Standardize a location column if we can detect it
    for col in df.columns:
        if any(k in str(col).lower() for k in ("landkreis", "region", "gebiet", "name", "kreisname")):
            df = df.rename(columns={col: "location"})
            break

    return df


def _detect_header_row(path: pathlib.Path) -> int:
    """Skip LGL metadata preamble rows (usually 5–10 rows of title/source info)."""
    try:
        preview = pd.read_excel(path, header=None, nrows=20)
        for i, row in preview.iterrows():
            non_null = row.dropna()
            if len(non_null) >= 3:  # first row with at least 3 columns = header
                return i
    except Exception:
        pass
    return 0


if __name__ == "__main__":
    result = fetch()
    print(result.head(10).to_string())
    print(f"\n{len(result)} rows, {len(result.columns)} columns")

"""Load BZgA Drogenaffinitätsstudie microdata from GESIS cache.

Microdata: free GESIS Datenweitergabevertrag (no fee).
  1. Search https://search.gesis.org/ for "ZA3580" (or individual wave ZA IDs)
  2. Download .sav files after signing Datenweitergabevertrag
  3. Place in data/bzga_drogenaffinitaet/
  4. Run fetch("bzga_drogenaffinitaet")

PDF reports (no download needed): https://www.bzga.de/infomaterialien/
"""
from __future__ import annotations
import pathlib

import pandas as pd


_SOURCE_ID = "bzga_drogenaffinitaet"

_INSTRUCTIONS = """\
BZgA Drogenaffinitätsstudie microdata is archived at GESIS (series ZA3580).

Access (free, requires standard Datenweitergabevertrag — no fee):
  1. Go to https://search.gesis.org/ and search "BZgA Drogenaffinität"
     or directly for individual wave ZA numbers (e.g. ZA7655 for 2019)
  2. Sign the Datenweitergabevertrag online and submit a brief project description
  3. Download the .sav file for each desired wave
  4. Place files in: {cache_dir}/
  5. Re-run fetch("bzga_drogenaffinitaet")

For PDF reports only (no download needed):
  https://www.bzga.de/infomaterialien/alkohol-tabak-drogen/tabak/
"""


def fetch(cache_dir: str = "data/") -> pd.DataFrame:
    """Load BZgA Drogenaffinitätsstudie from GESIS-downloaded .sav files.

    Raises FileNotFoundError with instructions if no files are found.
    """
    cache = pathlib.Path(cache_dir) / _SOURCE_ID
    cache.mkdir(parents=True, exist_ok=True)

    sav_files = sorted(cache.glob("*.sav"))
    if not sav_files:
        raise FileNotFoundError(_INSTRUCTIONS.format(cache_dir=cache))

    import pyreadstat
    frames = []
    for f in sav_files:
        df, _meta = pyreadstat.read_sav(str(f), apply_value_formats=True)
        df["source_id"] = _SOURCE_ID
        df["geographic_level"] = "germany"
        df["gesis_file"] = f.stem
        frames.append(df)

    return pd.concat(frames, ignore_index=True)


if __name__ == "__main__":
    result = fetch()
    print(result.head(5).to_string())
    print(f"\n{len(result)} rows, {len(result.columns)} columns")

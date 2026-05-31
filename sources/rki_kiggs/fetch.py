"""Load RKI KiGGS microdata from cache.

Wave 1 PUF: free registration at RKI FDZ (no formal DUA).
  1. Register: https://www.rki.de/DE/Content/Forsch/FDZ/Datenzugang/Public_Use_File/
  2. Download KiGGS Wave 1 PUF (.sav)
  3. Place in data/rki_kiggs/
  4. Run fetch("rki_kiggs")

Full microdata (Baseline + Wave 2): formal FDZ agreement required.
"""
from __future__ import annotations
import pathlib

import pandas as pd


_SOURCE_ID = "rki_kiggs"

_INSTRUCTIONS = """\
KiGGS microdata must be downloaded from the RKI FDZ.

Wave 1 PUF (free, only registration needed):
  https://www.rki.de/DE/Content/Forsch/FDZ/Datenzugang/Public_Use_File/public_use_file_node.html

Full microdata (Baseline, Wave 2 — formal DUA):
  https://www.rki.de/DE/Content/Forsch/FDZ/fdz_node.html

After download, place .sav files in: {cache_dir}/
Then re-run fetch("rki_kiggs").
"""


def fetch(cache_dir: str = "data/") -> pd.DataFrame:
    """Load KiGGS SPSS files from cache.

    Raises FileNotFoundError with download instructions if no .sav files found.
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
        df["wave_file"] = f.stem
        frames.append(df)

    return pd.concat(frames, ignore_index=True)


if __name__ == "__main__":
    result = fetch()
    print(result.head(5).to_string())
    print(f"\n{len(result)} rows, {len(result.columns)} columns")

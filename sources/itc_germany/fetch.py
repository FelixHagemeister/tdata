"""Load ITC Germany Survey microdata from cache.

Requires formal data-use agreement with University of Waterloo.
  1. Submit request: https://itcproject.org/resources/data/
  2. Receive .sav files after approval (~2–6 weeks)
  3. Place in data/itc_germany/
  4. Run fetch("itc_germany")
"""
from __future__ import annotations
import pathlib

import pandas as pd


_SOURCE_ID = "itc_germany"

_INSTRUCTIONS = """\
ITC Germany Survey data requires a formal data-use agreement.

Steps:
  1. Submit a data request at: https://itcproject.org/resources/data/
     Include a brief description of your analysis plan.
  2. Contact for Germany data: Ute Mons (u.mons@dkfz-heidelberg.de)
  3. After approval (~2–6 weeks), download .sav files
  4. Place files in: {cache_dir}/
  5. Re-run fetch("itc_germany")
"""


def fetch(cache_dir: str = "data/") -> pd.DataFrame:
    """Load ITC Germany .sav files from cache.

    Raises FileNotFoundError with instructions if no files found.
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

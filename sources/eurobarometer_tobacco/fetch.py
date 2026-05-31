"""Load Eurobarometer tobacco survey microdata (EB 458 / EB 506) from GESIS.

Data: full microdata with e-cig, HTP, quit behavior for Germany.
Access: requires free GESIS account (no data-use agreement).
  1. Register: https://login.gesis.org
  2. Download ZA6925 (2017) and/or ZA7780 (2021) .sav files
  3. Place in data/eurobarometer_tobacco/
"""
from __future__ import annotations
import pathlib

import pandas as pd
import pyreadstat


_SOURCE_ID = "eurobarometer_tobacco"

# GESIS ZA numbers and their year labels
_WAVES = {
    "ZA6925": 2017,
    "ZA7780": 2021,
}

# Columns to keep — Germany filter + key tobacco variables
# Actual variable names depend on GESIS codebook; these are indicative.
_GERMANY_COUNTRY_CODE = 10  # Eurobarometer: isocntry=="DE" or countrycode==10

_DOWNLOAD_INSTRUCTIONS = """\
Eurobarometer tobacco microdata requires a free GESIS account.

  1. Register (no fee, no DUA): https://login.gesis.org
  2. Download ZA6925 (2017): https://doi.org/10.4232/1.13067
     → choose 'SPSS Portable' or 'SPSS System File' (.sav)
  3. Download ZA7780 (2021): https://doi.org/10.4232/1.13953
     → same format
  4. Place .sav files in:  {cache_dir}/
  5. Re-run fetch("eurobarometer_tobacco")
"""


def fetch(cache_dir: str = "data/", waves: list[str] | None = None) -> pd.DataFrame:
    """Return Germany-subset of Eurobarometer tobacco microdata.

    Loads all .sav files found in cache_dir/eurobarometer_tobacco/.
    Pass waves=['ZA6925'] to load only specific waves.
    """
    cache = pathlib.Path(cache_dir) / _SOURCE_ID
    cache.mkdir(parents=True, exist_ok=True)

    sav_files = sorted(cache.glob("*.sav"))
    if not sav_files:
        raise FileNotFoundError(
            _DOWNLOAD_INSTRUCTIONS.format(cache_dir=cache)
        )

    frames = []
    for sav_file in sav_files:
        if waves:
            za_id = _detect_za_id(sav_file)
            if za_id and za_id not in waves:
                continue
        df = _load_wave(sav_file)
        if df is not None:
            frames.append(df)

    if not frames:
        raise FileNotFoundError(
            f"No usable .sav files found in {cache}.\n\n"
            + _DOWNLOAD_INSTRUCTIONS.format(cache_dir=cache)
        )

    combined = pd.concat(frames, ignore_index=True)
    return combined


def _load_wave(sav_file: pathlib.Path) -> pd.DataFrame | None:
    try:
        df, meta = pyreadstat.read_sav(str(sav_file), apply_value_formats=True)
    except Exception as exc:
        print(f"Warning: could not read {sav_file.name}: {exc}")
        return None

    za_id = _detect_za_id(sav_file)
    year = _WAVES.get(za_id, None) if za_id else None

    # Filter to Germany
    germany_mask = _filter_germany(df)
    if germany_mask is None:
        print(f"Warning: could not identify Germany filter in {sav_file.name}. Keeping all rows.")
        df_de = df.copy()
    else:
        df_de = df[germany_mask].copy()

    df_de["source_id"] = _SOURCE_ID
    df_de["geographic_level"] = "germany"
    df_de["location"] = "Germany"
    df_de["gesis_za"] = za_id or sav_file.stem
    if year:
        df_de["survey_year"] = year

    return df_de


def _filter_germany(df: pd.DataFrame) -> pd.Series | None:
    # Try common Eurobarometer country variable names
    for col in ("isocntry", "ISOCNTRY", "country", "COUNTRY", "v7", "V7"):
        if col in df.columns:
            vals = df[col].astype(str).str.upper()
            mask = vals.isin({"DE", "DEW", "DEE", "GERMANY", "10", "10.0"})
            if mask.any():
                return mask
    return None


def _detect_za_id(path: pathlib.Path) -> str | None:
    name = path.stem.upper()
    for za in _WAVES:
        if za in name:
            return za
    return None


if __name__ == "__main__":
    result = fetch()
    print(result.head(5).to_string())
    print(f"\n{len(result)} rows, {len(result.columns)} columns")

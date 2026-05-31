"""Fetch Mikrozensus smoking tables from Destatis.

Data: aggregated smoking prevalence for Germany.
Access: free, no registration.

Primary: direct Excel download (full historical table).
Fallback: HTML scrape of the detail page.
"""
from __future__ import annotations
import io
import pathlib

import pandas as pd
import requests


# Direct Excel download — full Rauchgewohnheiten table
_EXCEL_URL = (
    "https://www.destatis.de/DE/Themen/Gesellschaft-Umwelt/Gesundheit/"
    "Gesundheitszustand-Relevantes-Verhalten/Publikationen/Downloads-Gesundheitszustand/"
    "rauchgewohnheiten-5239004179005.xlsx?__blob=publicationFile"
)
# HTML fallback
_HTML_URL = (
    "https://www.destatis.de/DE/Themen/Gesellschaft-Umwelt/Gesundheit/"
    "Gesundheitszustand-Relevantes-Verhalten/Tabellen/rauchverhalten-insgesamt.html"
)
_SOURCE_ID = "destatis_mikrozensus"


def fetch(cache_dir: str = "data/") -> pd.DataFrame:
    """Return smoking prevalence table from Destatis Mikrozensus.

    Downloads the official Destatis Excel publication on first call;
    subsequent calls read from the local CSV cache.
    """
    cache = pathlib.Path(cache_dir) / _SOURCE_ID
    cache.mkdir(parents=True, exist_ok=True)
    cached_file = cache / "rauchverhalten.csv"

    if cached_file.exists():
        return pd.read_csv(cached_file)

    df = _download_excel()
    if df is None:
        df = _download_html()
    df.to_csv(cached_file, index=False)
    return df


def _download_excel() -> pd.DataFrame | None:
    try:
        resp = requests.get(_EXCEL_URL, timeout=30)
        resp.raise_for_status()
        xf = pd.ExcelFile(io.BytesIO(resp.content))
        # Collect all "Tab N" data sheets
        data_sheets = [s for s in xf.sheet_names if str(s).startswith("Tab")]
        if not data_sheets:
            return None
        # Parse Tab 1 (smoker/non-smoker by age+sex) as the primary table
        df_raw = pd.read_excel(xf, sheet_name="Tab 1", header=None)
        return _parse_tab(df_raw)
    except Exception:
        return None


def _normalize_excel(df_raw: pd.DataFrame) -> pd.DataFrame:
    # The Excel has multiple data sheets (Tab 1..Tab 8); re-read all of them
    # We already have the raw bytes cached in the response — re-download is avoided
    # by the caller caching to CSV. Here we parse Tab 1 which is the main
    # smoker/non-smoker breakdown by age and sex for 2017.
    return _parse_tab(df_raw)


def _parse_tab(df: pd.DataFrame) -> pd.DataFrame:
    """Parse a Destatis Mikrozensus tab sheet into tidy format."""
    # Column layout (0-indexed after row 3):
    # 0: age group  1: pop_total  2: pop_with_data  3: response_rate
    # 4: smokers_total  5: smokers_occasional  6: smokers_regular
    # 7: smokers_heavy  8: nonsmokers_total  9: nonsmokers_former
    # 10: avg_age_start
    col_names = [
        "age_group", "pop_1000", "pop_with_data_1000", "response_rate_pct",
        "smokers_total_1000", "smokers_occasional_1000", "smokers_regular_1000",
        "smokers_heavy_1000", "nonsmokers_total_1000", "former_smokers_1000",
        "avg_smoking_start_age",
    ]

    rows = []
    current_sex = None

    for _, row in df.iterrows():
        val0 = str(row.iloc[0]).strip() if pd.notna(row.iloc[0]) else ""
        val1 = str(row.iloc[1]).strip() if pd.notna(row.iloc[1]) else ""

        # Sex section headers sit in column 1 when column 0 is NaN
        if val1 in ("Männlich", "Weiblich", "Insgesamt"):
            current_sex = val1
            continue

        # Data rows: column 0 is the age group string, column 1 is a number
        if current_sex and val0 and pd.notna(row.iloc[1]):
            try:
                float(str(row.iloc[1]).replace(",", "."))
            except ValueError:
                continue
            record = {"sex": current_sex, "year": 2017}
            for i, col in enumerate(col_names):
                raw = row.iloc[i] if i < len(row) else None
                record[col] = pd.to_numeric(
                    str(raw).replace(",", ".").replace("/", ""), errors="coerce"
                ) if i > 0 else str(raw).strip()
            rows.append(record)

    result = pd.DataFrame(rows)
    result["source_id"] = _SOURCE_ID
    result["geographic_level"] = "germany"
    result["location"] = "Deutschland"
    return result


def _download_html() -> pd.DataFrame:
    try:
        resp = requests.get(_HTML_URL, timeout=30)
        resp.raise_for_status()
        tables = pd.read_html(io.StringIO(resp.text), decimal=",", thousands=".")
    except Exception as exc:
        raise RuntimeError(
            f"Failed to download from Destatis.\n"
            f"Excel: {_EXCEL_URL}\n"
            f"HTML:  {_HTML_URL}\n"
            f"Error: {exc}"
        ) from exc

    if not tables:
        raise RuntimeError("No tables found on the Destatis page.")

    df = max(tables, key=len).copy()
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [" ".join(str(c) for c in col).strip() for col in df.columns]
    df = df.dropna(how="all")
    df["source_id"] = _SOURCE_ID
    df["geographic_level"] = "germany"
    df["location"] = "Deutschland"
    return df


if __name__ == "__main__":
    result = fetch()
    print(result.head(10).to_string())
    print(f"\n{len(result)} rows, {len(result.columns)} columns")

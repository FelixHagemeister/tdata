"""Download BZgA Rauchverhalten PDF reports.

PDF reports freely available from BZgA; no registration required.
Microdata: contact forschung@bzga.de (archival status at GESIS unconfirmed).
"""
from __future__ import annotations
import pathlib

import pandas as pd
import requests


_SOURCE_ID = "bzga_rauchverhalten"

# Known PDF report URLs — verify current links at https://www.bzga.de/infomaterialien/
_PDF_URLS = {
    2021: "https://www.bzga.de/fileadmin/user_upload/PDF/studien/Sucht_Rauchen_2021.pdf",
    2018: "https://www.bzga.de/fileadmin/user_upload/PDF/studien/Sucht_Rauchen_2018.pdf",
    2016: "https://www.bzga.de/fileadmin/user_upload/PDF/studien/Sucht_Rauchen_2016.pdf",
}
_REPORTS_PAGE = "https://www.bzga.de/infomaterialien/alkohol-tabak-drogen/tabak/"


def fetch(cache_dir: str = "data/", years: list[int] | None = None) -> pd.DataFrame:
    """Download BZgA smoking reports and return a metadata DataFrame.

    Returns a DataFrame with one row per downloaded PDF:
        source_id, year, pdf_path, url, status

    To extract tabular data, use pdfplumber on the returned pdf_path values.
    """
    cache = pathlib.Path(cache_dir) / _SOURCE_ID
    cache.mkdir(parents=True, exist_ok=True)

    target_years = years or list(_PDF_URLS.keys())
    rows = []

    for year in target_years:
        url = _PDF_URLS.get(year)
        if not url:
            continue
        pdf_path = cache / f"bzga_rauchverhalten_{year}.pdf"
        status = _download_if_missing(url, pdf_path)
        rows.append({
            "source_id": _SOURCE_ID,
            "geographic_level": "germany",
            "year": year,
            "pdf_path": str(pdf_path),
            "url": url,
            "status": status,
        })

    if not rows:
        raise RuntimeError(
            f"No reports downloaded.\n"
            f"Check current report URLs at: {_REPORTS_PAGE}"
        )

    return pd.DataFrame(rows)


def _download_if_missing(url: str, dest: pathlib.Path) -> str:
    if dest.exists():
        return "cached"
    try:
        resp = requests.get(url, timeout=60, stream=True)
        resp.raise_for_status()
        dest.write_bytes(resp.content)
        return "downloaded"
    except Exception as exc:
        return f"failed: {exc}"


if __name__ == "__main__":
    result = fetch()
    print(result.to_string())

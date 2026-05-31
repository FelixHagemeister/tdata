"""Download DEBRA study annual report PDFs.

Annual PDF reports freely available from debra-studie.de.
Microdata: contact info@debra-studie.de (case-by-case agreement).
"""
from __future__ import annotations
import pathlib

import pandas as pd
import requests


_SOURCE_ID = "debra"

# Known PDF URLs — verify current links at https://www.debra-studie.de/publikationen
_REPORT_URLS = {
    2023: "https://www.debra-studie.de/fileadmin/user_upload/debra/Jahresberichte/DEBRA_Jahresbericht_2023.pdf",
    2022: "https://www.debra-studie.de/fileadmin/user_upload/debra/Jahresberichte/DEBRA_Jahresbericht_2022.pdf",
    2021: "https://www.debra-studie.de/fileadmin/user_upload/debra/Jahresberichte/DEBRA_Jahresbericht_2021.pdf",
}
_PUBLICATIONS_PAGE = "https://www.debra-studie.de/publikationen"


def fetch(cache_dir: str = "data/", years: list[int] | None = None) -> pd.DataFrame:
    """Download DEBRA annual reports and return a metadata DataFrame.

    Returns a DataFrame with one row per downloaded PDF.
    Use pdfplumber on returned pdf_path values to extract tabular data.
    """
    cache = pathlib.Path(cache_dir) / _SOURCE_ID
    cache.mkdir(parents=True, exist_ok=True)

    target_years = years or list(_REPORT_URLS.keys())
    rows = []

    for year in target_years:
        url = _REPORT_URLS.get(year)
        if not url:
            continue
        pdf_path = cache / f"debra_jahresbericht_{year}.pdf"
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
            f"No DEBRA reports found.\n"
            f"Check publications at: {_PUBLICATIONS_PAGE}"
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

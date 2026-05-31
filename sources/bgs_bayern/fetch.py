"""Download BGS Bayern health report PDFs from LGL.

PDF reports freely available. Microdata requires LGL agreement.
Contact: gesundheitsberichterstattung@lgl.bayern.de
"""
from __future__ import annotations
import pathlib

import pandas as pd
import requests


_SOURCE_ID = "bgs_bayern"

# LGL published BGS reports — verify current URLs at:
# https://www.lgl.bayern.de/gesundheit/gesundheitsberichterstattung/gesundheitsberichte/
# 2021 Suchtmonitoring focuses on smoking; 2014 general health report also covers it.
# More at: https://www.lgl.bayern.de/publikationen/index.htm
_REPORT_URLS = {
    2021: "https://www.lgl.bayern.de/publikationen/gesundheit/doc/gesundheitsreport_01_2021.pdf",
    2014: "https://www.lgl.bayern.de/publikationen/doc/gesundheitsreport_2014_02.pdf",
}
_REPORTS_PAGE = "https://www.lgl.bayern.de/gesundheit/gesundheitsberichterstattung/gesundheitsberichte/"


def fetch(cache_dir: str = "data/", years: list[int] | None = None) -> pd.DataFrame:
    """Download BGS Bayern report PDFs and return a metadata DataFrame."""
    cache = pathlib.Path(cache_dir) / _SOURCE_ID
    cache.mkdir(parents=True, exist_ok=True)

    target_years = years or list(_REPORT_URLS.keys())
    rows = []

    for year in target_years:
        url = _REPORT_URLS.get(year)
        if not url:
            continue
        pdf_path = cache / f"bgs_bayern_{year}.pdf"
        status = _download_if_missing(url, pdf_path)
        rows.append({
            "source_id": _SOURCE_ID,
            "geographic_level": "bavaria",
            "location": "Bayern",
            "year": year,
            "pdf_path": str(pdf_path),
            "url": url,
            "status": status,
        })

    if not rows:
        raise RuntimeError(
            f"No BGS Bayern reports found.\nCheck: {_REPORTS_PAGE}"
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

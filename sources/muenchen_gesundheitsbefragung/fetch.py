"""Download Münchner Gesundheitsbefragung PDF reports.

PDF reports freely available from muenchen.de.
Microdata: contact gesundheitsreferat@muenchen.de (case-by-case).
"""
from __future__ import annotations
import pathlib

import pandas as pd
import requests


_SOURCE_ID = "muenchen_gesundheitsbefragung"

# More editions at: https://stadt.muenchen.de/infos/gesundheitsberichte.html
_REPORT_URLS = {
    2016: "https://stadt.muenchen.de/dam/jcr:f24696d1-9f11-4916-abc4-15a6ff7e8b48/mb160301.pdf",
}
_GBE_PAGE = "https://stadt.muenchen.de/infos/gesundheitsberichterstattung.html"


def fetch(cache_dir: str = "data/", years: list[int] | None = None) -> pd.DataFrame:
    """Download Münchner Gesundheitsbefragung PDFs and return a metadata DataFrame.

    Note: The PDF URLs above are placeholders — verify current links at the
    Munich Gesundheitsberichterstattung page before use.
    """
    cache = pathlib.Path(cache_dir) / _SOURCE_ID
    cache.mkdir(parents=True, exist_ok=True)

    target_years = years or list(_REPORT_URLS.keys())
    rows = []

    for year in target_years:
        url = _REPORT_URLS.get(year)
        if not url:
            continue
        pdf_path = cache / f"muenchner_gesundheitsbefragung_{year}.pdf"
        status = _download_if_missing(url, pdf_path)
        rows.append({
            "source_id": _SOURCE_ID,
            "geographic_level": "munich",
            "location": "München",
            "year": year,
            "pdf_path": str(pdf_path),
            "url": url,
            "status": status,
        })

    if not rows:
        raise RuntimeError(
            f"No reports configured.\nCheck current URLs at: {_GBE_PAGE}"
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

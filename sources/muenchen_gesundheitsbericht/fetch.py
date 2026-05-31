"""Download Münchner Gesundheitsbericht PDFs from Landeshauptstadt München.

All editions freely available from muenchen.de; no registration required.
"""
from __future__ import annotations
import pathlib

import pandas as pd
import requests


_SOURCE_ID = "muenchen_gesundheitsbericht"

# Verify current URLs at:
# https://www.muenchen.de/rathaus/stadtinfos/gesundheit/gesundheitsberichterstattung/gesundheitsberichte.html
# More editions at: https://stadt.muenchen.de/infos/gesundheitsberichte.html
_REPORT_URLS = {
    2015: "https://stadt.muenchen.de/dam/jcr:6bfb400e-740c-49b6-bad4-78fc90d4a823/gesundheitsbericht_2015_lang.pdf",
}
_REPORTS_PAGE = (
    "https://www.muenchen.de/rathaus/stadtinfos/gesundheit/"
    "gesundheitsberichterstattung/gesundheitsberichte.html"
)


def fetch(cache_dir: str = "data/", years: list[int] | None = None) -> pd.DataFrame:
    """Download Münchner Gesundheitsbericht PDFs and return a metadata DataFrame.

    Note: PDF URLs above are illustrative — verify current paths at the
    Munich Gesundheitsberichterstattung page.
    """
    cache = pathlib.Path(cache_dir) / _SOURCE_ID
    cache.mkdir(parents=True, exist_ok=True)

    target_years = years or list(_REPORT_URLS.keys())
    rows = []

    for year in target_years:
        url = _REPORT_URLS.get(year)
        if not url:
            continue
        pdf_path = cache / f"muenchen_gesundheitsbericht_{year}.pdf"
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
            f"No reports configured.\nCheck current URLs at: {_REPORTS_PAGE}"
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

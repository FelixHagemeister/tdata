"""Build the harmonized indicator dataset and the website data files.

Runs every ``sources/<id>/extract.py`` and loads every
``sources/<id>/curated.csv``, validates the combined table against
``tobacco_gateway.schema`` and writes:

  dataset/indicators.csv      canonical harmonized table (tracked in git)
  dataset/build_info.json     row counts per source and build timestamp
  docs/data/indicators.json   same rows for the website
  docs/data/catalog.json      indicator catalog + dimension labels
  docs/data/sources.json      SOURCE.md front-matter of all sources

Usage:  python scripts/build_dataset.py [--cache-dir data/] [--only source_id ...]
"""
from __future__ import annotations
import argparse
import datetime as dt
import importlib.util
import json
import pathlib
import re
import sys

import pandas as pd
import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from tobacco_gateway.schema import COLUMNS, INDICATORS, UNIT_LABELS, finalize, validate  # noqa: E402
from tobacco_gateway.curated import load_curated  # noqa: E402


def _load_extract(source_dir: pathlib.Path):
    spec = importlib.util.spec_from_file_location(f"_extract_{source_dir.name}", source_dir / "extract.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.extract


def _frontmatter(path: pathlib.Path) -> dict | None:
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    return yaml.safe_load(m.group(1)) if m else None


def build(cache_dir: str, only: list[str] | None = None) -> pd.DataFrame:
    frames: list[pd.DataFrame] = []
    info: dict[str, dict] = {}
    for source_dir in sorted((ROOT / "sources").iterdir()):
        if not source_dir.is_dir() or (only and source_dir.name not in only):
            continue
        parts = []
        if (source_dir / "extract.py").exists():
            print(f"[{source_dir.name}] extract.py ...", flush=True)
            parts.append(_load_extract(source_dir)(cache_dir=cache_dir))
        if (source_dir / "curated.csv").exists():
            print(f"[{source_dir.name}] curated.csv ...", flush=True)
            parts.append(load_curated(source_dir.name))
        if not parts:
            continue
        df = finalize(pd.concat(parts, ignore_index=True))
        problems = validate(df)
        if problems:
            raise SystemExit(f"[{source_dir.name}] schema problems: {problems}")
        info[source_dir.name] = {"rows": int(len(df)),
                                 "indicators": sorted(df["indicator_id"].unique()),
                                 "years": [int(df["year"].min()), int(df["year"].max())]}
        print(f"[{source_dir.name}] {len(df)} rows")
        frames.append(df)
    data = finalize(pd.concat(frames, ignore_index=True))
    problems = validate(data)
    if problems:
        raise SystemExit(f"combined dataset schema problems: {problems}")
    data = data.sort_values(["indicator_id", "geo_level", "geo_name", "year", "sex",
                             "age_group", "education", "group_type", "group",
                             "standardization", "source_id"]).reset_index(drop=True)
    _write(data, info)
    return data


def _write(data: pd.DataFrame, info: dict) -> None:
    (ROOT / "dataset").mkdir(exist_ok=True)
    (ROOT / "docs" / "data").mkdir(parents=True, exist_ok=True)
    data.to_csv(ROOT / "dataset" / "indicators.csv", index=False)

    build_info = {"built": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d"),
                  "rows": int(len(data)), "sources": info}
    (ROOT / "dataset" / "build_info.json").write_text(json.dumps(build_info, indent=2, ensure_ascii=False))

    # Columnar JSON with dictionary-encoded long strings keeps the website
    # payload small (rows are arrays; note/source_ref/source_url are indices).
    dict_cols = ["note", "source_ref", "source_url"]
    strings: dict[str, list[str]] = {}
    encoded = data.copy()
    for col in dict_cols:
        values = sorted(encoded[col].astype(str).unique())
        strings[col] = values
        lookup = {v: i for i, v in enumerate(values)}
        encoded[col] = encoded[col].astype(str).map(lookup)
    encoded = encoded.astype(object).where(encoded.notna(), None)
    payload = {"columns": COLUMNS, "strings": strings,
               "rows": encoded[COLUMNS].values.tolist(), "built": build_info["built"]}
    (ROOT / "docs" / "data" / "indicators.json").write_text(
        json.dumps(payload, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    data.to_csv(ROOT / "docs" / "data" / "indicators.csv", index=False)

    catalog = {
        "columns": COLUMNS,
        "indicators": INDICATORS,
        "units": UNIT_LABELS,
        "geo_levels": {"germany": "Deutschland", "state": "Bundesland", "region": "Region",
                       "city": "Stadt", "country": "Land (international)"},
        "dimensions": {"sex": "Geschlecht", "age_group": "Altersgruppe",
                       "education": "Bildung", "group": "Weitere Merkmale",
                       "geo_name": "Gebiet", "year": "Jahr", "source_id": "Quelle"},
        "built": build_info["built"],
    }
    (ROOT / "docs" / "data" / "catalog.json").write_text(json.dumps(catalog, ensure_ascii=False, indent=1), encoding="utf-8")

    sources = []
    for source_dir in sorted((ROOT / "sources").iterdir()):
        md = source_dir / "SOURCE.md"
        if md.exists():
            meta = _frontmatter(md)
            if meta:
                meta["in_dataset"] = source_dir.name in info
                meta["dataset_rows"] = info.get(source_dir.name, {}).get("rows", 0)
                sources.append(meta)
    (ROOT / "docs" / "data" / "sources.json").write_text(json.dumps(sources, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\nwrote {len(data)} rows to dataset/indicators.csv and docs/data/")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache-dir", default=str(ROOT / "data"))
    ap.add_argument("--only", nargs="*")
    args = ap.parse_args()
    build(args.cache_dir, args.only)

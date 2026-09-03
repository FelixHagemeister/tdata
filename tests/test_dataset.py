"""Schema and content checks for the harmonized dataset."""
import json
import pathlib

import pandas as pd
import pytest

from tobacco_gateway import indicators as I
from tobacco_gateway.schema import COLUMNS, INDICATORS, validate

ROOT = pathlib.Path(__file__).resolve().parent.parent


@pytest.fixture(scope="module")
def df():
    return I.load()


def test_dataset_exists_and_validates(df):
    assert list(df.columns) == COLUMNS
    assert validate(df) == []
    assert len(df) > 1000


def test_every_indicator_in_catalog(df):
    assert set(df["indicator_id"]) <= set(INDICATORS)


def test_geographic_cascade_present(df):
    geo = set(df["geo_name"])
    assert {"Deutschland", "Bayern", "München"} <= geo


def test_known_values(df):
    """Spot checks against the published sources."""
    bay17 = df[(df.source_id == "destatis_mikrozensus") & (df.geo_name == "Bayern") & (df.indicator_id == "smoking_current")
               & (df.sex == "gesamt") & (df.age_group == "gesamt")]
    assert len(bay17) == 1 and abs(bay17.value.iloc[0] - 20.5) < 0.1  # LGL cites 20.5 % for Bavaria 2017
    de19 = df[(df.source_id == "rki_gbe_ncd") & (df.geo_name == "Deutschland") & (df.indicator_id == "smoking_current")
              & (df.sex == "gesamt") & (df.age_group == "gesamt") & (df.education == "gesamt") & (df.standardization == "beobachtet") & (df.group_type == "")]
    assert len(de19) == 1 and de19.value.iloc[0] == pytest.approx(28.9)
    muc = df[(df.geo_name == "München") & (df.indicator_id == "smoking_daily")]
    assert muc.value.iloc[0] == 12


def test_website_files_match_dataset(df):
    payload = json.loads((ROOT / "docs" / "data" / "indicators.json").read_text(encoding="utf-8"))
    assert payload["columns"] == COLUMNS
    assert len(payload["rows"]) == len(df)
    catalog = json.loads((ROOT / "docs" / "data" / "catalog.json").read_text(encoding="utf-8"))
    assert set(catalog["indicators"]) == set(INDICATORS)
    sources = json.loads((ROOT / "docs" / "data" / "sources.json").read_text(encoding="utf-8"))
    assert {s["id"] for s in sources if s["in_dataset"]} == set(df["source_id"])


def test_curated_rows_cite_pages(df):
    cur = df[df.source_id.isin(["bgs_bayern", "muenchen_gesundheitsbefragung"])]
    assert cur["source_ref"].str.contains("S. ").all()
    assert cur["source_url"].str.startswith("https://").all()

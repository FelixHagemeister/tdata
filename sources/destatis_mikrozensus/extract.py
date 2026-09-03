"""Map the Destatis Mikrozensus 2017 'Rauchgewohnheiten' workbook into the
harmonized schema.

Tables used:
  Tab 1 – smokers / non-smokers by sex and age group (Germany)
  Tab 6 – predominant product among smokers by sex (Germany)
  Tab 7 – smokers / non-smokers by sex and Bundesland
All shares are computed on the population that answered the (voluntary)
smoking questions ("Bevölkerung mit Angaben über die Rauchgewohnheiten").
"""
from __future__ import annotations
import io
import pathlib
import sys

import pandas as pd
import requests

_ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(_ROOT))
from tobacco_gateway.schema import finalize  # noqa: E402
from tobacco_gateway.fetch import load_source_module  # noqa: E402

_fetch_mod = load_source_module("destatis_mikrozensus")
_EXCEL_URL = _fetch_mod._EXCEL_URL
_SOURCE_ID = _fetch_mod._SOURCE_ID

_PAGE_URL = ("https://www.destatis.de/DE/Themen/Gesellschaft-Umwelt/Gesundheit/"
             "Gesundheitszustand-Relevantes-Verhalten/Publikationen/_publikationen-innen-rauchgewohnheiten.html")
_SEX = {"Männlich": "männlich", "Weiblich": "weiblich", "Insgesamt": "gesamt"}
_STATES = {"Baden-Württemberg", "Bayern", "Berlin", "Brandenburg", "Bremen", "Hamburg",
           "Hessen", "Mecklenburg-Vorpommern", "Niedersachsen", "Nordrhein-Westfalen",
           "Rheinland-Pfalz", "Saarland", "Sachsen", "Sachsen-Anhalt",
           "Schleswig-Holstein", "Thüringen"}
_AGGREGATE_AGES = {"15 - 40", "40 - 65", "65 und mehr"}
_NOTE = "Mikrozensus 2017 (freiwillige Gesundheitsfragen); Bevölkerung ab 15 Jahren; Anteile bezogen auf Personen mit Angaben zum Rauchen"


def _workbook(cache_dir: str) -> pd.ExcelFile:
    cache = pathlib.Path(cache_dir) / _SOURCE_ID
    cache.mkdir(parents=True, exist_ok=True)
    path = cache / "rauchgewohnheiten_2017.xlsx"
    if not path.exists():
        resp = requests.get(_EXCEL_URL, timeout=60)
        resp.raise_for_status()
        path.write_bytes(resp.content)
    return pd.ExcelFile(io.BytesIO(path.read_bytes()))


def _num(v):
    if v is None or (isinstance(v, float) and pd.isna(v)):
        return float("nan")
    s = str(v).strip().replace(",", ".")
    if s in ("/", "-", "–", ".", "x", "..."):
        return float("nan")
    try:
        return float(s)
    except ValueError:
        return float("nan")


def _age(label: str) -> str:
    s = label.strip()
    if s in ("Zusammen", "Insgesamt"):
        return "gesamt"
    if s.endswith("und mehr"):
        return s.replace(" und mehr", "+")
    return s.replace(" - ", "–")


def _iter_rows(df: pd.DataFrame):
    """Yield (sex, first_cell, row) for data rows; sex headers sit in column 1."""
    sex = None
    for _, row in df.iterrows():
        c0 = row.iloc[0]
        c1 = row.iloc[1]
        c1s = str(c1).strip() if pd.notna(c1) else ""
        if (pd.isna(c0) or str(c0).strip() == "") and c1s in _SEX:
            sex = _SEX[c1s]
            continue
        if sex is None or pd.isna(c0):
            continue
        label = str(c0).strip()
        if not label or label[0].isdigit() and " " not in label and "-" not in label:
            # footnotes like "1 Bezogen auf ..." start with a digit followed by text
            pass
        if label.startswith(("1 ", "2 ", "3 ")) and len(label) > 12:
            continue
        if pd.isna(_num(c1)):
            continue
        yield sex, label, row


def _tab1(xf: pd.ExcelFile) -> list[dict]:
    df = pd.read_excel(xf, sheet_name="Tab 1", header=None)
    rows = []
    for sex, label, r in _iter_rows(df):
        if label in _AGGREGATE_AGES:
            continue
        base = _num(r.iloc[2])
        if not base:
            continue
        vals = {
            "smoking_current": _num(r.iloc[4]) / base * 100,
            "smoking_occasional": _num(r.iloc[5]) / base * 100,
            "smoking_daily": _num(r.iloc[6]) / base * 100,
            "smoking_heavy": _num(r.iloc[7]) / base * 100,
            "smoking_former": _num(r.iloc[9]) / base * 100,
            "smoking_never": (_num(r.iloc[8]) - _num(r.iloc[9])) / base * 100,
            "smoking_start_age": _num(r.iloc[10]),
        }
        for ind, v in vals.items():
            if pd.isna(v):
                continue
            rows.append(dict(indicator_id=ind, geo_level="germany", geo_name="Deutschland",
                             year=2017, sex=sex, age_group=_age(label),
                             value=round(v, 2),
                             unit="years" if ind == "smoking_start_age" else "percent",
                             n=base * 1000, source_ref="Tab 1 (Raucher und Nichtraucher nach Geschlecht und Altersgruppen)"))
    return rows


def _tab7(xf: pd.ExcelFile) -> list[dict]:
    df = pd.read_excel(xf, sheet_name="Tab 7", header=None)
    rows = []
    for sex, label, r in _iter_rows(df):
        if label != "Deutschland" and label not in _STATES:
            continue
        base = _num(r.iloc[2])
        if not base:
            continue
        vals = {
            "smoking_current": _num(r.iloc[3]) / base * 100,
            "smoking_occasional": _num(r.iloc[4]),
            "smoking_daily": _num(r.iloc[5]),
            "smoking_heavy": _num(r.iloc[6]),
            "smoking_former": _num(r.iloc[8]),
            "smoking_start_age": _num(r.iloc[9]),
        }
        for ind, v in vals.items():
            if pd.isna(v):
                continue
            rows.append(dict(indicator_id=ind,
                             geo_level="germany" if label == "Deutschland" else "state",
                             geo_name=label, year=2017, sex=sex, age_group="gesamt",
                             value=round(v, 2),
                             unit="years" if ind == "smoking_start_age" else "percent",
                             n=base * 1000, source_ref="Tab 7 (Raucher und Nichtraucher nach Geschlecht und Ländern)"))
    return rows


def _tab6(xf: pd.ExcelFile) -> list[dict]:
    df = pd.read_excel(xf, sheet_name="Tab 6", header=None)
    products = {3: "Zigaretten", 4: "Zigarren/Zigarillos", 5: "Pfeifentabak", 6: "Shisha (Wasserpfeife)"}
    rows = []
    for sex, label, r in _iter_rows(df):
        if label not in ("Zusammen", "Insgesamt"):
            continue
        base = _num(r.iloc[2])
        if not base:
            continue
        for col, name in products.items():
            v = _num(r.iloc[col])
            if pd.isna(v):
                continue
            rows.append(dict(indicator_id="smoking_product_share", geo_level="germany",
                             geo_name="Deutschland", year=2017, sex=sex, age_group="gesamt",
                             group_type="Rauchart", group=name, value=round(v / base * 100, 2),
                             unit="percent", n=base * 1000,
                             source_ref="Tab 6 (Raucher, überwiegende Rauchart nach Geschlecht und Altersgruppen)"))
    return rows


def extract(cache_dir: str = "data/") -> pd.DataFrame:
    xf = _workbook(cache_dir)
    rows = _tab1(xf) + _tab7(xf) + _tab6(xf)
    # Tab 1 and Tab 7 both contain the Germany total; keep the Tab 1 version.
    df = pd.DataFrame(rows)
    dup_mask = (df["source_ref"].str.startswith("Tab 7") & (df["geo_name"] == "Deutschland"))
    df = df[~dup_mask].copy()
    df["source_id"] = _SOURCE_ID
    df["source_url"] = _EXCEL_URL
    df["note"] = _NOTE
    df["period"] = "2017"
    return finalize(df)


if __name__ == "__main__":
    out = extract()
    print(out.groupby(["indicator_id", "geo_level"]).size())
    print(out[(out.geo_name == "Bayern")].to_string())

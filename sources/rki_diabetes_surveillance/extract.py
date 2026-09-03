"""Map RKI Diabetes-Surveillance smoking rows into the harmonized schema.

Adult rows for 2019 are omitted here because the identical GEDA 2019/2020
values are already provided by ``rki_gbe_ncd``.
"""
from __future__ import annotations
import pathlib
import sys

import pandas as pd

_ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(_ROOT))
from tobacco_gateway.schema import finalize  # noqa: E402
from tobacco_gateway.fetch import load_source_module  # noqa: E402

_fetch_mod = load_source_module("rki_diabetes_surveillance")
fetch = _fetch_mod.fetch
LANDING_URL = _fetch_mod.LANDING_URL

_SOURCE_ID = "rki_diabetes_surveillance"
_STATES = {"Baden-Württemberg", "Bayern", "Berlin", "Brandenburg", "Bremen", "Hamburg",
           "Hessen", "Mecklenburg-Vorpommern", "Niedersachsen", "Nordrhein-Westfalen",
           "Rheinland-Pfalz", "Saarland", "Sachsen", "Sachsen-Anhalt",
           "Schleswig-Holstein", "Thüringen"}
_SEX = {"Gesamt": "gesamt", "Männlich": "männlich", "Weiblich": "weiblich"}
_EDU = {"Gesamt": "gesamt", "untere": "niedrig", "mittlere": "mittel", "obere": "hoch"}
_SURVEY = {2003: "GSTel03 (Telefonsurvey 2003)", 2009: "GEDA 2009", 2010: "GEDA 2010",
           2012: "GEDA 2012", 2019: "GEDA 2019/2020-EHIS"}
_KIGGS = {2004: "2003–2006", 2010: "2009–2012", 2015: "2014–2017"}


def _age(label) -> str:
    s = str(label)
    if s in ("Gesamt", "nan"):
        return "gesamt"
    s = s.replace(" Jahre", "").strip()
    if s.startswith("≥") or s.startswith(">="):
        return s.lstrip("≥>=") + "+"
    return s.replace("-", "–")


def extract(cache_dir: str = "data/") -> pd.DataFrame:
    raw = fetch(cache_dir=cache_dir)
    raw = raw[raw["Indikator_Name"] == "Rauchen"]
    rows = []
    for _, r in raw.iterrows():
        if pd.isna(r["Wert"]):
            continue
        year = int(r["Jahr"])
        phase = str(r["Lebensphase_Name"])
        if phase.startswith("Erwachsene"):
            if year == 2019:
                continue  # covered by rki_gbe_ncd (same GEDA 2019/2020 values)
            ind = "smoking_current"
            period = str(year)
            note = f"{_SURVEY.get(year, 'GEDA')}; Erwachsene ab 18 Jahren; Telefonsurveys bis 2012 nur eingeschränkt mit GEDA 2019/2020 vergleichbar"
        elif phase.startswith("Kinder"):
            ind = "youth_smoking_current"
            period = _KIGGS.get(year, str(year))
            note = f"KiGGS-Welle {period}; 11- bis 17-Jährige"
        else:
            continue
        geo_name = str(r["Region_Name"])
        geo_level = "germany" if geo_name == "Deutschland" else ("state" if geo_name in _STATES else "region")
        rows.append({
            "indicator_id": ind,
            "geo_level": geo_level,
            "geo_name": geo_name,
            "year": year,
            "period": period,
            "sex": _SEX.get(str(r["Geschlecht_Name"]), "gesamt"),
            "age_group": _age(r["Alter_Name"]),
            "education": _EDU.get(str(r["Bildung_Casmin_Name"]), "gesamt"),
            "standardization": "altersstandardisiert" if str(r["Standardisierung_Name"]).startswith("alters") else "beobachtet",
            "value": float(r["Wert"]),
            "unit": "percent",
            "ci_lower": r.get("Unteres_Konfidenzintervall"),
            "ci_upper": r.get("Oberes_Konfidenzintervall"),
            "n": r.get("Stichprobe") if "Stichprobe" in r else None,
            "source_id": _SOURCE_ID,
            "source_ref": f"Indikator {r['Indikator_ID']} – Rauchen ({phase}), Datenstand {r['Datenstand']}",
            "source_url": LANDING_URL,
            "note": note,
        })
    return finalize(pd.DataFrame(rows))


if __name__ == "__main__":
    out = extract()
    print(out.groupby(["indicator_id", "geo_level", "year"]).size())
    print(f"{len(out)} rows")

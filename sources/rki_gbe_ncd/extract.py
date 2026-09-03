"""Map RKI GBE NCD indicator rows into the harmonized schema."""
from __future__ import annotations
import pathlib
import sys

import pandas as pd

_ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(_ROOT))
from tobacco_gateway.schema import finalize  # noqa: E402
from tobacco_gateway.fetch import load_source_module  # noqa: E402

_fetch_mod = load_source_module("rki_gbe_ncd")
fetch = _fetch_mod.fetch
LANDING_URL = _fetch_mod.LANDING_URL
_URL = _fetch_mod._URL

_SOURCE_ID = "rki_gbe_ncd"
_STATES = {"Baden-Württemberg", "Bayern", "Berlin", "Brandenburg", "Bremen", "Hamburg",
           "Hessen", "Mecklenburg-Vorpommern", "Niedersachsen", "Nordrhein-Westfalen",
           "Rheinland-Pfalz", "Saarland", "Sachsen", "Sachsen-Anhalt",
           "Schleswig-Holstein", "Thüringen"}
_RKI_REGIONS = {"Nordost", "Nordwest", "Mitte-Ost", "Mitte-West", "Süden"}
_SEX = {"Gesamt": "gesamt", "Männlich": "männlich", "Weiblich": "weiblich"}
_EDU = {"Gesamt": "gesamt", "niedrig": "niedrig", "mittel": "mittel", "hoch": "hoch"}
_STD = {"beobachtet": "beobachtet", "altersstandardisiert": "altersstandardisiert"}

_INDICATORS = {
    1020501: ("smoking_current", "percent", "GEDA 2019/2020-EHIS; Erwachsene ab 18 Jahren"),
    1020502: ("passive_smoking", "percent", "GEDA 2019/2020-EHIS; Nichtrauchende ab 18 Jahren"),
    2020306: ("lung_cancer_incidence", "per_100000", "Zentrum für Krebsregisterdaten; Europastandardbevölkerung"),
    2020309: ("lung_cancer_mortality", "per_100000", "Todesursachenstatistik; Europastandardbevölkerung"),
    4010101: ("tobacco_control_score", "points", "Tobacco Control Scale 2021"),
}


def _geo(name: str) -> str:
    if name == "Deutschland":
        return "germany"
    if name in _STATES:
        return "state"
    if name in _RKI_REGIONS:
        return "region"
    return "country"


def _age(label) -> str:
    s = str(label)
    if s in ("Alle Altersgruppen", "nan", "Gesamt"):
        return "gesamt"
    s = s.replace(" Jahre", "").strip()
    if s.startswith(">="):
        return s[2:] + "+"
    if s.startswith("<="):
        return "0–" + s[2:]
    return s.replace("-", "–")


def extract(cache_dir: str = "data/") -> pd.DataFrame:
    raw = fetch(cache_dir=cache_dir)
    rows = []
    for _, r in raw.iterrows():
        if r["Indikator_ID"] not in _INDICATORS or pd.isna(r["Wert"]):
            continue
        ind, unit, base_note = _INDICATORS[r["Indikator_ID"]]
        geo_name = str(r["Region_Name"])
        geo_level = _geo(geo_name)
        group_type, group = "", ""
        if ind == "tobacco_control_score":
            if r["Kennzahl_ID"] != 0:
                group_type, group = "Teilbereich", str(r["Kennzahl_Name"])
        gisd = r.get("GISD_Name")
        if pd.notna(gisd) and str(gisd) != "Gesamt":
            group_type, group = "Regionale sozioökonomische Deprivation (GISD)", str(gisd)
        quali = r.get("Berufliche_Qualifikation_Name")
        if pd.notna(quali) and str(quali) != "Gesamt":
            group_type, group = "Berufliche Qualifikation", str(quali)
        note = base_note
        if pd.notna(r.get("Anmerkung")) and str(r.get("Anmerkung")).strip():
            note += "; " + str(r["Anmerkung"]).strip()
        unc = r.get("Unsicherheit")
        if pd.notna(unc) and float(unc) >= 1:
            note += "; RKI-Hinweis: statistisch unsichere Schätzung"
        year = int(str(r["Zeitraum_Name"])[:4])
        period = str(r["Zeitraum_Name"])
        if ind in ("smoking_current", "passive_smoking") and year == 2019:
            period = "2019/2020"
        rows.append({
            "indicator_id": ind,
            "geo_level": geo_level,
            "geo_name": geo_name,
            "year": year,
            "period": period,
            "sex": _SEX.get(str(r["Geschlecht_Name"]), "gesamt"),
            "age_group": _age(r["Alter_Name"]),
            "education": _EDU.get(str(r["Bildung_Casmin_Name"]), "gesamt"),
            "group_type": group_type,
            "group": group,
            "standardization": _STD.get(str(r["Standardisierung_Name"]), "beobachtet"),
            "value": float(r["Wert"]),
            "unit": unit,
            "ci_lower": r.get("Unteres_Konfidenzintervall"),
            "ci_upper": r.get("Oberes_Konfidenzintervall"),
            "n": r.get("Stichprobe") if pd.notna(r.get("Stichprobe")) else r.get("Fälle"),
            "source_id": _SOURCE_ID,
            "source_ref": f"Indikator {r['Indikator_ID']} – {r['Indikator_Name']} ({r['Kennzahl_Name']}), Datenstand {r['Datenstand']}",
            "source_url": LANDING_URL,
            "note": note,
        })
    df = pd.DataFrame(rows)
    # Lung cancer: the RKI reports both observed and standardized totals in some
    # combinations; the harmonized set keeps the age-standardized value only,
    # except for single age groups where only observed rates exist.
    return finalize(df)


if __name__ == "__main__":
    out = extract()
    print(out.groupby(["indicator_id", "geo_level"]).size())
    print(f"{len(out)} rows")

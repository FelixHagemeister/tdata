"""Harmonized indicator schema shared by extractors, the build script, the
Python API and the website.

Every extractor returns a DataFrame with exactly the columns in ``COLUMNS``.
``INDICATORS`` is the catalog of indicator ids with German labels; the build
script exports it to ``docs/data/catalog.json`` so the website and the Python
package use the same definitions.
"""
from __future__ import annotations

import pandas as pd

COLUMNS = [
    "indicator_id",     # key into INDICATORS
    "geo_level",        # germany | state | region | city | country
    "geo_name",         # Deutschland, Bayern, München, Oberpfalz, ...
    "year",             # int, reference year (first year of a period)
    "period",           # as published, e.g. "2019/2020"
    "sex",              # gesamt | männlich | weiblich
    "age_group",        # gesamt | "18–29" | "65+" | ...
    "education",        # gesamt | niedrig | mittel | hoch
    "group_type",       # optional extra dimension name (e.g. Familienstand), else ""
    "group",            # value of the extra dimension, else ""
    "standardization",  # beobachtet | altersstandardisiert
    "value",            # float
    "unit",             # percent | per_100000 | years | points
    "ci_lower",         # float or NaN
    "ci_upper",         # float or NaN
    "n",                # sample size / population base, or NaN
    "source_id",        # folder name under sources/
    "source_ref",       # table / page / indicator reference inside the source
    "source_url",       # direct link to the file or page the value came from
    "note",             # free text caveat
]

GEO_LEVELS = ["germany", "state", "region", "city", "country"]
SEX_VALUES = ["gesamt", "männlich", "weiblich"]
EDU_VALUES = ["gesamt", "niedrig", "mittel", "hoch"]
STD_VALUES = ["beobachtet", "altersstandardisiert"]
UNITS = ["percent", "per_100000", "years", "points"]

# Indicator catalog. ``population`` is a short German description of the
# denominator; ``keywords`` are used by the deterministic question engine.
INDICATORS: dict[str, dict] = {
    "smoking_current": {
        "label": "Rauchen (täglich oder gelegentlich)",
        "short": "Raucheranteil",
        "population": "Anteil der Befragten, die aktuell rauchen",
        "unit": "percent",
        "keywords": ["rauch", "raucher", "raucherquote", "raucheranteil", "tabak", "smok"],
    },
    "smoking_daily": {
        "label": "Tägliches Rauchen",
        "short": "täglich",
        "population": "Anteil der Befragten, die täglich (regelmäßig) rauchen",
        "unit": "percent",
        "keywords": ["täglich", "taeglich", "regelmäßig", "regelmaessig", "daily"],
    },
    "smoking_occasional": {
        "label": "Gelegentliches Rauchen",
        "short": "gelegentlich",
        "population": "Anteil der Befragten, die gelegentlich rauchen",
        "unit": "percent",
        "keywords": ["gelegentlich", "occasional"],
    },
    "smoking_heavy": {
        "label": "Starkes Rauchen (mehr als 20 Zigaretten pro Tag)",
        "short": "stark",
        "population": "Anteil der Befragten, die mehr als 20 Zigaretten pro Tag rauchen",
        "unit": "percent",
        "keywords": ["stark", "starke raucher", "kettenraucher", "heavy"],
    },
    "smoking_former": {
        "label": "Ehemaliges Rauchen",
        "short": "ehemalig",
        "population": "Anteil der Befragten, die früher geraucht haben und aufgehört haben",
        "unit": "percent",
        "keywords": ["ehemalig", "ehemalige", "früher", "aufgehört", "aufgehoert", "ex-raucher", "exraucher", "former", "quit"],
    },
    "smoking_never": {
        "label": "Nie geraucht",
        "short": "nie",
        "population": "Anteil der Befragten, die nie geraucht haben",
        "unit": "percent",
        "keywords": ["nie geraucht", "nieraucher", "nichtraucher", "never"],
    },
    "smoking_start_age": {
        "label": "Durchschnittliches Alter bei Rauchbeginn",
        "short": "Rauchbeginn",
        "population": "Mittleres Alter, in dem Raucherinnen und Raucher begonnen haben",
        "unit": "years",
        "keywords": ["rauchbeginn", "einstiegsalter", "anfangen", "begonnen", "start"],
    },
    "smoking_product_share": {
        "label": "Rauchart (Anteil an allen Rauchenden)",
        "short": "Rauchart",
        "population": "Anteil der Rauchenden, die überwiegend das jeweilige Produkt rauchen",
        "unit": "percent",
        "keywords": ["rauchart", "zigarre", "zigarillo", "pfeife", "shisha", "wasserpfeife", "produkt"],
    },
    "passive_smoking": {
        "label": "Passivrauchbelastung",
        "short": "Passivrauchen",
        "population": "Anteil der Nichtrauchenden, die mindestens täglich Tabakrauch ausgesetzt sind",
        "unit": "percent",
        "keywords": ["passiv", "passivrauch", "secondhand"],
    },
    "youth_smoking_current": {
        "label": "Rauchen bei Kindern und Jugendlichen (11–17 Jahre)",
        "short": "Jugendliche",
        "population": "Anteil der 11- bis 17-Jährigen, die aktuell rauchen",
        "unit": "percent",
        "keywords": ["jugend", "jugendliche", "kinder", "youth", "teen"],
    },
    "youth_smoking_30d": {
        "label": "Rauchen in den letzten 30 Tagen (Schülerinnen und Schüler, 9./10. Klasse)",
        "short": "Schüler 30 Tage",
        "population": "Anteil der Schülerinnen und Schüler der 9. und 10. Jahrgangsstufe, die in den letzten 30 Tagen geraucht haben",
        "unit": "percent",
        "keywords": ["schüler", "schueler", "30 tage", "espad", "schule"],
    },
    "youth_smoking_ever": {
        "label": "Jemals geraucht (Schülerinnen und Schüler, 9./10. Klasse)",
        "short": "Schüler jemals",
        "population": "Anteil der Schülerinnen und Schüler der 9. und 10. Jahrgangsstufe, die jemals geraucht haben",
        "unit": "percent",
        "keywords": ["jemals", "lebenszeit", "ever"],
    },
    "ecig_current": {
        "label": "Aktuelle Nutzung von E-Zigaretten",
        "short": "E-Zigarette",
        "population": "Anteil der Befragten, die aktuell E-Zigaretten nutzen",
        "unit": "percent",
        "keywords": ["e-zigarette", "ezigarette", "e-zigaretten", "vape", "vapen", "dampfen", "liquid"],
    },
    "htp_current": {
        "label": "Aktuelle Nutzung von Tabakerhitzern",
        "short": "Tabakerhitzer",
        "population": "Anteil der Befragten, die aktuell Tabakerhitzer nutzen",
        "unit": "percent",
        "keywords": ["tabakerhitzer", "iqos", "heated", "erhitzer"],
    },
    "lung_cancer_incidence": {
        "label": "Lungenkrebs: Neuerkrankungen je 100.000 Einwohner (altersstandardisiert)",
        "short": "Lungenkrebs-Inzidenz",
        "population": "Altersstandardisierte Neuerkrankungsrate je 100.000 Einwohner (Europastandard)",
        "unit": "per_100000",
        "keywords": ["lungenkrebs", "inzidenz", "neuerkrankung", "krebs", "cancer"],
    },
    "lung_cancer_mortality": {
        "label": "Lungenkrebs: Sterbefälle je 100.000 Einwohner (altersstandardisiert)",
        "short": "Lungenkrebs-Sterblichkeit",
        "population": "Altersstandardisierte Sterberate je 100.000 Einwohner (Europastandard)",
        "unit": "per_100000",
        "keywords": ["sterblichkeit", "sterbefälle", "sterbefaelle", "mortalität", "mortalitaet", "tod", "todesfälle", "gestorben", "mortality"],
    },
    "tobacco_control_score": {
        "label": "Tabakkontrollskala (Punkte von 100)",
        "short": "Tabakkontrolle",
        "population": "Bewertung der Tabakkontrollpolitik eines Landes (Tobacco Control Scale)",
        "unit": "points",
        "keywords": ["tabakkontrolle", "tabakpolitik", "kontrollskala", "tobacco control", "politik", "werbeverbot"],
    },
}

UNIT_LABELS = {
    "percent": "%",
    "per_100000": "je 100.000",
    "years": "Jahre",
    "points": "Punkte",
}


def empty_frame() -> pd.DataFrame:
    return pd.DataFrame({c: pd.Series(dtype="object") for c in COLUMNS})


def validate(df: pd.DataFrame, strict: bool = True) -> list[str]:
    """Return a list of schema problems (empty list means valid)."""
    problems: list[str] = []
    missing = [c for c in COLUMNS if c not in df.columns]
    extra = [c for c in df.columns if c not in COLUMNS]
    if missing:
        problems.append(f"missing columns: {missing}")
    if extra:
        problems.append(f"unexpected columns: {extra}")
    if problems:
        return problems

    bad_ind = sorted(set(df["indicator_id"]) - set(INDICATORS))
    if bad_ind:
        problems.append(f"unknown indicator_id: {bad_ind}")
    for col, allowed in [("geo_level", GEO_LEVELS), ("sex", SEX_VALUES),
                         ("education", EDU_VALUES), ("standardization", STD_VALUES),
                         ("unit", UNITS)]:
        bad = sorted(set(df[col].astype(str)) - set(allowed))
        if bad:
            problems.append(f"{col}: invalid values {bad}")
    if df["value"].isna().any():
        problems.append(f"{int(df['value'].isna().sum())} rows without value")
    if not pd.api.types.is_numeric_dtype(df["year"]):
        problems.append("year must be numeric")
    pct = df[df["unit"] == "percent"]
    if ((pct["value"] < 0) | (pct["value"] > 100)).any():
        problems.append("percent values outside 0–100")
    key = ["indicator_id", "geo_level", "geo_name", "year", "sex", "age_group",
           "education", "group_type", "group", "standardization", "source_id"]
    dups = df.duplicated(subset=key, keep=False)
    if dups.any():
        problems.append(f"{int(dups.sum())} duplicate rows on key {key}")
    if strict:
        for col in ["indicator_id", "geo_name", "source_id", "source_ref"]:
            if (df[col].astype(str).str.strip() == "").any():
                problems.append(f"empty values in {col}")
    return problems


def finalize(df: pd.DataFrame) -> pd.DataFrame:
    """Fill optional columns with defaults, coerce types, order columns."""
    df = df.copy()
    defaults = {"period": "", "sex": "gesamt", "age_group": "gesamt",
                "education": "gesamt", "group_type": "", "group": "",
                "standardization": "beobachtet", "ci_lower": float("nan"),
                "ci_upper": float("nan"), "n": float("nan"), "note": "",
                "source_url": ""}
    for col, default in defaults.items():
        if col not in df.columns:
            df[col] = default
        else:
            df[col] = df[col].where(df[col].notna(), default)
    df["period"] = df["period"].astype(str)
    df.loc[df["period"].isin(["", "nan"]), "period"] = df["year"].astype(int).astype(str)
    df["year"] = df["year"].astype(int)
    for col in ["value", "ci_lower", "ci_upper", "n"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    for col in ["group_type", "group", "note", "source_url", "source_ref"]:
        df[col] = df[col].astype(str).replace("nan", "")
    return df[COLUMNS].reset_index(drop=True)

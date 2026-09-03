"""Access to the harmonized indicator dataset and a deterministic
question-answering helper.

    from tobacco_gateway import indicators
    df = indicators.load()
    sub = indicators.select(df, indicator="smoking_current", geo="Bayern", breakdown="sex")
    ans = indicators.answer("Wie viele Menschen rauchen in Bayern?")
    print(ans.text); ans.data

The website (``docs/app.js``) implements the same rules in JavaScript so
that both give the same answer for the same question.
"""
from __future__ import annotations

import pathlib
import re
from dataclasses import dataclass, field

import pandas as pd

from .schema import INDICATORS, UNIT_LABELS

_ROOT = pathlib.Path(__file__).parent.parent
DATASET = _ROOT / "dataset" / "indicators.csv"

STATES = ["Baden-Württemberg", "Bayern", "Berlin", "Brandenburg", "Bremen", "Hamburg",
          "Hessen", "Mecklenburg-Vorpommern", "Niedersachsen", "Nordrhein-Westfalen",
          "Rheinland-Pfalz", "Saarland", "Sachsen", "Sachsen-Anhalt",
          "Schleswig-Holstein", "Thüringen"]
REGIONS = ["Oberbayern", "Niederbayern", "Oberpfalz", "Oberfranken", "Mittelfranken",
           "Unterfranken", "Schwaben"]
GEO_ALIASES = {
    "münchen": "München", "muenchen": "München", "munich": "München",
    "bayern": "Bayern", "bavaria": "Bayern", "bayerisch": "Bayern", "bayerische": "Bayern",
    "deutschland": "Deutschland", "bund": "Deutschland", "bundesweit": "Deutschland",
    "germany": "Deutschland", "deutsch": "Deutschland", "deutschen": "Deutschland",
}
BREAKDOWN_KEYWORDS = {
    "sex": ["geschlecht", "männer", "maenner", "frauen", "männlich", "weiblich", "mann", "frau", "sex", "gender"],
    "age_group": ["alter", "altersgruppe", "altersgruppen", "jung", "alt", "jährige", "jaehrige", "age"],
    "education": ["bildung", "bildungsgruppe", "bildungsstand", "abitur", "hauptschule", "education"],
    "geo_name": ["bundesländer", "bundeslaender", "bundesland", "ländervergleich", "laendervergleich", "vergleich der länder", "regional", "regionen", "länder", "laender", "states"],
    "year": ["zeit", "entwicklung", "trend", "verlauf", "seit", "über die jahre", "jahre", "zeitreihe", "historisch", "früher", "damals", "gesunken", "gestiegen", "rückgang", "veränderung", "over time"],
    "group": ["rauchart", "familienstand", "erwerb", "schulart", "deprivation", "teilbereich", "produkt", "berufliche"],
}
FAMILIES = {
    "youth_smoking_current": ["youth_smoking_30d", "youth_smoking_ever"],
    "youth_smoking_30d": ["youth_smoking_current", "youth_smoking_ever"],
    "youth_smoking_ever": ["youth_smoking_30d", "youth_smoking_current"],
    "smoking_daily": ["smoking_current"],
    "smoking_occasional": ["smoking_current"],
    "smoking_heavy": ["smoking_daily"],
}
SEX_FILTERS = {"männer": "männlich", "maenner": "männlich", "männlich": "männlich", "mann": "männlich",
               "frauen": "weiblich", "weiblich": "weiblich", "frau": "weiblich"}


@dataclass
class Selection:
    indicator: str
    geo: str
    breakdown: str | None = None
    year: int | None = None
    sex: str = "gesamt"
    matched: list[str] = field(default_factory=list)


@dataclass
class Answer:
    text: str
    data: pd.DataFrame
    selection: Selection
    sources: list[str]


def load(path: str | pathlib.Path | None = None) -> pd.DataFrame:
    """Load the harmonized dataset (``dataset/indicators.csv``)."""
    df = pd.read_csv(path or DATASET, dtype={"group_type": str, "group": str, "note": str,
                                            "period": str, "source_url": str}, keep_default_na=False)
    for col in ["value", "ci_lower", "ci_upper", "n"]:
        df[col] = pd.to_numeric(df[col].replace("", pd.NA), errors="coerce")
    df["year"] = df["year"].astype(int)
    return df


def _fmt(value: float, unit: str) -> str:
    if pd.isna(value):
        return "–"
    s = f"{value:,.1f}".replace(",", "X").replace(".", ",").replace("X", ".")
    if s.endswith(",0") and unit != "percent":
        s = s[:-2]
    return f"{s} {UNIT_LABELS.get(unit, unit)}".replace(" %", " %")


def select(df: pd.DataFrame, indicator: str, geo: str = "Deutschland",
           breakdown: str | None = None, year: int | None = None,
           sex: str = "gesamt", standardization: str = "beobachtet") -> pd.DataFrame:
    """Filter the dataset to one indicator / area, optionally broken down by
    ``sex``, ``age_group``, ``education``, ``group``, ``geo_name`` (all
    Bundesländer) or ``year`` (time series). Dimensions not broken down are
    held at their total ("gesamt")."""
    d = df[df["indicator_id"] == indicator]
    if breakdown == "geo_name":
        d = d[d["geo_level"].isin(["state", "germany"])]
    else:
        d = d[d["geo_name"] == geo]
    for dim in ["sex", "age_group", "education"]:
        if breakdown != dim:
            want = sex if dim == "sex" else "gesamt"
            if (d[dim] == want).any():
                d = d[d[dim] == want]
            elif dim == "sex":
                d = d.iloc[0:0]
            # else: indicator only published for one specific group (e.g. "9./10. Klasse") – keep it
    if breakdown != "group":
        d = d[d["group_type"] == ""]
    else:
        d = d[d["group_type"] != ""]
    # Prefer observed values; fall back to standardized when nothing observed exists
    if (d["standardization"] == standardization).any():
        d = d[d["standardization"] == standardization]
    if breakdown in ("sex", "age_group", "education", "group"):
        has_real = d[d[breakdown if breakdown != "group" else "group"] != "gesamt"]["source_id"].unique()
        d = d[d["source_id"].isin(has_real)]
    if year is not None and breakdown == "year":
        d = d[d["year"] >= year] if (d["year"] >= year).any() else d
    if year is not None and breakdown != "year":
        d = d[d["year"] == year] if (d["year"] == year).any() else d
    if breakdown != "year" and year is None and len(d):
        # latest year per source keeps one bar per category
        latest = d.groupby("source_id")["year"].transform("max")
        d = d[d["year"] == latest]
    return d.sort_values(["source_id", "year", "sex", "age_group", "education", "group", "geo_name"]).reset_index(drop=True)


def parse_question(question: str) -> Selection:
    q = question.lower()
    tokens = re.findall(r"[a-zäöüß0-9./-]+", q)
    matched: list[str] = []

    # indicator: pick the catalog entry with the longest matching keyword
    best, best_len = "smoking_current", 0
    for ind, meta in INDICATORS.items():
        for kw in meta["keywords"]:
            if kw in q and len(kw) > best_len:
                best, best_len = ind, len(kw)
                matched.append(kw)
    if best == "lung_cancer_incidence" and any(k in q for k in INDICATORS["lung_cancer_mortality"]["keywords"]):
        best = "lung_cancer_mortality"
    if best in ("smoking_current",) and any(k in q for k in ("jugend", "kinder", "schüler", "schueler")):
        best = "youth_smoking_30d" if any(k in q for k in ("schüler", "schueler", "bayern")) else "youth_smoking_current"

    # geography
    geo = "Deutschland"
    for alias, name in GEO_ALIASES.items():
        if alias in q:
            geo = name
            matched.append(alias)
            break
    for name in STATES + REGIONS:
        if name.lower() in q:
            geo = name
            matched.append(name)
    if best in ("youth_smoking_30d", "youth_smoking_ever"):
        geo = "Bayern"
    if best == "tobacco_control_score" and geo == "Deutschland":
        pass

    # breakdown
    breakdown = None
    for dim, kws in BREAKDOWN_KEYWORDS.items():
        if any(kw in q for kw in kws):
            breakdown = dim
            matched.append(dim)
            break
    sex = "gesamt"
    for kw, val in SEX_FILTERS.items():
        if re.search(rf"\b{kw}\b", q):
            sex = val
    if breakdown == "sex" and sex != "gesamt" and not any(k in q for k in ("geschlecht", "vergleich", "unterschied", "und")):
        breakdown = None  # "Frauen in Bayern" = filter, not comparison
    if breakdown == "sex":
        sex = "gesamt"

    year = None
    m = re.search(r"\b(19[5-9]\d|20[0-4]\d)\b", q)
    if m:
        year = int(m.group(1))
    return Selection(indicator=best, geo=geo, breakdown=breakdown, year=year, sex=sex, matched=matched)


_DIM_LABELS = {"sex": "Geschlecht", "age_group": "Altersgruppe", "education": "Bildung",
               "geo_name": "Bundesland", "year": "Jahr", "group": "Merkmal"}
_SEX_LABEL = {"gesamt": "insgesamt", "männlich": "Männer", "weiblich": "Frauen"}


def _source_names(df: pd.DataFrame) -> list[str]:
    return sorted(df["source_id"].unique())


def answer(question: str, df: pd.DataFrame | None = None) -> Answer:
    """Deterministic answer: parse the question, select rows, write a German
    summary. Never invents numbers; says so when nothing matches."""
    if df is None:
        df = load()
    sel = parse_question(question)
    requested_breakdown = sel.breakdown
    meta = INDICATORS[sel.indicator]
    d = select(df, sel.indicator, sel.geo, sel.breakdown, sel.year, sel.sex)

    if d.empty and sel.breakdown:
        d = select(df, sel.indicator, sel.geo, None, sel.year, sel.sex)
        if not d.empty:
            sel.breakdown = None
    if d.empty:
        for alt in FAMILIES.get(sel.indicator, []):
            d = select(df, alt, sel.geo, sel.breakdown, sel.year, sel.sex)
            if d.empty and sel.breakdown:
                d = select(df, alt, sel.geo, None, sel.year, sel.sex)
            if not d.empty:
                sel.indicator = alt
                sel.breakdown = sel.breakdown if sel.breakdown and (d[sel.breakdown] != "gesamt").any() else None
                meta = INDICATORS[alt]
                break
    if d.empty:
        avail = sorted(df[df["indicator_id"] == sel.indicator]["geo_name"].unique())
        hint = (f" Für „{meta['label']}“ liegen Werte vor für: {', '.join(avail)}."
                if avail else " Für diesen Indikator enthält der Datensatz noch keine Werte;"
                             " siehe Quellenkatalog für Studien mit passenden Daten.")
        return Answer(f"Für „{meta['label']}“ in {sel.geo} liegen keine Werte im Datensatz vor.{hint}",
                      d, sel, [])

    unit = d["unit"].iloc[0]
    parts: list[str] = []
    if sel.breakdown == "year" or (sel.breakdown is None and d["year"].nunique() > 1):
        for src, g in d.groupby("source_id"):
            g = g.sort_values("year")
            first, last = g.iloc[0], g.iloc[-1]
            if len(g) > 1:
                parts.append(f"{meta['label']} in {sel.geo} ({_SEX_LABEL[sel.sex]}): {_fmt(first['value'], unit)} im Jahr {first['period']} "
                             f"und {_fmt(last['value'], unit)} im Jahr {last['period']} "
                             f"({'Rückgang' if last['value'] < first['value'] else 'Anstieg'} um "
                             f"{_fmt(abs(last['value'] - first['value']), unit).replace(' %', ' Prozentpunkte')}; Quelle: {src}).")
            else:
                parts.append(f"{meta['label']} in {sel.geo}: {_fmt(last['value'], unit)} ({last['period']}; Quelle: {src}).")
    elif sel.breakdown:
        col = sel.breakdown
        for src, g in d.groupby("source_id"):
            items = ", ".join(f"{row[col]}: {_fmt(row['value'], unit)}" for _, row in g.iterrows())
            parts.append(f"{meta['label']} in {sel.geo} nach {_DIM_LABELS[col]} ({g['period'].iloc[0]}; Quelle: {src}): {items}.")
    else:
        for _, row in d.iterrows():
            ci = (f" (95 %-KI {_fmt(row['ci_lower'], unit)} bis {_fmt(row['ci_upper'], unit)})"
                  if pd.notna(row["ci_lower"]) else "")
            parts.append(f"{meta['label']} in {row['geo_name']} ({_SEX_LABEL[row['sex']]}, {row['period']}): "
                         f"{_fmt(row['value'], unit)}{ci}. Quelle: {row['source_id']}, {row['source_ref']}.")
    notes = sorted({n for n in d["note"] if n})
    text = " ".join(parts)
    if requested_breakdown and sel.breakdown != requested_breakdown:
        text = (f"Eine Aufschlüsselung nach {_DIM_LABELS[requested_breakdown]} liegt für {sel.geo} "
                f"nicht vor; hier die verfügbaren Gesamtwerte. ") + text
    if notes:
        text += " Hinweis: " + " | ".join(notes[:3])
    return Answer(text, d, sel, _source_names(d))

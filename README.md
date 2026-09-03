# Tobacco Data Gateway

Offene Daten zum Rauchen, zu E-Zigaretten und Tabakfolgen für **München → Bayern → Deutschland**,
harmonisiert nach Geschlecht, Alter, Bildung, Region und Zeit – mit Antworten in Text und Grafik.
Ziel des Projekts ist es, Übersicht über vorhandene Datenquellen zu geben, um eine evidenzbasierte Grundlage für Präventionsmaßnahmen und gesundheitspolitische Entscheidungen zu bieten.

**Website:** https://felixhagemeister.github.io/tdata/ (GitHub Pages aus `docs/`)

Drei Zugänge zu denselben Daten:

| Zugang | Für wen | Wo |
|---|---|---|
| Website mit Frage-Box, Explorer, Grafiken, Tabellen, CSV-Export | Journalist:innen, Forschung, Think-Tanks, NGOs | `docs/` |
| Harmonisierter Datensatz (eine Zeile je Wert, mit Quelle, Tabelle und Seite) | Analysen in R, Python, Excel; KI-Agenten | `dataset/indicators.csv`, `docs/data/*.json` |
| Python-Paket `tobacco_gateway` | Skripte und Notebooks; Rohdaten-Abruf je Quelle | `tobacco_gateway/`, `sources/` |

---

## Schnellstart

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
```

```python
from tobacco_gateway import answer, load_indicators, select_indicators, fetch, query

# Frage in natürlicher Sprache (deterministisch, keine erfundenen Zahlen)
a = answer("Wie viele Menschen rauchen in Bayern?")
print(a.text)        # "Rauchen (täglich oder gelegentlich) in Bayern: 20,5 % (2017; Quelle: destatis_mikrozensus). ... 26,4 % (2019/2020; Quelle: rki_gbe_ncd) ..."
a.data               # die zugrunde liegenden Zeilen als DataFrame

# Harmonisierter Datensatz direkt
df = load_indicators()
select_indicators(df, "lung_cancer_mortality", geo="Bayern", breakdown="year")
select_indicators(df, "smoking_current", geo="Deutschland", breakdown="education")

# Rohdaten einer Quelle (Cache in data/, gitignored)
raw = fetch("rki_gbe_ncd")          # RKI-Indikatorensatz, nur Tabak-Zeilen
geda = fetch("rki_geda")            # GEDA 2019/2020 Open-Data-Aggregate

# Welche Quelle beantwortet eine Frage? (Katalogsuche über SOURCE.md)
for r in query("E-Zigaretten Jugendliche Bayern")[:3]:
    print(r.source_id, r.score)
```

Website lokal ansehen:

```bash
python -m http.server -d docs 8000   # http://localhost:8000
```

Datensatz neu bauen (lädt die Upstream-Dateien in `data/` und schreibt `dataset/` und `docs/data/`):

```bash
python scripts/build_dataset.py
pytest -q
```

---

## Was drin ist

Der harmonisierte Datensatz (`dataset/indicators.csv`, Stand siehe `dataset/build_info.json`) enthält
u. a.:

| Indikator | Gebiete | Jahre | Dimensionen | Quelle |
|---|---|---|---|---|
| Rauchen (täglich oder gelegentlich), ab 18 J. | Deutschland, alle Bundesländer | 2003–2019 | Geschlecht, Alter, Bildung | RKI GBE / Diabetes-Surveillance (GEDA) |
| Rauchen, täglich, gelegentlich, stark, ehemalig, nie; Rauchbeginn; Rauchart, ab 15 J. | Deutschland, alle Bundesländer | 2017 | Geschlecht, Alter (5-Jahres-Gruppen), Rauchart | Destatis Mikrozensus |
| Rauchen | München | 2016 | – | Münchner Gesundheitsbefragung |
| Rauchen | Oberpfalz | 2013, 2017 | – | LGL Suchtmonitoring (Mikrozensus) |
| Rauchen Schüler:innen 9./10. Klasse (30 Tage, jemals) | Bayern | 2011, 2019 | Geschlecht, Schulart | LGL Suchtmonitoring (ESPAD) |
| Rauchen 11–17 J. | Deutschland, RKI-Regionen | 2004, 2010, 2015 | Geschlecht, Alter | RKI (KiGGS) |
| Passivrauchbelastung | Deutschland, RKI-Regionen | 2014, 2019 | Geschlecht, Alter, Bildung | RKI GBE |
| Lungenkrebs: Inzidenz und Sterblichkeit je 100.000 | Deutschland, alle Bundesländer | 1999–2023 | Geschlecht, Alter, regionale Deprivation | RKI GBE (ZfKD, Todesursachenstatistik) |
| Tabakkontrollskala | Deutschland und 36 europäische Länder | 2021 | Teilbereiche | RKI GBE (TCS) |

Schema und Regeln: `dataset/README.md`. Indikatorenkatalog mit Definitionen: `tobacco_gateway/schema.py`
(exportiert nach `docs/data/catalog.json`).

**Bekannte Lücken (Stand 2026-09):** keine E-Zigaretten-/Tabakerhitzer-Zeitreihe (DEBRA, GEDA 2022/23 und
BZgA veröffentlichen sie nur in PDFs bzw. hinter Datennutzungsvereinbarungen); keine Kreisebene (Gesundheitsatlas
Bayern nur per manuellem Export); München nur ein Erhebungsjahr. Siehe `PLAN.md`, Phase 5.

---

## Struktur

```
tdata/
├── docs/                      # Website (GitHub Pages): index.html, app.js, engine.js, style.css
│   └── data/                  # indicators.json/.csv, catalog.json, sources.json (generiert)
├── dataset/
│   ├── indicators.csv         # harmonisierter Datensatz (im Repo, generiert)
│   ├── build_info.json        # Zeilen je Quelle, Build-Datum
│   └── README.md              # Schema
├── sources/                   # eine Mappe je Quelle
│   ├── INDEX.md               # Quellenverzeichnis (YAML + Tabelle)
│   └── <source_id>/
│       ├── SOURCE.md          # Metadaten (YAML-Frontmatter) + Notizen
│       ├── fetch.py           # Rohdaten laden (oder Anleitung, wenn manuell)
│       ├── extract.py         # optional: Rohdaten -> harmonisiertes Schema
│       └── curated.csv        # optional: aus PDFs übertragene Werte mit Seitenangabe
├── tobacco_gateway/           # Python-Paket
│   ├── schema.py              # Spalten, Indikatorenkatalog, Validierung
│   ├── indicators.py          # load(), select(), answer()  (Frage-Engine, Python)
│   ├── fetch.py               # fetch(source_id) Dispatcher
│   ├── query.py               # Katalogsuche über SOURCE.md
│   └── curated.py             # Loader für curated.csv
├── scripts/
│   ├── build_dataset.py       # Extraktoren ausführen, validieren, dataset/ und docs/data/ schreiben
│   └── fetch_all.py           # Rohdaten aller Quellen laden
├── notebooks/example_queries.ipynb
├── tests/                     # pytest: Schema, Spot-Checks, Frage-Engine, Katalog
├── .github/workflows/         # CI (Tests) und monatlicher Daten-Refresh als Pull Request
├── data/                      # gitignored: Rohdaten-Cache
├── PLAN.md · SOURCES_RESEARCH.md · pyproject.toml
```

---

## Grundsätze

- **Nur öffentlich zugängliche Daten.** Quellen mit Datennutzungsvereinbarung sind dokumentiert, ihre Werte
  werden nicht reproduziert.
- **Keine Rohdaten im Repo, aber ein kuratierter Aggregatdatensatz.** `dataset/indicators.csv` enthält
  ausschließlich veröffentlichte Kennzahlen mit Quellenangabe (Tabelle, Seite, Datenstand). Rohdateien
  landen im gitignorierten `data/`.
- **Keine erfundenen Zahlen.** Die Frage-Engine (`answer()` in Python, `engine.js` im Browser) ist
  deterministisch: Stichwörter wählen Indikator, Gebiet und Aufschlüsselung; Texte sind Vorlagen über
  den gefundenen Zeilen. Fehlt etwas, sagt sie das.
- **Quellen werden nicht stillschweigend gemischt.** Unterschiedliche Erhebungen (Mikrozensus ab 15 J.,
  GEDA ab 18 J., Telefonsurveys bis 2012) erscheinen als getrennte Reihen mit Hinweis.
- **Geografische Kaskade:** München vor Bayern vor Deutschland, wo Daten existieren.

## Quelle hinzufügen

1. `sources/<source_id>/SOURCE.md` mit YAML-Frontmatter anlegen (Vorlage: bestehende Quellen).
2. `fetch.py` mit `fetch(cache_dir="data/") -> pd.DataFrame` schreiben.
3. Werte in das Schema bringen: `extract.py` mit `extract(cache_dir) -> pd.DataFrame` (Spalten aus
   `tobacco_gateway.schema.COLUMNS`) **oder** `curated.csv` mit Seitenangabe in `source_ref`.
4. Eintrag in `sources/INDEX.md`; `python scripts/build_dataset.py`; `pytest`.

## Lizenz

Code: MIT. Daten: jeweils Lizenz der Quelle – RKI-Indikatoren CC BY 4.0, Destatis Datenlizenz
Deutschland – Namensnennung 2.0, Berichte des LGL Bayern und der Landeshauptstadt München mit
Quellenangabe. Bitte beim Weiterverwenden die Originalquelle nennen (in jeder Zeile: `source_id`,
`source_ref`, `source_url`).

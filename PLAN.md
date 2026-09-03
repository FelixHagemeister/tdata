# Tobacco Data Gateway — Project Plan

*Revised 2026-09-02. The original v0.1 plan (a source catalogue plus Python package) is kept as
Phases 1–3 below; Phases 4–5 add the harmonized dataset and the public web interface that the
project goal requires.*

## Goal

A public GitHub repository and website that give researchers, think tanks, advocacy organizations
and journalists a single, well-structured entry point to publicly available tobacco-related data for
**Munich → Bavaria → Germany**, across socio-demographic (sex, age, education, further attributes),
geographic (city, state, region, country) and time dimensions — with usable results **as text and
graphs on a web interface**, and machine-readable for AI agents.

## Decisions (interview 2026-09-02)

| Question | Decision | Consequence |
|---|---|---|
| Web stack | Static site on GitHub Pages (`docs/`) | No server; JSON files double as an API; charts and question engine run in the browser |
| Data in repo | Curated aggregate dataset is committed (`dataset/indicators.csv`) | Every row cites source, table/page and data status; raw microdata stays out (`data/` gitignored) |
| Interface language | German | Indicator labels, answer texts and UI in German; ids and code in English |
| Answer engine | Deterministic (keyword parsing + templates), no LLM in v1 | Works offline on a static page; no invented numbers; an LLM layer can be added later on the same data contract |

## Guiding principles

| Principle | Implication |
|---|---|
| Publicly available data only | Sources with data-use agreements are documented, their values not reproduced |
| No raw data in the repo; curated aggregates yes | `data/` is a gitignored cache; `dataset/indicators.csv` holds published figures with citations |
| Never mix surveys silently | Different surveys (Mikrozensus 15+, GEDA 18+, telephone surveys ≤ 2012) are separate series with notes |
| Geographic cascade | Prefer Munich, fall back to Bavaria, then Germany |
| Tobacco scope | Cigarettes, e-cigarettes, heated tobacco, plus consequences (lung cancer) and policy (tobacco control scale) |
| Language | Python for data and package; vanilla JS for the site (no build step, no dependencies) |
| Solo-maintained | Simple structure; tests and a monthly refresh workflow catch upstream changes |

## Architecture

```
sources/<id>/fetch.py  ──►  data/ (cache)  ──►  sources/<id>/extract.py ─┐
sources/<id>/curated.csv (figures transcribed from PDFs, with page refs) ─┤
                                                                          ▼
                     scripts/build_dataset.py  ──►  tobacco_gateway.schema.validate
                                                                          │
              ┌───────────────────────────────────────────────────────────┤
              ▼                                                           ▼
   dataset/indicators.csv (canonical, tracked)            docs/data/{indicators,catalog,sources}.json
   tobacco_gateway.indicators: load / select / answer     docs/engine.js (same rules) + docs/app.js (UI)
```

The harmonized schema (`tobacco_gateway/schema.py`) is the contract shared by extractors, package,
tests and website. One row = one published value with all dimensions and a citation.

## Repository structure

See README.md (kept in sync). Key additions since v0.1: `dataset/`, `docs/`, `tobacco_gateway/schema.py`,
`tobacco_gateway/indicators.py`, `sources/*/extract.py`, `sources/*/curated.csv`, `tests/`,
`.github/workflows/`.

## Phased roadmap

### Phase 1 — Foundation ✅
- [x] Project plan, README, package skeleton (`fetch`, `query`, `normalize`)
- [x] 13 sources with SOURCE.md + fetch.py; INDEX.md; example notebook

### Phase 2 — Source coverage ✅ (partly superseded)
- [x] Survey candidate sources and access conditions (SOURCES_RESEARCH.md)
- [x] Verified live downloads: Destatis Mikrozensus 2017 workbook; LGL and Munich PDFs
- [x] Discovered RKI open data on GitHub/Zenodo (GBE NCD indicators, Diabetes-Surveillance, GEDA 2019/2020 aggregates) — CC BY 4.0, machine-readable, Bundesland level. These replace the earlier "GEDA cannot be scraped" dead end.

### Phase 3 — Agent interface ✅
- [x] `query()` keyword matching over SOURCE.md
- [x] Machine-readable catalog (`docs/data/catalog.json`, `docs/data/sources.json`)

### Phase 4 — Harmonized dataset and web interface ✅ (2026-09-02)
- [x] Schema + indicator catalog with German labels and keywords
- [x] Extractors: `rki_gbe_ncd`, `rki_diabetes_surveillance`, `destatis_mikrozensus`
- [x] Curated figures with page references: `bgs_bayern` (Suchtmonitoring Bayern 2021), `muenchen_gesundheitsbefragung` (2016)
- [x] `scripts/build_dataset.py` with validation; 4,800 rows across 18 indicators
- [x] Python API: `load_indicators()`, `select_indicators()`, `answer()`
- [x] Website (`docs/`): question box with examples, explorer (indicator, area, breakdown, source, year, sex, standardization), answer text, SVG line/bar charts and stat tiles with tooltips, table, CSV export, shareable links, source catalogue, API section; light/dark theme; mobile layout
- [x] Tests (schema, spot checks against published figures, question engine, catalogue) and CI
- [x] Monthly refresh workflow that rebuilds from upstream and opens a pull request

### Phase 5 — Coverage gaps (next)
- [ ] **E-cigarettes / heated tobacco time series.** DEBRA factsheets (PDF) 2016–present, GEDA 2022/2023 fact sheets (Journal of Health Monitoring), BZgA Drogenaffinität reports: transcribe key figures into `curated.csv` with page references, or parse PDF tables with pdfplumber where layouts are stable.
- [ ] **Munich, second wave.** Münchner Gesundheitsbefragung 2021 report (Stadtbezirk breakdown if published); Gesundheitsbericht München with smoking figures — the 2015 file currently cached is the "Älter werden in München" study and holds no smoking data.
- [ ] **District level Bavaria.** Gesundheitsatlas Bayern (LGL) manual Excel export → `curated.csv`/`extract.py`; Mikrozensus 2013/2017 by Regierungsbezirk via GENESIS Bayern (login).
- [ ] **Historical Mikrozensus (1999–2013) for Germany and Bavaria** from older Destatis publications or GBE-Bund tables, to extend the trend before 2017.
- [ ] **Eurobarometer (GESIS, free login):** e-cigarette and heated tobacco prevalence for Germany 2017/2020 from microdata (pyreadstat).
- [ ] Publish the site (enable GitHub Pages from `docs/`), add the real repository URL in README/site, and register the dataset on Zenodo for a DOI.

### Phase 6 — Optional
- [ ] LLM-backed free-form answers on top of `catalog.json` + `indicators.json` (serverless function with an API key)
- [ ] Embedding-based source search
- [ ] Bilingual UI (English labels stored next to German ones in the catalog)

## Open questions (resolved)

1. **SPSS/Stata files** — keep `pyreadstat` for microdata sources (Eurobarometer, KiGGS PUF).
2. **Mikrozensus historical data** — include; marked `status: historical`.
3. **Caching** — `fetch.py` caches raw files in `data/`; `refresh=True` re-downloads. The build is reproducible from cache.
4. **Where do numbers from PDFs live?** — in `sources/<id>/curated.csv`, one row per value, with page and figure/table reference; validated like extracted rows.

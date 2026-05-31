# Tobacco Data Gateway — Project Plan

## Goal

A public GitHub repository that gives researchers, think tanks, and advocacy
organizations a single, well-structured entry point to publicly available
tobacco-related data for **Munich → Bavaria → Germany** (in order of
geographic preference).

The repository should be usable by both humans and AI agents: a human can
browse source documentation and run a script; an agent can read structured
metadata to decide which dataset answers a given question, then call the
appropriate fetch function.

---

## Guiding principles

| Principle | Implication |
|---|---|
| Publicly available data only | No sources requiring data-use agreements in v1 |
| No raw data in the repo | Scripts fetch from authoritative sources on demand |
| Geographic cascade | Prefer Munich data; fall back to Bavaria, then Germany |
| Tobacco scope | Cigarettes, e-cigarettes, heated tobacco products (HTP) |
| Time horizon | Past 10 years (~2015–present) |
| Language | Python |
| Solo-maintained | Keep structure simple; avoid over-engineering |

---

## Repository structure

```
tobacco-data-gateway/
│
├── README.md                  # Project overview, quick-start, source index
├── PLAN.md                    # This file
│
├── sources/                   # One folder per data source
│   ├── INDEX.md               # Machine- and human-readable index of all sources
│   ├── rki_geda/
│   │   ├── SOURCE.md          # Structured metadata (see schema below)
│   │   └── fetch.py           # Download + normalize this source
│   ├── bzga_youth_tobacco/
│   │   ├── SOURCE.md
│   │   └── fetch.py
│   └── ...
│
├── tobacco_gateway/           # Installable Python package
│   ├── __init__.py
│   ├── fetch.py               # fetch(source_id, ...) dispatcher
│   ├── normalize.py           # shared normalization utilities
│   └── query.py               # helper: "which sources answer this question?"
│
├── notebooks/
│   └── example_queries.ipynb  # Worked examples (e.g. e-cig trend, quit intent)
│
├── scripts/
│   └── fetch_all.py           # Bulk download all sources to local cache
│
├── data/                      # gitignored — local cache of downloaded data
│
├── pyproject.toml
└── .gitignore
```

---

## SOURCE.md schema

Each source gets a `SOURCE.md` with a YAML front-matter block followed by
human-readable notes. The YAML block is the contract for agent use.

```yaml
---
id: rki_geda_2022
name: "RKI GEDA 2022/2023 — Gesundheit in Deutschland aktuell"
provider: "Robert Koch-Institut (RKI)"
url: "https://www.rki.de/geda"
geographic_level: germany   # munich | bavaria | germany | europe
population: adults_18plus
age_range: [18, 99]
tobacco_topics:
  - smoking_prevalence
  - daily_vs_occasional_smoking
  - quit_attempts
  - e-cigarette_use
years_available: [2022, 2023]
update_frequency: biennial
data_format: csv            # csv | excel | api | pdf | spss
access_method: direct_download
license: "dl-de/by-2-0"    # or "unknown", "open", etc.
language: de
sample_questions:
  - "What share of adults in Germany smoke daily?"
  - "How many smokers attempted to quit in the past 12 months?"
fetch_script: sources/rki_geda/fetch.py
notes: >
  Representative sample of ~23,000 adults. Weights provided.
  Munich-level breakdowns not available; Bavarian subsample possible.
---
```

---

## Python package interface

```python
from tobacco_gateway import fetch, query

# Fetch a specific source into a pandas DataFrame
df = fetch("rki_geda_2022")

# Ask which sources can answer a question
sources = query("e-cigarette use trend by age group in Bavaria")
# → returns ranked list of source IDs with relevance notes

# Fetch all available sources to local cache
fetch("*")
```

The `query()` function in v1 will be keyword-based (matching against
`tobacco_topics` and `sample_questions` in SOURCE.md). In a later version it
can be backed by an embedding-based search or an LLM.

---

## Data hosting strategy

Raw data is **not** stored in the repository.

| Scenario | Approach |
|---|---|
| Data available via stable URL | `fetch.py` downloads directly; cached in `data/` (gitignored) |
| Data requires clicking through a form | Document steps in SOURCE.md; fetch.py automates where possible |
| Processed / normalized snapshots | Upload to **Zenodo** with DOI; link from SOURCE.md |

**Why Zenodo over OSF or hosting in GitHub?**
- Free, no account required to download
- DOIs make data citable
- 50 GB per record
- GitHub integration (auto-archive releases)
- Good programmatic access (REST API)

---

## Target data sources (to be discovered and verified)

The following are candidates; each needs a SOURCE.md once confirmed accessible.

### Germany-level
| Source | Provider | Key topics |
|---|---|---|
| GEDA (Gesundheit in Deutschland aktuell) | RKI | Smoking prevalence, quit attempts, e-cig |
| KiGGS (children/youth health) | RKI | Youth tobacco initiation |
| BZgA Drogenaffinitätsstudie | BZgA | Youth smoking & e-cig trends |
| BZgA Rauchverhalten Erwachsene | BZgA | Adult smoking behavior |
| DEBRA (Deutsche Befragung zum Rauchverhalten) | Univ. Leipzig / Surv. | Quit intent, e-cig prevalence |
| Microcensus (Mikrozensus) | Destatis | Smoking by region, age, income |
| Eurobarometer (Special/Standard) | EU Commission | Cross-country; Germany breakdowns |
| ITC Germany Survey | ITC Project | Policy response, quit attempts |

### Bavaria-level
| Source | Provider | Key topics |
|---|---|---|
| Gesundheitsatlas Bayern | LGL Bayern | Regional health indicators incl. smoking |
| Bavarian State Health Survey (BGS) | LGL Bayern | Smoking prevalence by district |
| Bayerisches Landesamt für Statistik | StaBa Bayern | Microcensus Bavaria |

### Munich-level
| Source | Provider | Key topics |
|---|---|---|
| Münchner Gesundheitsbefragung | Gesundheitsreferat München | Local smoking data |
| Munich health reporting (Gesundheitsbericht) | Landeshauptstadt München | Periodic reports; may include tobacco |

---

## Phased roadmap

### Phase 1 — Foundation (current)
- [x] Write project plan (this file)
- [ ] Create GitHub repository
- [ ] Write README and contributing guide
- [ ] Implement `tobacco_gateway` package skeleton
- [ ] Add 2–3 well-documented sources end-to-end (GEDA + BZgA as starting points)

### Phase 2 — Source coverage
- [ ] Survey all candidate sources; confirm accessibility
- [ ] Write SOURCE.md for each confirmed source
- [ ] Implement fetch.py per source
- [ ] Notebook: worked examples for 3–5 representative questions

### Phase 3 — Agent interface
- [ ] Implement `query()` with keyword matching
- [ ] Publish INDEX.md in a machine-readable format (JSON/YAML mirror)
- [ ] (Optional) Embed SOURCE.md summaries for semantic search

### Phase 4 — Data snapshots (optional)
- [ ] Normalize and upload processed datasets to Zenodo
- [ ] Link Zenodo DOIs from SOURCE.md files

---

## Open questions

1. **SPSS/Stata files** — Include `pyreadstat` as a dependency. Converting to CSV
   on fetch would discard variable labels, value labels, and missing-value
   metadata that downstream analyses may need; `pyreadstat` preserves all of
   that and returns a pandas DataFrame directly. Add `pyreadstat` to
   `pyproject.toml`; `fetch.py` scripts should read `.sav`/`.dta` with
   `pyreadstat.read_sav` / `pyreadstat.read_dta` and return a labeled DataFrame.

2. **Microzensus historical data** — Yes, include. Although smoking questions were
   dropped after 2017, the 2013–2017 waves provide the only district-level
   smoking-prevalence time series for Bavaria and Munich. Mark the source with
   `status: historical` in SOURCE.md and note the cutoff year explicitly.

3. **Caching behaviour** — `fetch.py` scripts always re-download; no caching by
   default. This keeps the code simple and ensures data freshness. Users who
   want to avoid repeated downloads can wrap calls in their own logic or use
   `scripts/fetch_all.py` once and work from `data/` locally.

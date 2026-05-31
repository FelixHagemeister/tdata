# Tobacco Data Gateway

A structured entry point to publicly available tobacco-related datasets for **Munich → Bavaria → Germany**.

Usable by humans (browse docs, run scripts) and AI agents (query structured metadata, call fetch functions).

---

## Quick start

```bash
pip install -e ".[dev]"
```

```python
from tobacco_gateway import fetch, query

# Which sources cover e-cigarette use in Bavaria?
results = query("e-cigarette use trend in Bavaria")
for r in results:
    print(r.source_id, r.score, r.tobacco_topics)

# Fetch Mikrozensus smoking data (free, no registration)
df = fetch("destatis_mikrozensus")

# Fetch district-level Bavaria data (manual export required)
df = fetch("gesundheitsatlas_bayern")   # reads from data/ cache

# Fetch all sources (results dict with DataFrames or exceptions)
all_data = fetch("*")
```

---

## Repository structure

```
tobacco-data-gateway/
├── README.md
├── PLAN.md                    # Project plan and guiding principles
├── SOURCES_RESEARCH.md        # Detailed source research notes
│
├── sources/
│   ├── INDEX.md               # Machine- and human-readable source index
│   ├── destatis_mikrozensus/
│   │   ├── SOURCE.md          # Structured metadata (YAML frontmatter)
│   │   └── fetch.py           # Download + normalize
│   └── ...                    # 12 more sources
│
├── tobacco_gateway/           # Installable Python package
│   ├── fetch.py               # fetch(source_id) dispatcher
│   ├── normalize.py           # Shared normalization utilities
│   └── query.py               # Keyword-based source matching
│
├── scripts/
│   └── fetch_all.py           # Bulk download all automatable sources
│
├── notebooks/
│   └── example_queries.ipynb  # Worked examples
│
└── data/                      # gitignored — local cache
```

---

## Source overview

| Source | Geography | Years | Access |
|---|---|---|---|
| [destatis_mikrozensus](sources/destatis_mikrozensus/SOURCE.md) | Germany | 1999–2017 | Free (scrape) |
| [staba_mikrozensus](sources/staba_mikrozensus/SOURCE.md) | Bavaria | 2009–2017 | Free (GENESIS) |
| [eurobarometer_tobacco](sources/eurobarometer_tobacco/SOURCE.md) | Germany | 2003–2021 | Free (GESIS registration) |
| [rki_geda](sources/rki_geda/SOURCE.md) | Germany | 2009–2023 | Aggregate free; microdata DUA |
| [rki_kiggs](sources/rki_kiggs/SOURCE.md) | Germany | 2006–2017 | Wave 1 PUF free; full DUA |
| [bzga_drogenaffinitaet](sources/bzga_drogenaffinitaet/SOURCE.md) | Germany | 1973–2021 | GESIS agreement (free) |
| [bzga_rauchverhalten](sources/bzga_rauchverhalten/SOURCE.md) | Germany | 1997–2021 | PDF free |
| [debra](sources/debra/SOURCE.md) | Germany | 2016–present | PDF free; microdata negotiation |
| [itc_germany](sources/itc_germany/SOURCE.md) | Germany | 2016–2022 | DUA (Univ. Waterloo) |
| [gesundheitsatlas_bayern](sources/gesundheitsatlas_bayern/SOURCE.md) | Bavaria (district) | 2015–2022 | Free (manual export) |
| [bgs_bayern](sources/bgs_bayern/SOURCE.md) | Bavaria | 2015–2022 | PDF free; microdata LGL |
| [muenchen_gesundheitsbefragung](sources/muenchen_gesundheitsbefragung/SOURCE.md) | Munich (Stadtbezirk) | 2016–2021 | PDF free; microdata negotiation |
| [muenchen_gesundheitsbericht](sources/muenchen_gesundheitsbericht/SOURCE.md) | Munich | 2004–2020 | PDF free |

---

## Geographic cascade

The gateway follows a **Munich → Bavaria → Germany** preference hierarchy:

| Level | Best source for smoking prevalence |
|---|---|
| Munich (district) | `muenchen_gesundheitsbefragung` |
| Munich (city) | `muenchen_gesundheitsbericht` |
| Bavaria (district) | `gesundheitsatlas_bayern` |
| Bavaria (state) | `staba_mikrozensus`, `bgs_bayern` |
| Germany | `destatis_mikrozensus`, `rki_geda`, `eurobarometer_tobacco` |

---

## Guiding principles

- **Public data only** — no sources requiring data-use agreements in automated v1 fetches
- **No raw data in the repo** — scripts fetch from authoritative sources on demand
- **No e-cigarette data before ~2014** — smoking modules predating e-cigs lack this variable
- **Mikrozensus smoking discontinued after 2017** — mark these sources as `status: historical`

---

## Data hosting

Raw data is not stored in this repository. Local cache lives in `data/` (gitignored).

For sources requiring registration or data-use agreements, `fetch.py` raises
a `FileNotFoundError` with step-by-step download instructions.

---

## Contributing

Add a new source:
1. Create `sources/<source_id>/SOURCE.md` with the standard YAML frontmatter (see existing examples)
2. Create `sources/<source_id>/fetch.py` with a `fetch(cache_dir="data/") -> pd.DataFrame` function
3. Add an entry to `sources/INDEX.md`

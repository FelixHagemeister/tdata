---
id: bzga_drogenaffinitaet
name: "BZgA Drogenaffinitätsstudie — Jugendliche und junge Erwachsene"
provider: "Bundeszentrale für gesundheitliche Aufklärung (BZgA)"
url: "https://www.bzga.de/forschung/studien-untersuchungen/studien/suchtpraevention/"
geographic_level: germany
population: youth_and_young_adults
age_range: [12, 25]
tobacco_topics:
  - smoking_prevalence
  - smoking_initiation_age
  - cigarettes_per_day
  - product_type
  - e-cigarette_use
  - waterpipe_use
  - nicotine_pouches
  - perceived_smoking_risk
  - attitudes_toward_smoking
years_available: [1973, 1976, 1979, 1982, 1986, 1990, 1993, 1997, 2001, 2004, 2008, 2011, 2014, 2016, 2018, 2019, 2021]
status: active
update_frequency: irregular
data_format: spss
access_method: gesis_agreement
license: "GESIS Datenweitergabevertrag (free, no fee)"
language: de
gesis_series: "ZA3580"
pdf_reports_url: "https://www.bzga.de/infomaterialien/alkohol-tabak-drogen/"
sample_questions:
  - "What share of 12-17 year olds in Germany currently smoke?"
  - "At what age do young Germans typically start smoking?"
  - "How has e-cigarette use among young people changed since 2014?"
  - "What is the trend in youth smoking rates since the 1970s?"
fetch_script: sources/bzga_drogenaffinitaet/fetch.py
notes: >
  Longest-running youth tobacco survey in Germany — data back to 1973.
  n ≈ 3,000–7,000 per wave. PDF reports freely available.
  Microdata archived at GESIS (series ZA3580); requires a standard
  Datenweitergabevertrag (free, submit project description + signed form).
  E-cigarette variables from ~2014; nicotine pouches in most recent waves.
  Bavaria subsample possible in microdata (n ~150–300 per wave).
---

## BZgA Drogenaffinitätsstudie

The definitive long-run time series for youth tobacco trends in Germany,
running since 1973. The most recent waves cover e-cigarettes, heated
tobacco products, and nicotine pouches.

### Access

**PDF reports (free, no registration):**
<https://www.bzga.de/infomaterialien/alkohol-tabak-drogen/tabak/>

**Microdata (free, requires GESIS agreement):**
1. Search GESIS for study series ZA3580: <https://search.gesis.org/>
2. Download and sign the Datenweitergabevertrag
3. Submit with brief project description to GESIS
4. Receive download link (typically within days)
5. Place `.sav` files in `data/bzga_drogenaffinitaet/` and run `fetch()`

---
id: rki_geda
name: "RKI GEDA — Gesundheit in Deutschland aktuell"
provider: "Robert Koch-Institut (RKI)"
url: "https://www.rki.de/DE/Content/Gesundheitsmonitoring/Studien/Geda/Geda_node.html"
geographic_level: germany
population: adults_18plus
age_range: [18, 99]
tobacco_topics:
  - smoking_prevalence
  - daily_vs_occasional_smoking
  - cigarettes_per_day
  - quit_attempts
  - quit_intention
  - e-cigarette_use
  - heated_tobacco_products
  - nicotine_replacement_therapy
  - passive_smoking
years_available: [2009, 2010, 2012, 2015, 2020, 2023]
status: active
update_frequency: biennial
data_format: csv_aggregates__spss_microdata
access_method: open_data_aggregates__microdata_fdz
license: "CC BY 4.0 (aggregates); RKI data-use agreement (microdata)"
language: de
fdz_url: "https://www.rki.de/DE/Content/Forsch/FDZ/fdz_node.html"
aggregate_reports_url: "https://www.rki.de/EN/Content/Health_Monitoring/Journal_of_Health_Monitoring/Journal_node.html"
sample_questions:
  - "What share of adults in Germany smoke daily?"
  - "How many smokers attempted to quit in the past 12 months?"
  - "What is the prevalence of e-cigarette use in Germany?"
  - "How has smoking prevalence changed since 2009?"
  - "What share of adults use heated tobacco products like IQOS?"
fetch_script: sources/rki_geda/fetch.py
notes: >
  Germany's flagship adult health survey. Representative sample of ~23,000–33,000
  adults. Microdata access requires formal data-use agreement (Datennutzungsvertrag)
  with the RKI FDZ; analysis via remote desktop or on-site.
  Aggregated GEDA 2019/2020-EHIS results (prevalence by Bundesland, sex, age,
  education incl. smoking RCstatE_k3 and passive smoking RCpass4B_k2) are open data
  on GitHub (CC BY 4.0) — fetch.py downloads them without a DUA. The harmonized
  dataset takes these values via rki_gbe_ncd / rki_diabetes_surveillance.
  Bavaria possible in FDZ microdata (small n per Bundesland ~1,500–2,000).
  Munich not possible — no city-level geography in microdata.
  E-cigarette variables from 2019/20 onward; HTP from 2022/23.
---

## RKI GEDA — Gesundheit in Deutschland aktuell

GEDA is the gold standard for adult smoking surveillance in Germany.
It covers all major tobacco variables across six waves since 2009.

### Survey waves

| Wave | Field period | n | Notes |
|---|---|---|---|
| GEDA 2009 | 2008–2009 | ~21,000 | |
| GEDA 2010 | 2010 | ~22,000 | |
| GEDA 2012 | 2012 | ~19,000 | |
| GEDA 2014/15-EHIS | 2014–2015 | ~24,000 | European Health Interview Survey |
| GEDA 2019/20-EHIS | 2019–2020 | ~23,000 | First e-cig module |
| GEDA 2022/23 | 2022–2023 | ~33,000 | HTP + quit intention |

### Access tiers

| Tier | What | Requirements |
|---|---|---|
| Aggregate reports | Key statistics by age/sex | None — freely available |
| Scientific Use File | Full microdata | RKI FDZ data-use agreement |

Apply for microdata: <https://www.rki.de/DE/Content/Forsch/FDZ/fdz_node.html>

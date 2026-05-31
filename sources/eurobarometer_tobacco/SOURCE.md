---
id: eurobarometer_tobacco
name: "Eurobarometer Special Surveys on Tobacco (EB 458 / EB 506)"
provider: "European Commission (DG SANTE), archived at GESIS"
url: "https://www.gesis.org/en/eurobarometer-data-service/survey-series/special-eb"
geographic_level: germany
population: adults_15plus
age_range: [15, 99]
tobacco_topics:
  - smoking_prevalence
  - daily_vs_occasional_smoking
  - product_type
  - e-cigarette_use
  - heated_tobacco_products
  - nicotine_pouches
  - quit_attempts
  - cessation_aid_use
  - smoke_free_policy_attitudes
  - health_warning_awareness
  - smoking_initiation_age
years_available: [2003, 2006, 2009, 2012, 2017, 2021]
status: active
update_frequency: irregular
data_format: spss
access_method: gesis_download
license: "GESIS standard terms"
language: multi
gesis_ids:
  - id: ZA6925
    year: 2017
    doi: "https://doi.org/10.4232/1.13067"
  - id: ZA7780
    year: 2021
    doi: "https://doi.org/10.4232/1.13953"
sample_questions:
  - "What share of adults in Germany use e-cigarettes?"
  - "How many Germans have tried to quit smoking in the past 12 months?"
  - "What types of tobacco products do German smokers use?"
  - "What is the trend in heated tobacco product use in Germany?"
fetch_script: sources/eurobarometer_tobacco/fetch.py
notes: >
  Free microdata access via GESIS after free user account registration
  (no data-use agreement, no institutional affiliation required).
  ~1,500 respondents in Germany per wave (cross-sectional, face-to-face).
  No sub-national geographic identifiers — Germany as a whole only.
  The 2021 wave (ZA7780) includes heated tobacco products and nicotine pouches,
  making it the most complete tobacco product inventory available as free microdata.
  Earlier waves back to 2003 are also archived at GESIS (ZA3612, ZA4141, ZA4977, ZA5652).
---

## Eurobarometer Special Surveys on Tobacco

The European Commission's dedicated tobacco surveys are the only
freely available microdata covering e-cigarettes, heated tobacco
products, and nicotine pouches for Germany. Conducted roughly every
3–5 years across all EU member states.

### Available waves

| Wave | ZA number | Year | Key additions |
|---|---|---|---|
| EB 58.2 | ZA3612 | 2003 | Baseline tobacco |
| EB 64.1 | ZA4141 | 2006 | Cessation behavior |
| EB 72.3 | ZA4977 | 2009 | E-cigs introduced |
| EB 77.1 | ZA5652 | 2012 | Plain packaging attitudes |
| **EB 87.1** | **ZA6925** | **2017** | Full e-cig module |
| **EB 96.2** | **ZA7780** | **2021** | HTP + nicotine pouches |

### Access

1. Register for a free GESIS account: <https://login.gesis.org>
2. Download the `.sav` file for ZA6925 and/or ZA7780
3. Place in `data/eurobarometer/` and run `fetch("eurobarometer_tobacco")`

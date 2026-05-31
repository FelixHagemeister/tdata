---
id: bgs_bayern
name: "Bayerische Gesundheitsstudie (BGS) — LGL Bayern"
provider: "Bayerisches Landesamt für Gesundheit und Lebensmittelsicherheit (LGL)"
url: "https://www.lgl.bayern.de/gesundheit/gesundheitsberichterstattung/gesundheitsstudien/"
geographic_level: bavaria
population: adults_18plus
age_range: [18, 99]
tobacco_topics:
  - smoking_prevalence
  - daily_vs_occasional_smoking
  - cigarettes_per_day
  - smoking_initiation_age
  - passive_smoking
  - quit_attempts
  - e-cigarette_use
  - waterpipe_use
years_available: [2015, 2022]
status: active
update_frequency: biennial
data_format: pdf
access_method: pdf_or_lgl_agreement
license: "PDF reports: free; microdata: LGL data-use agreement"
language: de
reports_url: "https://www.lgl.bayern.de/gesundheit/gesundheitsberichterstattung/gesundheitsberichte/"
sample_questions:
  - "What is the smoking prevalence among adults in Bavaria?"
  - "How has Bavarian smoking changed from 2015 to 2022?"
  - "What share of Bavarian adults have tried e-cigarettes?"
fetch_script: sources/bgs_bayern/fetch.py
notes: >
  The primary source of individual-level tobacco data for Bavaria.
  Published PDF reports freely available. Microdata held internally by LGL;
  formal data-use agreement with LGL Bayern required for access.
  Contact: gesundheitsberichterstattung@lgl.bayern.de
  District-level breakdowns not published (sample sizes too small);
  Regierungsbezirk-level may appear in some tables.
  Underlying data source for the Gesundheitsatlas Bayern district maps.
  E-cigarette variables added in Wave 2 (2021/22).
---

## Bayerische Gesundheitsstudie (BGS)

The backbone of Bavarian health surveillance. The BGS is conducted
every ~7 years as a statewide representative survey.

### Waves

| Wave | Field period | n (adults) |
|---|---|---|
| BGS Wave 1 | 2014–2015 | ~5,000 |
| BGS Wave 2 | 2021–2022 | ~5,000 |

### Reports

Freely downloadable from LGL:
<https://www.lgl.bayern.de/gesundheit/gesundheitsberichterstattung/gesundheitsberichte/>

### Microdata

Contact LGL Bayern: gesundheitsberichterstattung@lgl.bayern.de

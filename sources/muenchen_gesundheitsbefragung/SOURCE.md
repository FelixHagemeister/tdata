---
id: muenchen_gesundheitsbefragung
name: "Münchner Gesundheitsbefragung — Gesundheitsreferat München"
provider: "Referat für Gesundheit und Umwelt (RGU), Landeshauptstadt München"
url: "https://www.muenchen.de/rathaus/stadtinfos/gesundheit/gesundheitsberichterstattung/muenchner-gesundheitsbefragung.html"
geographic_level: munich
population: adults_18plus
age_range: [18, 99]
tobacco_topics:
  - smoking_prevalence
  - cigarettes_per_day
  - e-cigarette_use
  - passive_smoking
  - quit_intention
  - quit_attempts
years_available: [2016, 2021]
status: active
update_frequency: irregular
data_format: pdf
access_method: pdf_or_negotiation
license: "PDF reports: free; microdata: negotiated with Gesundheitsreferat"
language: de
sample_questions:
  - "What is the smoking prevalence in Munich overall?"
  - "Which Munich Stadtbezirk has the highest smoking rate?"
  - "How does smoking prevalence vary across Munich's 25 urban districts?"
  - "What share of Munich adults have tried e-cigarettes?"
fetch_script: sources/muenchen_gesundheitsbefragung/fetch.py
notes: >
  The ONLY source with sub-city (Stadtbezirk-level) smoking data for
  Munich. Covers all 25 Munich urban districts. High priority for the
  Munich component of the gateway.
  PDF reports available; microdata negotiated directly with
  Gesundheitsreferat München (no formal public framework — case-by-case).
  Contact: gesundheitsreferat@muenchen.de
  Stratified by age, sex, Stadtbezirk, SES, migration background.
  E-cigarette variables added in 2020/21 wave.
---

## Münchner Gesundheitsbefragung

The only source offering smoking data at the Stadtbezirk level —
Munich's 25 urban districts. This is the most geographically granular
tobacco dataset in the gateway.

### Waves

| Wave | Field period | Notes |
|---|---|---|
| MGF 2015/16 | 2015–2016 | Traditional tobacco only |
| MGF 2020/21 | 2020–2021 | Added e-cigarettes; partly COVID-affected |

### Access

**PDF reports:** muenchen.de Gesundheitsberichterstattung

**Microdata:** Contact Gesundheitsreferat München
(gesundheitsreferat@muenchen.de) for individual data sharing arrangements.

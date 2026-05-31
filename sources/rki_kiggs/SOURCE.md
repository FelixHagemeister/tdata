---
id: rki_kiggs
name: "RKI KiGGS — Studie zur Gesundheit von Kindern und Jugendlichen"
provider: "Robert Koch-Institut (RKI)"
url: "https://www.rki.de/DE/Content/Gesundheitsmonitoring/Studien/KiGGS/kiggs_node.html"
geographic_level: germany
population: children_adolescents
age_range: [0, 17]
tobacco_topics:
  - youth_smoking_initiation
  - smoking_prevalence
  - daily_vs_occasional_smoking
  - cigarettes_per_day
  - smoking_initiation_age
  - passive_smoking
  - e-cigarette_use
  - waterpipe_use
  - quit_attempts
  - parental_smoking
years_available: [2006, 2012, 2017]
status: active
update_frequency: irregular
data_format: spss
access_method: rki_fdz
license: "RKI data-use agreement (Wave 1 PUF: free registration)"
language: de
puf_url: "https://www.rki.de/DE/Content/Forsch/FDZ/Datenzugang/Public_Use_File/public_use_file_node.html"
fdz_url: "https://www.rki.de/DE/Content/Forsch/FDZ/fdz_node.html"
sample_questions:
  - "At what age do German adolescents typically start smoking?"
  - "What share of 12-17 year olds in Germany have ever tried smoking?"
  - "How has youth smoking changed between 2006 and 2017?"
  - "What is the prevalence of passive smoking exposure among children?"
fetch_script: sources/rki_kiggs/fetch.py
notes: >
  Longitudinal cohort + cross-sectional design. Wave 1 Public Use File (PUF)
  is freely downloadable after free online registration at RKI FDZ — no
  formal data-use agreement needed. Geography is coarsened to East/West in the
  PUF. Full microdata (Baseline and Wave 2) requires FDZ agreement.
  E-cigarette variables only from Wave 2 (2014–2017) onward.
  Cohort linkage (Wave 1 → Wave 2) allows longitudinal smoking onset analysis.
---

## RKI KiGGS

The only nationally representative longitudinal youth health survey in Germany.
Covers tobacco initiation and use from early adolescence through young adulthood.

### Survey waves

| Wave | Field period | Design | n (tobacco age group) |
|---|---|---|---|
| Baseline (Wave 0) | 2003–2006 | Cross-sectional | ~5,500 (12–17) |
| Wave 1 | 2009–2012 | Cross-sec. + cohort | ~4,000 (12–17) |
| Wave 2 | 2014–2017 | Cross-sec. + cohort | ~5,500 (12–17) |

### Wave 1 Public Use File

Free download after registration (no DUA):
<https://www.rki.de/DE/Content/Forsch/FDZ/Datenzugang/Public_Use_File/public_use_file_node.html>

Note: geography coarsened (East/West only), some variables removed.

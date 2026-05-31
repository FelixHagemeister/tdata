---
id: muenchen_gesundheitsbericht
name: "Münchner Gesundheitsbericht — Landeshauptstadt München"
provider: "Landeshauptstadt München (LHM)"
url: "https://www.muenchen.de/rathaus/stadtinfos/gesundheit/gesundheitsberichterstattung/gesundheitsberichte.html"
geographic_level: munich
population: all
age_range: [0, 99]
tobacco_topics:
  - smoking_prevalence
  - passive_smoking
  - smoking_related_mortality
  - smoking_related_hospitalizations
  - youth_smoking
  - e-cigarette_use
years_available: [2004, 2009, 2014, 2020]
status: active
update_frequency: quinquennial
data_format: pdf
access_method: direct_download
license: "public document (free)"
language: de
sample_questions:
  - "How does Munich's smoking prevalence compare to Bavaria and Germany?"
  - "What are the smoking-related mortality rates in Munich?"
  - "How has smoking prevalence in Munich changed over time?"
fetch_script: sources/muenchen_gesundheitsbericht/fetch.py
notes: >
  Comprehensive periodic health report. PDF only — no structured data download.
  Synthesizes data from BGS, Mikrozensus, Münchner Gesundheitsbefragung,
  and administrative health records. Useful as a secondary reference and for
  Munich vs. Bavaria vs. Germany trend comparisons.
  Smoking chapter covers prevalence by age and sex, hospitalization/mortality,
  passive smoking, and youth tobacco. E-cigarettes mentioned in 2019/20 edition.
  Not a primary data source — underlying data comes from other gateway sources.
---

## Münchner Gesundheitsbericht

Comprehensive health status reports published approximately every 5 years.
Synthesizes multiple data sources with a Munich focus.

### Editions

| Edition | Year | Tobacco chapter? |
|---|---|---|
| 1st edition | 2004 | Yes |
| 2nd edition | 2009 | Yes |
| 3rd edition | 2014 | Yes |
| 4th edition | 2019/2020 | Yes (incl. e-cigs) |

### Access

All reports freely downloadable from LHM:
<https://www.muenchen.de/rathaus/stadtinfos/gesundheit/gesundheitsberichterstattung/gesundheitsberichte.html>

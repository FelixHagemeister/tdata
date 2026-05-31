---
id: staba_mikrozensus
name: "Mikrozensus Bayern — Rauchgewohnheiten (StaBa Bayern)"
provider: "Bayerisches Landesamt für Statistik (StaBa Bayern)"
url: "https://www.statistikdaten.bayern.de/genesis/"
geographic_level: bavaria
population: adults_15plus
age_range: [15, 99]
tobacco_topics:
  - smoking_prevalence
  - daily_vs_occasional_smoking
  - cigarettes_per_day
  - smoking_initiation_age
years_available: [2009, 2013, 2017]
status: historical
update_frequency: discontinued
data_format: excel
access_method: manual_download
license: "dl-de/by-2-0"
language: de
sample_questions:
  - "What share of adults in Bavaria smoked daily in 2017?"
  - "How has smoking prevalence changed in Bavaria from 2009 to 2017?"
  - "How does Bavarian smoking prevalence compare to the national average?"
fetch_script: sources/staba_mikrozensus/fetch.py
notes: >
  Bavaria-specific slice of the national Mikrozensus, available via
  GENESIS Bayern. Covers all 7 Regierungsbezirke. Smoking questions
  were dropped after 2017. Complements destatis_mikrozensus; use this
  source when Bavaria or sub-Bavaria geography is required.
  Munich (Landeshauptstadt) may appear as a separate unit in some tables.
---

## Mikrozensus Bayern

The Bavarian arm of the national Mikrozensus covers approximately
65,000 Bavarian households per year. The health supplement with
smoking variables ran from 2009 to 2017.

### Geographic granularity

- Bavaria state total
- 7 Regierungsbezirke (Oberbayern includes Munich)
- Munich as kreisfreie Stadt in broad tables

### Access

Aggregated tables are downloadable from GENESIS Bayern after creating
a free account: <https://www.statistikdaten.bayern.de/genesis/>

Anonymous (GUEST) API access was removed; login is now required.
Search for table series `12211` (Rauchgewohnheiten), export as CSV.

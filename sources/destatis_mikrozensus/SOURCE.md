---
id: destatis_mikrozensus
name: "Mikrozensus — Rauchgewohnheiten der Bevölkerung (Destatis)"
provider: "Statistisches Bundesamt (Destatis)"
url: "https://www.destatis.de/DE/Themen/Gesellschaft-Umwelt/Gesundheit/Gesundheitsverhalten-Risikofaktoren/Tabellen/rauchverhalten-mikrozensus.html"
geographic_level: germany
population: adults_15plus
age_range: [15, 99]
tobacco_topics:
  - smoking_prevalence
  - daily_vs_occasional_smoking
  - cigarettes_per_day
  - smoking_initiation_age
  - ex_smoker_cessation_duration
years_available: [1999, 2003, 2005, 2009, 2013, 2017]
status: historical
update_frequency: discontinued
data_format: html_table
access_method: direct_scrape
license: "dl-de/by-2-0"
language: de
sample_questions:
  - "What share of adults in Germany smoked daily in 2017?"
  - "How has smoking prevalence changed from 2005 to 2017?"
  - "What percentage of men vs. women smoke in Germany?"
  - "How many cigarettes per day do daily smokers consume?"
fetch_script: sources/destatis_mikrozensus/fetch.py
notes: >
  The health supplement of the Mikrozensus (Germany's largest annual
  household survey, ~800,000 persons) included smoking questions in
  1999, 2003, 2005, 2009, 2013, and 2017. The smoking module was
  discontinued after 2017. Bavaria and Regierungsbezirk breakdowns
  are available in the aggregated GENESIS tables (see staba_mikrozensus).
  No e-cigarette variables — module discontinued before they were added.
  Bavarian subsample available in GENESIS Bayern (see staba_mikrozensus).
---

## Mikrozensus — Rauchgewohnheiten

The Mikrozensus health supplement is Germany's most comprehensive
population-level smoking time-series covering 1999–2017. Its large
sample (~800,000 households) makes it uniquely suited for regional
and demographic subgroup analysis.

### Key indicators

| Indicator | Years |
|---|---|
| Smoking status (daily / occasional / former / never) | 1999–2017 |
| Cigarettes per day | 1999–2017 |
| Age at smoking initiation | 2003–2017 |
| Years since quitting (ex-smokers) | 2005–2017 |
| Passive smoking at workplace | 2009–2017 |

### Access

Aggregated tables are freely downloadable from the Destatis website
(no registration). The `fetch.py` script scrapes the HTML table.

For Bavaria-specific data, use `staba_mikrozensus`.

For microdata (SPSS/Stata), apply via the FDZ:
<https://www.forschungsdatenzentrum.de/de/zugang>

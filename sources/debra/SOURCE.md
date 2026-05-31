---
id: debra
name: "DEBRA — Deutsche Befragung zum Rauchverhalten"
provider: "Universität Leipzig / Kantar"
url: "https://www.debra-studie.de"
geographic_level: germany
population: adults_14plus
age_range: [14, 99]
tobacco_topics:
  - smoking_prevalence
  - daily_vs_occasional_smoking
  - cigarettes_per_day
  - e-cigarette_use
  - heated_tobacco_products
  - quit_attempts
  - quit_intention
  - cessation_aid_use
years_available_continuous: "2016-present"
update_frequency: monthly
data_format: pdf
access_method: pdf_or_dua
license: "PDF reports: free; microdata: case-by-case agreement"
language: de
sample_questions:
  - "What is the current quit intent rate among German smokers?"
  - "How many German smokers are currently trying to quit?"
  - "What cessation aids are being used by German smokers?"
  - "What is the monthly trend in e-cigarette use in Germany?"
fetch_script: sources/debra/fetch.py
notes: >
  Monthly cross-sectional telephone survey (~2,000 respondents/month),
  running since January 2016. Best source for temporal granularity on
  quit intent and cessation behavior. Aggregate trend data in annual PDF
  reports and peer-reviewed articles (Suchtmedizin, Addiction, Tobacco Control).
  Microdata not in any public repository — case-by-case agreement with
  University of Leipzig PI. Contact: info@debra-studie.de
  National sample only; Bavaria/Munich estimates unreliable without
  aggregating multiple months.
---

## DEBRA — Deutsche Befragung zum Rauchverhalten

The only monthly tobacco survey in Germany. Ideal for:
- Tracking quit intent trends over time
- Evaluating policy impacts (e.g. price increases, warning labels)
- Monitoring cessation aid uptake

### Access

**Annual PDF reports:** <https://www.debra-studie.de/publikationen>

**Peer-reviewed publications:** Search PubMed for "DEBRA study Germany"

**Microdata:** Contact info@debra-studie.de — case-by-case agreement
with the University of Leipzig research team.

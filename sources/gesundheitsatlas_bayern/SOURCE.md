---
id: gesundheitsatlas_bayern
name: "Gesundheitsatlas Bayern — Raucherstatus (LGL Bayern)"
provider: "Bayerisches Landesamt für Gesundheit und Lebensmittelsicherheit (LGL)"
url: "https://www.gesundheitsatlas.bayern.de"
geographic_level: bavaria
population: adults
age_range: [18, 99]
tobacco_topics:
  - smoking_prevalence
  - daily_vs_occasional_smoking
years_available: [2015, 2022]
status: active
update_frequency: biennial
data_format: excel
access_method: manual_export
license: "public health data (free)"
language: de
sample_questions:
  - "What is the smoking prevalence in Munich compared to other Bavarian districts?"
  - "Which Bavarian Landkreis has the highest smoking rate?"
  - "How does smoking prevalence vary across Bavaria's 96 districts?"
  - "What is Munich's smoking rate compared to the Bavarian average?"
fetch_script: sources/gesundheitsatlas_bayern/fetch.py
notes: >
  The ONLY freely available source with district-level smoking data for
  all 96 Bavarian Landkreise and kreisfreie Städte — including Munich
  as a separate unit. High priority for the geographic cascade goal.
  Data derives from the Bayerische Gesundheitsstudie (BGS).
  Access: interactive web tool only — no bulk download or public API.
  Use the Atlas export button (Excel/CSV) for each indicator view,
  then place the file in data/gesundheitsatlas_bayern/.
---

## Gesundheitsatlas Bayern

The only freely available smoking data at district level for Bavaria,
covering all 96 Landkreise and kreisfreie Städte including Munich.

### Manual export steps

1. Navigate to <https://www.gesundheitsatlas.bayern.de>
2. Select "Gesundheitsprofile" → "Sucht" → "Rauchen"
3. Select indicator: "Raucherstatus — aktuell Rauchende"
4. Click the export/download button (Excel icon)
5. Save the file to `data/gesundheitsatlas_bayern/raucherstatus.xlsx`
6. Run `fetch("gesundheitsatlas_bayern")`

### What you get

- All 96 Landkreise + kreisfreie Städte
- Munich (Landeshauptstadt München) as a distinct unit
- Male / female breakdowns
- Comparison to Bavarian state average
- Two waves: BGS Wave 1 (~2014/15) and Wave 2 (~2021/22)

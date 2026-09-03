---
id: rki_diabetes_surveillance
name: "RKI Diabetes-Surveillance — Indikator Rauchen"
provider: "Robert Koch-Institut (RKI), Nationale Diabetes-Surveillance"
url: "https://github.com/robert-koch-institut/Diabetes-Surveillance"
doi: "10.5281/zenodo.7972384"
geographic_level: germany
granularity: bundesland
population: adults_and_youth
age_range: [11, 99]
tobacco_topics:
  - smoking_prevalence
  - youth_smoking_initiation
  - smoking_trend
years_available: [2003, 2004, 2009, 2010, 2012, 2015, 2019]
status: active
update_frequency: yearly
data_format: tsv
access_method: direct_download
license: "CC BY 4.0"
language: de
sample_questions:
  - "Wie hat sich der Raucheranteil in Deutschland seit 2003 entwickelt?"
  - "Wie viele Jugendliche rauchen in Deutschland?"
  - "Rauchen nach Bildungsgruppe im Zeitverlauf"
fetch_script: sources/rki_diabetes_surveillance/fetch.py
extract_script: sources/rki_diabetes_surveillance/extract.py
notes: >
  Die Diabetes-Surveillance führt Rauchen als Risikofaktor. Erwachsene: GSTel03,
  GEDA 2009, 2010, 2012 und GEDA 2019/2020-EHIS (Deutschland nach Geschlecht, Alter,
  Bildung; 2019 zusätzlich nach Bundesland). Kinder und Jugendliche (11–17 Jahre):
  KiGGS-Basiserhebung 2003–2006, Welle 1 2009–2012, Welle 2 2014–2017. Telefonsurveys
  bis 2012 sind mit dem Mixed-Mode-Survey 2019/2020 nur eingeschränkt vergleichbar.
  Die Werte für 2019 werden im harmonisierten Datensatz aus rki_gbe_ncd übernommen.
---

# RKI Diabetes-Surveillance — Rauchen

Der Indikatorensatz der Nationalen Diabetes-Surveillance (CC BY 4.0) enthält den
Indikator "Rauchen" (Handlungsfeld 1: Diabetesrisiko reduzieren) mit der längsten
frei verfügbaren Zeitreihe aus RKI-Surveys. `fetch.py` lädt die TSV (ca. 3 MB) und
gibt die Rauch-Zeilen zurück; `extract.py` bildet sie auf `smoking_current`
(Erwachsene) und `youth_smoking_current` (11–17 Jahre) ab.

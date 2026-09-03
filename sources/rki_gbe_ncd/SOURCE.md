---
id: rki_gbe_ncd
name: "RKI Gesundheitsberichterstattung — Indikatoren zu nichtübertragbaren Erkrankungen"
provider: "Robert Koch-Institut (RKI), Gesundheitsberichterstattung des Bundes"
url: "https://github.com/robert-koch-institut/Gesundheitsberichterstattung_-_Daten_zu_nichtuebertragbaren_Erkrankungen"
doi: "10.5281/zenodo.13920400"
geographic_level: germany
granularity: bundesland
population: adults_18plus
age_range: [18, 99]
tobacco_topics:
  - smoking_prevalence
  - passive_smoking
  - lung_cancer_incidence
  - lung_cancer_mortality
  - tobacco_control_policy
years_available: [1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023]
status: active
update_frequency: yearly
data_format: tsv
access_method: direct_download
license: "CC BY 4.0"
language: de
sample_questions:
  - "Wie hoch ist der Raucheranteil in Bayern im Vergleich zu anderen Bundesländern?"
  - "Wie unterscheidet sich das Rauchen nach Bildung, Alter und Geschlecht?"
  - "Wie hat sich die Lungenkrebs-Sterblichkeit in Bayern seit 1999 entwickelt?"
  - "Wie schneidet Deutschland auf der Tabakkontrollskala ab?"
fetch_script: sources/rki_gbe_ncd/fetch.py
extract_script: sources/rki_gbe_ncd/extract.py
notes: >
  Indikatorensatz der Gesundheitsberichterstattung des Bundes (Diabetes-, NCD- und
  Public-Health-Indikatoren) als offene Daten auf GitHub/Zenodo. Tabakrelevant sind
  Indikator 1020501 "Rauchen (ab 18 Jahre)" (GEDA 2019/2020-EHIS; nach Bundesland,
  Geschlecht, Alter, Bildung), 1020502 "Passivrauchbelastung", 2020306/2020309
  "Lungenkrebs: Inzidenz/Sterblichkeit" (1999–2023 nach Bundesland, Geschlecht, Alter,
  regionaler Deprivation) und 4010101 "Tabakkontrolle" (Tobacco Control Scale 2021,
  Ländervergleich). Werte für Bayern verfügbar, keine Kreis- oder Stadtebene.
---

# RKI GBE — Daten zu nichtübertragbaren Erkrankungen

Das RKI veröffentlicht den Indikatorensatz seiner Gesundheitsberichterstattung als
eine TSV-Datei (ca. 20 MB, ca. 64.000 Zeilen) unter CC BY 4.0. Die Datei wird von
`fetch.py` in `data/rki_gbe_ncd/` zwischengespeichert; `extract.py` überführt die
tabakrelevanten Indikatoren in das harmonisierte Schema (`dataset/indicators.csv`).

## Enthaltene Tabak-Indikatoren

| Indikator-ID | Name | Zeitraum | Dimensionen |
|---|---|---|---|
| 1020501 | Rauchen (ab 18 Jahre) | 2019 (GEDA 2019/2020-EHIS) | Bundesland, Geschlecht, Alter, Bildung (CASMIN), beobachtet/altersstandardisiert |
| 1020502 | Passivrauchbelastung (ab 18 Jahre) | 2019 | RKI-Regionen, Geschlecht, Alter, Bildung |
| 2020306 | Lungenkrebs: Inzidenz | 1999–2023 | Bundesland, Geschlecht, Alter, GISD-Quintile |
| 2020309 | Lungenkrebs: Sterblichkeit | 1999–2023 | Bundesland, Geschlecht, Alter, GISD-Quintile |
| 4010101 | Tabakkontrolle (Tobacco Control Scale) | 2021 | Länder Europas, Teilbereiche |

## Zitierweise

Robert Koch-Institut (Hrsg.): Gesundheitsberichterstattung – Daten zu
nichtübertragbaren Erkrankungen. Berlin: Zenodo. DOI 10.5281/zenodo.13920400.
Der jeweilige `Datenstand` steht in jeder Zeile des harmonisierten Datensatzes
(`source_ref`).

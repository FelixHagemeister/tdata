# Harmonisierter Datensatz

`indicators.csv` – eine Zeile je veröffentlichtem Wert. Generiert von `scripts/build_dataset.py`
aus `sources/*/extract.py` und `sources/*/curated.csv`; bitte nicht von Hand editieren.

| Spalte | Inhalt |
|---|---|
| `indicator_id` | Schlüssel im Katalog `tobacco_gateway/schema.py` (z. B. `smoking_current`, `lung_cancer_mortality`) |
| `geo_level` | `germany`, `state` (Bundesland), `region` (Regierungsbezirk oder RKI-Region), `city`, `country` |
| `geo_name` | Deutschland, Bayern, München, Oberpfalz, … |
| `year` | Bezugsjahr (erstes Jahr eines Zeitraums) |
| `period` | Zeitraum wie veröffentlicht, z. B. `2019/2020` |
| `sex` | `gesamt`, `männlich`, `weiblich` |
| `age_group` | `gesamt` oder Gruppe wie `18–29`, `65+`, `9./10. Klasse` |
| `education` | `gesamt`, `niedrig`, `mittel`, `hoch` (CASMIN) |
| `group_type` / `group` | weitere Dimension, z. B. `Rauchart` / `Zigaretten`, `Schulart` / `Gymnasium`, `Regionale sozioökonomische Deprivation (GISD)` / `hoch (5. Quintil)` |
| `standardization` | `beobachtet` oder `altersstandardisiert` |
| `value`, `unit` | Wert und Einheit: `percent`, `per_100000`, `years`, `points` |
| `ci_lower`, `ci_upper` | 95-%-Konfidenzintervall, falls veröffentlicht |
| `n` | Stichprobe (Surveys), Fallzahl (Register) oder Bevölkerungsbasis in Personen (Mikrozensus) |
| `source_id` | Mappe unter `sources/` |
| `source_ref` | Tabelle, Indikator-ID, Seite und Datenstand in der Quelle |
| `source_url` | Datei oder Seite, aus der der Wert stammt |
| `note` | Erhebung, Grundgesamtheit, Vergleichbarkeitshinweise |

Regeln: keine Duplikate auf dem Schlüssel (Indikator, Gebiet, Jahr, Dimensionen, Standardisierung,
Quelle); Prozentwerte zwischen 0 und 100; jeder Wert hat `source_ref`. Geprüft von
`tobacco_gateway.schema.validate` im Build und in `tests/`.

---
# Tobacco Data Gateway — Source Index
# Machine-readable YAML block + human-readable table below.
# This file is auto-maintained; add new sources by creating SOURCE.md files.

sources:

  - id: destatis_mikrozensus
    name: "Mikrozensus — Rauchgewohnheiten (Destatis)"
    geographic_level: germany
    years: [1999, 2003, 2005, 2009, 2013, 2017]
    status: historical
    access: free
    topics: [smoking_prevalence, daily_vs_occasional, cigarettes_per_day]
    fetch_script: sources/destatis_mikrozensus/fetch.py

  - id: staba_mikrozensus
    name: "Mikrozensus Bayern (StaBa Bayern)"
    geographic_level: bavaria
    years: [2009, 2013, 2017]
    status: historical
    access: free
    topics: [smoking_prevalence, daily_vs_occasional, cigarettes_per_day]
    fetch_script: sources/staba_mikrozensus/fetch.py

  - id: eurobarometer_tobacco
    name: "Eurobarometer Special Tobacco Surveys (EB 458 / EB 506)"
    geographic_level: germany
    years: [2003, 2006, 2009, 2012, 2017, 2021]
    status: active
    access: free_registration  # free GESIS account, no DUA
    topics: [smoking_prevalence, e-cigarette_use, heated_tobacco_products,
             quit_attempts, cessation_aid_use, policy_attitudes]
    gesis_ids: [ZA6925, ZA7780]
    fetch_script: sources/eurobarometer_tobacco/fetch.py

  - id: rki_geda
    name: "RKI GEDA — Gesundheit in Deutschland aktuell"
    geographic_level: germany
    years: [2009, 2010, 2012, 2015, 2020, 2023]
    status: active
    access: aggregate_free__microdata_dua
    topics: [smoking_prevalence, quit_attempts, quit_intention,
             e-cigarette_use, heated_tobacco_products, passive_smoking]
    fetch_script: sources/rki_geda/fetch.py

  - id: rki_kiggs
    name: "RKI KiGGS — Kindergesundheitsstudie"
    geographic_level: germany
    years: [2006, 2012, 2017]
    status: active
    access: puf_free_registration__full_dua
    population: children_adolescents
    topics: [youth_smoking_initiation, smoking_prevalence, passive_smoking,
             e-cigarette_use, parental_smoking]
    fetch_script: sources/rki_kiggs/fetch.py

  - id: bzga_drogenaffinitaet
    name: "BZgA Drogenaffinitätsstudie"
    geographic_level: germany
    years: [1973, 1993, 2001, 2008, 2011, 2014, 2016, 2018, 2021]
    status: active
    access: gesis_agreement  # free, standard academic process
    population: youth_and_young_adults
    topics: [smoking_prevalence, youth_smoking_initiation, e-cigarette_use,
             nicotine_pouches, waterpipe_use]
    fetch_script: sources/bzga_drogenaffinitaet/fetch.py

  - id: bzga_rauchverhalten
    name: "BZgA Rauchverhalten der Bevölkerung"
    geographic_level: germany
    years: [1997, 2003, 2010, 2013, 2016, 2018, 2021]
    status: active
    access: pdf_free
    topics: [smoking_prevalence, e-cigarette_use, heated_tobacco_products,
             quit_attempts, cessation_aid_use]
    fetch_script: sources/bzga_rauchverhalten/fetch.py

  - id: debra
    name: "DEBRA — Deutsche Befragung zum Rauchverhalten"
    geographic_level: germany
    years_continuous: "2016-present"
    status: active
    access: pdf_free__microdata_negotiation
    topics: [smoking_prevalence, quit_intention, quit_attempts,
             e-cigarette_use, cessation_aid_use]
    fetch_script: sources/debra/fetch.py

  - id: itc_germany
    name: "ITC Germany / 4CV Survey"
    geographic_level: germany
    years: [2016, 2018, 2020, 2022]
    status: active
    access: dua_required  # Univ. Waterloo, ~2–6 weeks
    topics: [smoking_prevalence, e-cigarette_use, dual_use,
             quit_attempts, health_risk_perceptions, policy_attitudes,
             brand_price, cessation_aid_use]
    fetch_script: sources/itc_germany/fetch.py

  - id: gesundheitsatlas_bayern
    name: "Gesundheitsatlas Bayern (LGL)"
    geographic_level: bavaria
    granularity: landkreis  # 96 Landkreise + kreisfreie Städte incl. Munich
    years: [2015, 2022]
    status: active
    access: free_manual_export  # interactive tool, no bulk API
    topics: [smoking_prevalence, daily_vs_occasional]
    fetch_script: sources/gesundheitsatlas_bayern/fetch.py

  - id: bgs_bayern
    name: "Bayerische Gesundheitsstudie (BGS Bayern, LGL)"
    geographic_level: bavaria
    years: [2015, 2022]
    status: active
    access: pdf_free__microdata_lgl_agreement
    topics: [smoking_prevalence, daily_vs_occasional, quit_attempts,
             e-cigarette_use, passive_smoking]
    fetch_script: sources/bgs_bayern/fetch.py

  - id: muenchen_gesundheitsbefragung
    name: "Münchner Gesundheitsbefragung (Gesundheitsreferat München)"
    geographic_level: munich
    granularity: stadtbezirk  # 25 urban districts
    years: [2016, 2021]
    status: active
    access: pdf_free__microdata_negotiation
    topics: [smoking_prevalence, e-cigarette_use, passive_smoking, quit_intention]
    fetch_script: sources/muenchen_gesundheitsbefragung/fetch.py

  - id: muenchen_gesundheitsbericht
    name: "Münchner Gesundheitsbericht (LHM)"
    geographic_level: munich
    years: [2004, 2009, 2014, 2020]
    status: active
    access: pdf_free
    topics: [smoking_prevalence, passive_smoking, smoking_related_mortality]
    note: secondary_source  # synthesizes other sources
    fetch_script: sources/muenchen_gesundheitsbericht/fetch.py

---

## Source index

| ID | Name | Geography | Years | Access | Key topics |
|---|---|---|---|---|---|
| destatis_mikrozensus | Mikrozensus Destatis | Germany | 1999–2017 | Free | Prevalence, trend |
| staba_mikrozensus | Mikrozensus Bayern | Bavaria | 2009–2017 | Free | Prevalence, regional |
| eurobarometer_tobacco | Eurobarometer EB 458/506 | Germany | 2003–2021 | Free (GESIS reg.) | E-cig, HTP, quit behavior |
| rki_geda | RKI GEDA | Germany | 2009–2023 | Aggregate free; micro DUA | Full adult tobacco profile |
| rki_kiggs | RKI KiGGS | Germany | 2006–2017 | Wave 1 PUF free; full DUA | Youth initiation |
| bzga_drogenaffinitaet | BZgA Drogenaffinität | Germany | 1973–2021 | GESIS agreement | Youth long-run trend |
| bzga_rauchverhalten | BZgA Rauchverhalten | Germany | 1997–2021 | PDF free | Adult trend |
| debra | DEBRA | Germany | 2016–present | PDF free; micro negotiation | Quit intent, monthly |
| itc_germany | ITC Germany | Germany | 2016–2022 | DUA Univ. Waterloo | Policy, HTP, dual use |
| gesundheitsatlas_bayern | Gesundheitsatlas Bayern | Bavaria (district) | 2015–2022 | Free (manual export) | District-level prevalence |
| bgs_bayern | BGS Bayern | Bavaria | 2015–2022 | PDF free; micro LGL | Bavarian adult profile |
| muenchen_gesundheitsbefragung | Münchner Gesundheitsbefragung | Munich (Stadtbezirk) | 2016–2021 | PDF free; micro negotiation | Sub-city prevalence |
| muenchen_gesundheitsbericht | Münchner Gesundheitsbericht | Munich | 2004–2020 | PDF free | Munich vs. Bavaria trends |

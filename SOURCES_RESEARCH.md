# Tobacco Data Gateway — Source Research

> **Caveat:** Web access was unavailable during this research session. All findings
> are based on model training knowledge (cutoff August 2025). Every URL and access
> condition listed below **must be verified** before writing `SOURCE.md` files or
> `fetch.py` scripts.

---

## Quick reference table

| Source | Provider | Format | Free microdata? | Bavaria? | Munich? | Years (tobacco) |
|---|---|---|---|---|---|---|
| GEDA | RKI | SPSS/Stata (FDZ) | No — FDZ agreement | Small n | No | 2009–2023 |
| KiGGS | RKI | SPSS (PUF Welle 1 free) | Welle 1 PUF: free registration | Small n | No | 2003–2017 |
| Drogenaffinitätsstudie | BZgA / GESIS | SPSS/Stata | No — GESIS agreement | Small n | No | 1973–~2021 |
| Rauchverhalten Erwachsene | BZgA | PDF; SPSS unclear | No — contact BZgA | Small n | No | 1997–~2021 |
| DEBRA | Univ. Leipzig | PDF public; SPSS on request | No — case-by-case | No | No | 2016–present |
| Mikrozensus | Destatis / FDZ | Excel/CSV (agg.); SPSS (SUF) | Agg. tables free | Yes (agg. + SUF) | FDZ Regionalfile only | 1999–2017 |
| Eurobarometer (tobacco) | EU / GESIS | SPSS/Stata | **Yes** — free GESIS login | No | No | 2003–2021 |
| ITC Germany | Univ. Waterloo | SPSS | No — signed agreement | No | No | 2016–2022 |
| Gesundheitsatlas Bayern | LGL Bayern | Web + Excel/CSV export | Agg. only (free) | All 96 Landkreise | Yes (city unit) | ~2014–present |
| BGS Bayern | LGL Bayern | PDF (free); SPSS (agreement) | No — LGL agreement | Statewide | No | 2014/15, 2021/22 |
| Mikrozensus Bayern | StaBa Bayern | Excel/CSV via GENESIS | Agg. tables free | Bavaria + Regierungsbezirke | No | 2009, 2013, 2017, 2021 |
| Münchner Gesundheitsbefragung | Gesundheitsreferat München | PDF (free); microdata negotiated | Negotiate with city | No | Yes (Stadtbezirke) | ~2015/16, 2020/21 |
| Münchner Gesundheitsbericht | LHM München | PDF only (free) | No | No | Munich city only | ~2004, 2009, 2014, 2019/20 |

---

## Germany-level sources

---

### RKI GEDA — Gesundheit in Deutschland aktuell

**Provider:** Robert Koch-Institut (RKI)
**URLs:**
- Study homepage: `https://www.rki.de/DE/Content/Gesundheitsmonitoring/Studien/Geda/Geda_node.html`
- RKI FDZ: `https://www.rki.de/DE/Content/Forsch/FDZ/fdz_node.html`
- Journal of Health Monitoring (free aggregate results): `https://www.rki.de/EN/Content/Health_Monitoring/Journal_of_Health_Monitoring/Journal_node.html`

**Survey waves:**

| Wave | Field period | n |
|---|---|---|
| GEDA 2009 | 2008–2009 | ~21,000 |
| GEDA 2010 | 2010 | ~22,000 |
| GEDA 2012 | 2012 | ~19,000 |
| GEDA 2014/2015-EHIS | 2014–2015 | ~24,000 |
| GEDA 2019/2020-EHIS | 2019–2020 | ~23,000 |
| GEDA 2022/2023 | 2022–2023 | ~33,000 (rolling) |

**Data format:** SPSS (.sav) and/or Stata (.dta) for microdata; PDF/HTML for published reports.

**Access:**
- Aggregate reports/fact sheets: freely available, no registration.
- Microdata: formal **data-use agreement (Datennutzungsvertrag)** with the RKI FDZ required. Analysis via remote desktop or on-site; no file transfer of microdata.

**Bavaria / Munich:** Bavaria possible in FDZ files (small n per Bundesland). Munich not possible — no city-level geography in microdata.

**Tobacco variables:**
- Smoking status (daily / occasional / ex / never) — all waves
- Cigarettes per day — all waves
- Quit attempt in past 12 months — 2014/15, 2019/20, 2022/23
- Passive smoking exposure — several waves
- E-cigarette / vaping use — 2019/20 onward (more detail in 2022/23)
- Heated tobacco products (e.g. IQOS) — 2022/23
- Nicotine replacement therapy use — 2019/20, 2022/23
- Quit intention — 2022/23

**Phase 1 priority:** Yes — GEDA is the flagship adult health survey and should be one of the first two sources implemented.

---

### RKI KiGGS — Studie zur Gesundheit von Kindern und Jugendlichen

**Provider:** Robert Koch-Institut (RKI)
**URLs:**
- Study homepage: `https://www.rki.de/DE/Content/Gesundheitsmonitoring/Studien/KiGGS/kiggs_node.html`
- Public Use File page: `https://www.rki.de/DE/Content/Forsch/FDZ/Datenzugang/Public_Use_File/public_use_file_node.html`
- RKI FDZ: `https://www.rki.de/DE/Content/Forsch/FDZ/fdz_node.html`

**Survey waves:**

| Wave | Field period | Age group | n |
|---|---|---|---|
| Baseline (Welle 0) | 2003–2006 | 0–17 yrs | ~17,600 |
| Welle 1 | 2009–2012 | 0–17 (cross-sec.) + cohort | ~12,500 + 4,800 |
| Welle 2 | 2014–2017 | 0–17 (cross-sec.) + cohort | ~15,000 + 10,000 |

**Data format:** SPSS (.sav). Questionnaires as PDF.

**Access:**
- **KiGGS Welle 1 Public Use File (PUF):** SPSS download after **free online registration** — no formal data-use agreement. Coarser geography and reduced variables vs. scientific-use file.
- Baseline and Welle 2 full microdata: FDZ data-use agreement required.
- Aggregate reports: freely available.

**Bavaria / Munich:** Bavaria possible in FDZ scientific-use files (per-Bundesland n ~1,000–1,500). Not possible in PUF (geography coarsened to East/West). Munich not possible.

**Tobacco variables (12–17 age group and older cohort):**
- Ever tried smoking — all waves
- Current smoking status (never / occasional / daily / former) — all waves
- Age at smoking initiation — all waves
- Cigarettes per day — Welle 1, 2
- Passive smoking exposure (home, car) — all waves
- Parental smoking — all waves
- E-cigarette / vaping — Welle 2 onward
- Waterpipe / shisha — Welle 1, 2
- Quit attempt — Welle 2 cohort
- Longitudinal smoking onset — Welle 1 → Welle 2 cohort linkage

**Note:** The cohort design allows longitudinal analysis of tobacco initiation trajectories.

---

### BZgA Drogenaffinitätsstudie

**Provider:** Bundeszentrale für gesundheitliche Aufklärung (BZgA), archived at GESIS
**URLs:**
- BZgA study page: `https://www.bzga.de/forschung/studien-untersuchungen/studien/suchtpraevention/`
- GESIS search: `https://search.gesis.org/` — search "BZgA Drogenaffinität"
- Umbrella GESIS study number: **ZA3580** series (individual waves have separate ZA numbers, e.g. ZA7655 for 2019 — verify at GESIS)

**Population:** Youth ages 12–25, Germany-wide.

**Waves:** ~1973, 1976, 1979, 1982, 1986, 1990, 1993, 1997, 2001, 2004, 2008, 2011, 2014, 2016, 2018, 2019/2021. n ≈ 3,000–7,000 per wave.

**Data format:** SPSS (.sav) and Stata (.dta) at GESIS; PDF reports from BZgA.

**Access:**
- PDF reports: freely available from `https://www.bzga.de/infomaterialien/`
- Microdata: **GESIS data-use agreement (Datenweitergabevertrag)** — free, no fee, but requires project description and signed contract. Standard academic process.

**Bavaria / Munich:** Bavaria possible in microdata (per-state n ~150–300 — small but usable for broad trends). Munich not possible — no municipality identifier.

**Tobacco variables:**
- Smoking status (current / former / never)
- Age at smoking initiation
- Daily cigarette quantity
- Product type (cigarettes, roll-your-own, cigars, pipe)
- E-cigarette use (ever, current, frequency) — from ~2014
- Waterpipe / shisha
- Nicotine pouches — most recent waves
- Perceived risk of smoking
- Attitudes toward smoking

**Note:** E-cigarette coverage starts ~2014; earlier waves cover traditional tobacco only.

---

### BZgA Rauchverhalten der Bevölkerung in Deutschland

**Provider:** BZgA
**URLs:**
- PDF reports: `https://www.bzga.de/infomaterialien/alkohol-tabak-drogen/tabak/`
- Microdata: contact `forschung@bzga.de` — GESIS archival status for this series is **unconfirmed** (unlike the Drogenaffinitätsstudie)

**Population:** Adults (14+/18+), Germany-wide.

**Waves:** ~1997, 2003, 2007, 2010, 2012, 2013, 2014, 2016, 2018, 2021. n varies.

**Data format:** PDF reports (public); SPSS (.sav) for internal/requested microdata if available.

**Access:**
- PDF reports: freely available.
- Microdata: **unclear** — not consistently archived at GESIS. May require direct data request to BZgA research department.

**Bavaria / Munich:** National sample; Bavaria marginally feasible with small n; Munich not possible.

**Tobacco variables:**
- Smoking status (current / former / never)
- Daily vs. occasional smoking
- Daily cigarette quantity
- E-cigarette use (recent waves)
- Heated tobacco products (HTP, e.g. IQOS) — from ~2018
- Quit attempts and cessation behavior
- Use of cessation aids (NRT, apps, counseling)
- Secondhand smoke exposure

**Action needed:** Verify GESIS archival status or contact BZgA directly before writing `fetch.py`.

---

### DEBRA — Deutsche Befragung zum Rauchverhalten

**Provider:** University of Leipzig (Prof. Anil Batra) / Kantar
**URL:** `https://www.debra-studie.de` — publications at `https://www.debra-studie.de/publikationen`

**Design:** Monthly cross-sectional telephone survey, n ~2,000/month, running since January 2016.

**Data format:** No public microdata download. Aggregate trend data in peer-reviewed articles (*Suchtmedizin*, *Addiction*, *Tobacco Control*) and annual PDF reports on the website.

**Access:**
- PDF reports and journal articles: freely available.
- Microdata: **case-by-case data-use agreement** with University of Leipzig; not deposited in any open repository as of mid-2025.

**Bavaria / Munich:** National sample; ~2,000/month makes state-level estimates unreliable without aggregating many months. Munich not possible.

**Tobacco variables:**
- Smoking status (daily / occasional / former / never)
- Cigarettes per day
- E-cigarette / vaping use (current, former, never; frequency)
- Heated tobacco product use
- Quit attempts (past 12 months)
- Quit intention (stage of change)
- Use of cessation aids
- Sociodemographics (age, sex, education, employment)

**Note:** DEBRA is the best source for monthly trend data on quit intent and cessation aid use in Germany. Aggregate PDF data is usable without an agreement.

---

### Mikrozensus — Destatis

**Provider:** Statistisches Bundesamt (Destatis) + Statistische Landesämter
**URLs:**
- Destatis overview: `https://www.destatis.de/DE/Themen/Gesellschaft-Umwelt/Bevoelkerung/Haushalte-Familien/Methoden/mikrozensus.html`
- Published smoking tables: `https://www.destatis.de/DE/Themen/Gesellschaft-Umwelt/Gesundheit/Gesundheitsverhalten-Risikofaktoren/Tabellen/rauchverhalten-mikrozensus.html`
- GENESIS federal: `https://www-genesis.destatis.de` (table series **12211** / **23121**)
- FDZ microdata: `https://www.forschungsdatenzentrum.de/de/haushalte/mikrozensus`
- GESIS MISSY metadata: `https://www.gesis.org/missy/materials/MZ/`

**Health module waves with smoking questions:** 1999, 2003, 2005, 2009, 2013, **2017** (last). Smoking questions were **discontinued after 2017**.

**Data format:**
- GENESIS: Excel (.xlsx) and CSV (aggregated tables, free).
- SUF microdata: SPSS (.sav), Stata (.dta), CSV (70% subsample, via FDZ agreement).
- Campus File: further anonymized version for teaching.

**Access:**
- Aggregated GENESIS tables: **freely downloadable**, no registration.
- Scientific Use File (SUF): **formal FDZ data-use agreement** required. Apply at `https://www.forschungsdatenzentrum.de/de/zugang`.

**Bavaria / Munich:**
- Bavaria YES — Bundesland identifier in SUF and in GENESIS aggregate tables.
- Munich: only via FDZ Regionalfile (on-site access at FDZ), not in standard SUF. Not available in public tables.

**Tobacco variables (health module years):**
- Smoking status (daily / occasional / ex / never)
- Cigarettes per day
- Age at smoking initiation
- Years since quitting (ex-smokers)
- Passive smoking exposure at workplace
- No e-cigarette variable (module discontinued before e-cigs were added)

**Note (per plan):** Include as `status: historical` — marked as discontinued after 2017 but valuable for regional trend data 2009–2017.

---

### Eurobarometer Special Surveys on Tobacco

**Provider:** EU Commission (DG SANTE), archived at GESIS
**GESIS datasets:**

| EB | ZA number | Year | DOI |
|---|---|---|---|
| EB 239 / Spec. 58.2 | ZA3612 | 2003 | — |
| EB 272 / Spec. 64.1 | ZA4141 | 2006 | — |
| EB 332 / Spec. 72.3 | ZA4977 | 2009 | — |
| EB 385 / Spec. 77.1 | ZA5652 | 2012 | — |
| EB 458 / Spec. 87.1 | **ZA6925** | **2017** | `https://doi.org/10.4232/1.13067` |
| EB 506 / Spec. 96.2 | **ZA7780** | **2021** | `https://doi.org/10.4232/1.13953` |

**Data format:** SPSS (.sav) and Stata (.dta), with PDF questionnaires and codebooks.

**Access:** **Freely available** after free GESIS user account registration (no institutional affiliation required, no data-use agreement). Self-register at `https://login.gesis.org` and download same day.

**Bavaria / Munich:** Not possible — ~1,000 respondents per country; no sub-national regional identifiers in the tobacco Special Eurobarometers.

**Tobacco variables (EB 458 & EB 506):**
- Smoking status (daily / occasional / non-smoker / ex)
- Product type (manufactured cigarettes, RYO, cigars, pipe, shisha)
- E-cigarette / vaping use (EB 458 onward)
- Heated tobacco products (EB 506)
- Nicotine pouches (EB 506)
- Attitudes toward smoke-free policies
- Awareness of health warnings
- Quit attempts and motivation
- Use of cessation support / NRT
- Age at smoking initiation
- Urbanization level (but not Bundesland)

**Phase 1 priority:** Good candidate alongside GEDA — freely accessible microdata with no agreement required.

---

### ITC Germany Survey

**Provider:** International Tobacco Control Project, University of Waterloo (Canada)
**URLs:**
- Country page: `https://itcproject.org/countries/germany/`
- Data request: `https://itcproject.org/resources/data/`
- ITC 4CV (Four Country Smoking and Vaping): `https://itcproject.org/surveys/4cv/`

**Waves (Germany):**
- ITC 4CV Wave 1: 2016
- ITC 4CV Wave 2: 2018
- ITC 4CV Wave 3: 2020
- ITC Germany standalone: 2021–2022 (availability: "on request" as of mid-2025)

n ~4,000 adult smokers and vapers per wave (Germany); online panel (Kantar/YouGov).

**Data format:** SPSS (.sav) with PDF questionnaires and Excel codebooks.

**Access:** **Formal data-use agreement** with University of Waterloo required. Submit Data Request Form at the URL above; typical approval 2–6 weeks.

**Bavaria / Munich:** Not possible — no sub-national geographic identifiers in distributed files.

**Tobacco variables (most detailed instrument of all listed sources):**
- Smoking status (daily / non-daily / former / never)
- Cigarettes per day; brand; pack price
- E-cigarette / vaping: device type, frequency, nicotine concentration, reason for use
- Heated tobacco products (IQOS)
- Dual use (cigarettes + e-cigs)
- Quit attempts (number, recency, duration)
- Quit intentions (next month / 6 months / someday)
- Cessation methods (NRT, varenicline, bupropion, apps, quitlines)
- Policy attitudes (smoke-free laws, plain packaging, display bans)
- Health risk perceptions (cigarettes vs. e-cigs)
- Tobacco marketing exposure

---

## Bavaria-level sources

---

### Gesundheitsatlas Bayern (LGL Bayern)

**Provider:** Bayerisches Landesamt für Gesundheit und Lebensmittelsicherheit (LGL)
**URLs:**
- Atlas: `https://www.gesundheitsatlas.bayern.de`
- LGL entry: `https://www.lgl.bayern.de/gesundheit/gesundheitsberichterstattung/gesundheitsatlas/`

**Data format:** Interactive web app. Aggregated indicator values exportable as **Excel (.xlsx)** or **CSV** per displayed view. No bulk download, no public API.

**Access:** Freely accessible online, no registration. Aggregated district-level data can be exported directly.

**Geographic granularity:** All **96 Landkreise and kreisfreie Städte**, including Munich (Landeshauptstadt München) as a separate unit. Bavaria-wide summary also available.

**Tobacco variables:**
- Raucherstatus / Raucherquote (smoking prevalence, current smokers)
- Sex breakdown (male/female)
- Derived from BGS Bavaria (see below)
- Possibly also passive smoking and cessation indicators depending on wave

**Years:** ~2014/15 onward (BGS Welle 1 data), updated with BGS Welle 2 (~2021/22).

**Note:** This is the **only freely available source with district-level smoking data** for Bavaria including Munich. High priority for the gateway.

---

### BGS Bayern — Bayerische Gesundheitsstudie (LGL Bayern)

**Provider:** LGL Bayern
**URLs:**
- Health reports: `https://www.lgl.bayern.de/gesundheit/gesundheitsberichterstattung/gesundheitsberichte/`
- Study documentation: `https://www.lgl.bayern.de/gesundheit/gesundheitsberichterstattung/gesundheitsstudien/` (verify)
- Contact for microdata: `gesundheitsberichterstattung@lgl.bayern.de` (verify)

**Waves:**
- BGS Welle 1: 2014/2015
- BGS Welle 2: 2021/2022 (results published 2023–2024)

**Data format:** PDF reports (public); SPSS (.sav) internally at LGL (not released publicly).

**Access:**
- PDF reports: freely downloadable.
- Microdata: **formal data-use agreement with LGL Bayern** required. Contact the LGL health reporting team.

**Geographic granularity:** Bavaria statewide in published reports. District-level breakdowns not published (sample sizes too small). Regional groupings (Regierungsbezirke) may appear in some tables.

**Tobacco variables:**
- Smoking status (current / ex / never)
- Daily vs. occasional smoking
- Cigarettes per day
- Age at smoking initiation
- Passive smoking (home and work)
- Quit attempts
- E-cigarette / vaping use (Welle 2)
- Waterpipe / shisha
- Stratified by age, sex, education, migration background

---

### Mikrozensus Bayern — Bayerisches Landesamt für Statistik (StaBa Bayern)

**Provider:** Bayerisches Landesamt für Statistik
**URLs:**
- Main portal: `https://www.statistik.bayern.de`
- GENESIS Bayern: `https://www.statistikdaten.bayern.de/genesis/` — search table series **12211** (Mikrozensus Gesundheitsfragen / Rauchgewohnheiten)

**Health module years:** 2009, 2013, 2017 (smoking dropped after 2017). Possibly also 2021 for Bavaria.

**Data format:** Excel (.xlsx) and CSV from GENESIS Bayern (free, no registration).

**Access:** Aggregated GENESIS tables freely accessible and downloadable. Microdata (SUF) via federal FDZ (see Mikrozensus Destatis above).

**Geographic granularity:** Bavaria statewide and **Regierungsbezirk level** (7 regions). District (Landkreis) level not available for smoking. Munich appears as part of Oberbayern or as kreisfreie Stadt München in broad tables only.

**Tobacco variables:** Same as federal Mikrozensus (smoking status, quantity, initiation age) — no e-cigarettes.

**Note:** Complementary to the federal Mikrozensus Destatis source; GENESIS Bayern may offer more convenient Bavaria-specific table retrieval.

---

## Munich-level sources

---

### Münchner Gesundheitsbefragung

**Provider:** Gesundheitsreferat München (Referat für Gesundheit und Umwelt, RGU)
**URL:** `https://www.muenchen.de/rathaus/stadtinfos/gesundheit/gesundheitsberichterstattung/muenchner-gesundheitsbefragung.html` (verify)
- Contact for microdata: `gesundheitsreferat@muenchen.de` (verify)

**Waves:** ~2015/2016 and 2020/2021 (conducted partly under COVID conditions).

**Data format:** PDF reports (public); underlying data held by Gesundheitsreferat. No public microdata portal.

**Access:**
- PDF reports: free download from muenchen.de.
- Microdata / tabular data: must be **negotiated directly** with Gesundheitsreferat München. No formal public framework — case-by-case.

**Geographic granularity:** Munich city level, broken down by **Stadtbezirk** (25 urban districts) — highest geographic granularity of any source in this inventory.

**Tobacco variables:**
- Smoking status (current / ex / never)
- Cigarettes per day
- E-cigarette / vaping use (2020/21 wave)
- Passive smoking
- Quit intent / cessation attempts (some waves)
- Stratified by age, sex, Stadtbezirk, SES, migration background

**Note:** This is the **only source with sub-city geographic granularity** (Stadtbezirk level). High priority for the Munich component of the gateway. Even if microdata is not obtainable, the published PDFs are the closest thing to Munich-specific tobacco data.

---

### Münchner Gesundheitsbericht

**Provider:** Landeshauptstadt München
**URL:** `https://www.muenchen.de/rathaus/stadtinfos/gesundheit/gesundheitsberichterstattung/gesundheitsberichte.html` (verify)

**Editions:** ~2004, 2009, 2014, 2019/2020. Thematic supplements published between comprehensive editions.

**Data format:** PDF only. No structured download (no CSV/Excel/API). Tables embedded in PDF can be extracted.

**Access:** All PDF reports freely downloadable, no registration.

**Geographic granularity:** Munich city level as a whole; occasional Stadtbezirk maps for selected indicators. Not a primary data source — synthesizes data from BGS, Mikrozensus, Münchner Gesundheitsbefragung, and administrative records.

**Tobacco variables (chapter on substance use):**
- Smoking prevalence (Munich vs. Bavaria vs. Germany comparisons)
- Age- and sex-specific smoking rates
- Trends across report editions
- Passive smoking
- Smoking-related hospitalizations and mortality
- Youth smoking (from school surveys or KiGGS)
- E-cigarettes mentioned in most recent editions

**Note:** Useful as a secondary reference and for historical Munich trend comparisons. Not a primary data source — the underlying data comes from the other sources listed here.

---

## Key access findings

**Freely downloadable microdata (no agreement required):**
- Eurobarometer tobacco surveys (ZA6925, ZA7780) — free GESIS registration only
- KiGGS Welle 1 Public Use File — free GESIS-style registration at RKI FDZ

**Freely downloadable aggregated data:**
- Gesundheitsatlas Bayern — Excel/CSV export, district level incl. Munich
- Mikrozensus GENESIS tables (Destatis + StaBa Bayern) — Bavaria and Regierungsbezirk level
- All PDF reports from GEDA, KiGGS, BZgA, DEBRA, LGL, Münchner Gesundheitsbefragung, Münchner Gesundheitsbericht

**Requires standard academic data-use agreement (free, no fee):**
- RKI GEDA microdata (RKI FDZ)
- RKI KiGGS Welle 2 / Baseline full microdata (RKI FDZ)
- BZgA Drogenaffinitätsstudie (GESIS agreement)
- Mikrozensus SUF (federal FDZ)
- BGS Bayern (LGL Bayern)

**Requires case-by-case negotiation or unclear access:**
- BZgA Rauchverhalten Erwachsene microdata — contact `forschung@bzga.de`
- DEBRA microdata — contact University of Leipzig PI
- Münchner Gesundheitsbefragung microdata — contact Gesundheitsreferat München
- ITC Germany — data request form at itcproject.org (signed agreement, ~2–6 weeks)

---

## Recommended Phase 1 implementation order

1. **Eurobarometer EB 458 (ZA6925) + EB 506 (ZA7780)** — free microdata via GESIS; SPSS; `pyreadstat`; Germany level; e-cigs and HTP covered. Fastest to implement.
2. **RKI GEDA 2022/2023** — flagship adult survey; aggregate tables freely available from Journal of Health Monitoring even without FDZ access; implement `fetch.py` for aggregate tables first, document FDZ path for microdata.
3. **Gesundheitsatlas Bayern** — only freely available district-level source including Munich; Excel/CSV export; critical for the geographic cascade goal.
4. **Mikrozensus GENESIS tables** (Destatis + StaBa Bayern) — free, well-structured, covers Bavaria, historical smoking trend 2009–2017.
5. **Münchner Gesundheitsbefragung PDFs** — implement PDF fetch + document microdata negotiation path with Gesundheitsreferat.

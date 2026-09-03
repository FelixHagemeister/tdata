/* Tobacco Data Gateway – deterministic question engine (browser + Node).
 * Mirrors tobacco_gateway/indicators.py. No numbers are ever generated;
 * every answer is a lookup in the harmonized dataset. */
(function (root, factory) {
  if (typeof module === "object" && module.exports) module.exports = factory();
  else root.TDG = factory();
})(typeof self !== "undefined" ? self : this, function () {
  "use strict";

  const STATES = ["Baden-Württemberg", "Bayern", "Berlin", "Brandenburg", "Bremen", "Hamburg",
    "Hessen", "Mecklenburg-Vorpommern", "Niedersachsen", "Nordrhein-Westfalen", "Rheinland-Pfalz",
    "Saarland", "Sachsen", "Sachsen-Anhalt", "Schleswig-Holstein", "Thüringen"];
  const REGIONS = ["Oberbayern", "Niederbayern", "Oberpfalz", "Oberfranken", "Mittelfranken", "Unterfranken", "Schwaben"];
  const GEO_ALIASES = [["münchen", "München"], ["muenchen", "München"], ["munich", "München"],
    ["bayern", "Bayern"], ["bavaria", "Bayern"], ["bayerisch", "Bayern"],
    ["deutschland", "Deutschland"], ["bundesweit", "Deutschland"], ["germany", "Deutschland"], ["deutsch", "Deutschland"]];
  const BREAKDOWN_KEYWORDS = {
    sex: ["geschlecht", "männer", "maenner", "frauen", "männlich", "weiblich", "mann", "frau", "gender"],
    age_group: ["alter", "altersgruppe", "altersgruppen", "jung", "jährige", "jaehrige", "age"],
    education: ["bildung", "bildungsgruppe", "bildungsstand", "abitur", "hauptschule", "education"],
    geo_name: ["bundesländer", "bundeslaender", "bundesland", "ländervergleich", "laendervergleich", "vergleich der länder", "regional", "regionen", "länder", "laender", "states"],
    year: ["zeit", "entwicklung", "trend", "verlauf", "seit", "über die jahre", "jahre", "zeitreihe", "historisch", "früher", "damals", "gesunken", "gestiegen", "rückgang", "veränderung", "over time"],
    group: ["rauchart", "familienstand", "erwerb", "schulart", "deprivation", "teilbereich", "produkt", "berufliche"],
  };
  const SEX_FILTERS = { "männer": "männlich", "maenner": "männlich", "männlich": "männlich", "mann": "männlich",
    "frauen": "weiblich", "weiblich": "weiblich", "frau": "weiblich" };
  const FAMILIES = {
    youth_smoking_current: ["youth_smoking_30d", "youth_smoking_ever"],
    youth_smoking_30d: ["youth_smoking_current", "youth_smoking_ever"],
    youth_smoking_ever: ["youth_smoking_30d", "youth_smoking_current"],
    smoking_daily: ["smoking_current"], smoking_occasional: ["smoking_current"], smoking_heavy: ["smoking_daily"],
  };
  const DIM_LABELS = { sex: "Geschlecht", age_group: "Altersgruppe", education: "Bildung", geo_name: "Bundesland", year: "Jahr", group: "Merkmal" };
  const SEX_LABEL = { gesamt: "insgesamt", "männlich": "Männer", weiblich: "Frauen" };
  const UNIT_LABELS = { percent: "%", per_100000: "je 100.000", years: "Jahre", points: "Punkte" };

  function decode(payload) {
    const cols = payload.columns, strings = payload.strings;
    return payload.rows.map(function (arr) {
      const o = {};
      cols.forEach(function (c, i) { o[c] = arr[i]; });
      ["note", "source_ref", "source_url"].forEach(function (c) { o[c] = strings[c][o[c]]; });
      ["ci_lower", "ci_upper", "n"].forEach(function (c) { if (o[c] === null) o[c] = NaN; });
      return o;
    });
  }

  function fmt(value, unit, digits) {
    if (value === null || value === undefined || Number.isNaN(value)) return "–";
    const d = digits === undefined ? 1 : digits;
    let s = Number(value).toLocaleString("de-DE", { minimumFractionDigits: d, maximumFractionDigits: d });
    if (unit !== "percent" && s.endsWith(",0")) s = s.slice(0, -2);
    return s + " " + (UNIT_LABELS[unit] || unit);
  }

  function parseQuestion(question, catalog) {
    const q = question.toLowerCase();
    const matched = [];
    let best = "smoking_current", bestLen = 0;
    Object.keys(catalog.indicators).forEach(function (ind) {
      catalog.indicators[ind].keywords.forEach(function (kw) {
        if (q.indexOf(kw) !== -1 && kw.length > bestLen) { best = ind; bestLen = kw.length; matched.push(kw); }
      });
    });
    if (best === "lung_cancer_incidence" && catalog.indicators.lung_cancer_mortality.keywords.some(function (k) { return q.indexOf(k) !== -1; })) best = "lung_cancer_mortality";
    if (best === "smoking_current" && ["jugend", "kinder", "schüler", "schueler"].some(function (k) { return q.indexOf(k) !== -1; })) {
      best = (["schüler", "schueler", "bayern"].some(function (k) { return q.indexOf(k) !== -1; })) ? "youth_smoking_30d" : "youth_smoking_current";
    }
    let geo = "Deutschland";
    for (const [alias, name] of GEO_ALIASES) { if (q.indexOf(alias) !== -1) { geo = name; matched.push(alias); break; } }
    STATES.concat(REGIONS).forEach(function (name) { if (q.indexOf(name.toLowerCase()) !== -1) { geo = name; matched.push(name); } });
    if (best === "youth_smoking_30d" || best === "youth_smoking_ever") geo = "Bayern";

    let breakdown = null;
    for (const dim of Object.keys(BREAKDOWN_KEYWORDS)) {
      if (BREAKDOWN_KEYWORDS[dim].some(function (kw) { return q.indexOf(kw) !== -1; })) { breakdown = dim; matched.push(dim); break; }
    }
    let sex = "gesamt";
    Object.keys(SEX_FILTERS).forEach(function (kw) { if (new RegExp("(^|[^a-zäöüß])" + kw + "($|[^a-zäöüß])").test(q)) sex = SEX_FILTERS[kw]; });
    if (breakdown === "sex" && sex !== "gesamt" && !["geschlecht", "vergleich", "unterschied", "und"].some(function (k) { return q.indexOf(k) !== -1; })) breakdown = null;
    if (breakdown === "sex") sex = "gesamt";
    const m = q.match(/(^|[^0-9])(19[5-9][0-9]|20[0-4][0-9])([^0-9]|$)/);
    const year = m ? parseInt(m[2], 10) : null;
    return { indicator: best, geo: geo, breakdown: breakdown, year: year, sex: sex, matched: matched };
  }

  /* Filter rows. Returns rows sorted; mirrors indicators.select(). */
  function select(rows, opts) {
    const indicator = opts.indicator, geo = opts.geo || "Deutschland", breakdown = opts.breakdown || null;
    const year = opts.year || null, sex = opts.sex || "gesamt", std = opts.standardization || "beobachtet";
    let d = rows.filter(function (r) { return r.indicator_id === indicator; });
    if (breakdown === "geo_name") d = d.filter(function (r) { return r.geo_level === "state" || r.geo_level === "germany"; });
    else d = d.filter(function (r) { return r.geo_name === geo; });
    ["sex", "age_group", "education"].forEach(function (dim) {
      if (breakdown === dim) return;
      const want = dim === "sex" ? sex : "gesamt";
      if (d.some(function (r) { return r[dim] === want; })) d = d.filter(function (r) { return r[dim] === want; });
      else if (dim === "sex") d = [];
    });
    d = breakdown === "group" ? d.filter(function (r) { return r.group_type !== ""; }) : d.filter(function (r) { return r.group_type === ""; });
    if (opts.source) d = d.filter(function (r) { return r.source_id === opts.source; });
    if (d.some(function (r) { return r.standardization === std; })) d = d.filter(function (r) { return r.standardization === std; });
    if (["sex", "age_group", "education", "group"].indexOf(breakdown) !== -1) {
      const real = new Set(d.filter(function (r) { return r[breakdown] !== "gesamt"; }).map(function (r) { return r.source_id; }));
      d = d.filter(function (r) { return real.has(r.source_id); });
    }
    if (year !== null && breakdown === "year" && d.some(function (r) { return r.year >= year; })) d = d.filter(function (r) { return r.year >= year; });
    if (year !== null && breakdown !== "year" && d.some(function (r) { return r.year === year; })) d = d.filter(function (r) { return r.year === year; });
    if (breakdown !== "year" && year === null && d.length) {
      const latest = {};
      d.forEach(function (r) { if (!(r.source_id in latest) || r.year > latest[r.source_id]) latest[r.source_id] = r.year; });
      d = d.filter(function (r) { return r.year === latest[r.source_id]; });
    }
    const key = function (r) { return [r.source_id, r.year, r.sex, r.age_group, r.education, r.group, r.geo_name].join("|"); };
    return d.slice().sort(function (a, b) { return a.source_id < b.source_id ? -1 : a.source_id > b.source_id ? 1 : a.year - b.year || (key(a) < key(b) ? -1 : 1); });
  }

  function answer(question, rows, catalog) {
    const sel = parseQuestion(question, catalog);
    const requested = sel.breakdown;
    let d = select(rows, sel);
    if (!d.length && sel.breakdown) { d = select(rows, Object.assign({}, sel, { breakdown: null })); if (d.length) sel.breakdown = null; }
    if (!d.length) {
      for (const alt of (FAMILIES[sel.indicator] || [])) {
        d = select(rows, Object.assign({}, sel, { indicator: alt }));
        if (!d.length && sel.breakdown) d = select(rows, Object.assign({}, sel, { indicator: alt, breakdown: null }));
        if (d.length) {
          sel.indicator = alt;
          if (sel.breakdown && !d.some(function (r) { return r[sel.breakdown] !== "gesamt"; })) sel.breakdown = null;
          break;
        }
      }
    }
    const meta = catalog.indicators[sel.indicator];
    if (!d.length) {
      const avail = Array.from(new Set(rows.filter(function (r) { return r.indicator_id === sel.indicator; }).map(function (r) { return r.geo_name; }))).sort();
      const hint = avail.length ? " Für „" + meta.label + "“ liegen Werte vor für: " + avail.join(", ") + "."
        : " Für diesen Indikator enthält der Datensatz noch keine Werte; der Quellenkatalog nennt Studien, die diese Frage beantworten können.";
      return { text: "Für „" + meta.label + "“ in " + sel.geo + " liegen keine Werte im Datensatz vor." + hint, rows: [], selection: sel, empty: true };
    }
    return { text: describe(sel, d, meta, requested), rows: d, selection: sel, empty: false };
  }

  function groupBy(arr, keyFn) {
    const out = new Map();
    arr.forEach(function (r) { const k = keyFn(r); if (!out.has(k)) out.set(k, []); out.get(k).push(r); });
    return out;
  }

  function describe(sel, d, meta, requested) {
    const unit = d[0].unit, parts = [];
    const multiYear = new Set(d.map(function (r) { return r.year; })).size > 1;
    if (sel.breakdown === "year" || (sel.breakdown === null && multiYear)) {
      groupBy(d, function (r) { return r.source_id; }).forEach(function (g, src) {
        g.sort(function (a, b) { return a.year - b.year; });
        const first = g[0], last = g[g.length - 1];
        if (g.length > 1) {
          const diff = Math.abs(last.value - first.value);
          parts.push(meta.label + " in " + sel.geo + " (" + SEX_LABEL[sel.sex] + "): " + fmt(first.value, unit) + " im Jahr " + first.period +
            " und " + fmt(last.value, unit) + " im Jahr " + last.period + " (" + (last.value < first.value ? "Rückgang" : "Anstieg") + " um " +
            fmt(diff, unit).replace(" %", " Prozentpunkte") + "; Quelle: " + src + ").");
        } else {
          parts.push(meta.label + " in " + sel.geo + ": " + fmt(last.value, unit) + " (" + last.period + "; Quelle: " + src + ").");
        }
      });
    } else if (sel.breakdown) {
      const col = sel.breakdown;
      groupBy(d, function (r) { return r.source_id; }).forEach(function (g, src) {
        const items = g.map(function (r) { return (r[col] === "gesamt" ? "insgesamt" : r[col]) + ": " + fmt(r.value, unit); }).join(", ");
        parts.push(meta.label + " in " + (col === "geo_name" ? "Deutschland und den Bundesländern" : sel.geo) + " nach " + DIM_LABELS[col] + " (" + g[0].period + "; Quelle: " + src + "): " + items + ".");
      });
    } else {
      d.forEach(function (r) {
        const ci = Number.isNaN(r.ci_lower) ? "" : " (95 %-KI " + fmt(r.ci_lower, unit) + " bis " + fmt(r.ci_upper, unit) + ")";
        parts.push(meta.label + " in " + r.geo_name + " (" + SEX_LABEL[r.sex] + ", " + r.period + "): " + fmt(r.value, unit) + ci + ". Quelle: " + r.source_id + ", " + r.source_ref + ".");
      });
    }
    let text = parts.join(" ");
    if (requested && sel.breakdown !== requested) {
      text = "Eine Aufschlüsselung nach " + DIM_LABELS[requested] + " liegt für " + sel.geo + " nicht vor; hier die verfügbaren Gesamtwerte. " + text;
    }
    const notes = Array.from(new Set(d.map(function (r) { return r.note; }).filter(Boolean))).sort();
    if (notes.length) text += " Hinweis: " + notes.slice(0, 3).join(" | ");
    return text;
  }

  return { decode: decode, fmt: fmt, parseQuestion: parseQuestion, select: select, answer: answer, describe: describe,
    STATES: STATES, REGIONS: REGIONS, DIM_LABELS: DIM_LABELS, SEX_LABEL: SEX_LABEL, UNIT_LABELS: UNIT_LABELS, groupBy: groupBy };
});

/* Tobacco Data Gateway – explorer UI. Depends on engine.js (window.TDG). */
(function () {
  "use strict";
  const $ = function (id) { return document.getElementById(id); };
  const SERIES = ["--series-1", "--series-2", "--series-3", "--series-4", "--series-5", "--series-6"];
  const BREAKDOWNS = [
    ["none", "Gesamtwert (neuester Stand)"], ["year", "Zeitverlauf"], ["year_sex", "Zeitverlauf nach Geschlecht"],
    ["sex", "nach Geschlecht"], ["age_group", "nach Altersgruppe"], ["education", "nach Bildung"],
    ["geo_name", "Bundesländer im Vergleich"], ["group", "weitere Merkmale"],
  ];
  const SOURCE_LABELS = {};
  let ROWS = [], CATALOG = null, SOURCES = [];
  const state = { indicator: "smoking_current", geo: "Bayern", breakdown: "none", source: "auto", year: "auto", sex: "gesamt", std: false };
  let current = { rows: [], sel: null };

  function cssVar(name) { return getComputedStyle(document.documentElement).getPropertyValue(name).trim(); }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function uniq(arr) { return Array.from(new Set(arr)); }
  function sourceLabel(id) { return SOURCE_LABELS[id] || id; }
  function catLabel(v) { return v === "gesamt" ? "insgesamt" : v; }

  /* ---------- data loading ---------- */
  Promise.all([
    fetch("data/indicators.json").then(function (r) { return r.json(); }),
    fetch("data/catalog.json").then(function (r) { return r.json(); }),
    fetch("data/sources.json").then(function (r) { return r.json(); }),
  ]).then(function (res) {
    ROWS = TDG.decode(res[0]); CATALOG = res[1]; SOURCES = res[2];
    SOURCES.forEach(function (s) { SOURCE_LABELS[s.id] = s.name; });
    $("built").textContent = CATALOG.built;
    readHash();
    initControls();
    renderSources();
    renderKpis();
    render();
    window.addEventListener("resize", debounce(render, 150));
    window.addEventListener("hashchange", function () { readHash(); syncControls(); render(); });
  }).catch(function (err) {
    $("chart").innerHTML = '<div class="empty">Daten konnten nicht geladen werden: ' + esc(err.message) + "</div>";
  });

  function debounce(fn, ms) { let t; return function () { clearTimeout(t); t = setTimeout(fn, ms); }; }

  /* ---------- state <-> URL ---------- */
  function readHash() {
    const h = location.hash.replace(/^#/, "");
    if (!h || h.indexOf("=") === -1) return;
    const p = new URLSearchParams(h);
    if (p.get("i") && CATALOG.indicators[p.get("i")]) state.indicator = p.get("i");
    if (p.get("g")) state.geo = p.get("g");
    if (p.get("b")) state.breakdown = p.get("b");
    if (p.get("src")) state.source = p.get("src");
    if (p.get("y")) state.year = p.get("y");
    if (p.get("s")) state.sex = p.get("s");
    state.std = p.get("std") === "1";
  }
  function writeHash() {
    const p = new URLSearchParams({ i: state.indicator, g: state.geo, b: state.breakdown, src: state.source, y: state.year, s: state.sex, std: state.std ? "1" : "0" });
    history.replaceState(null, "", "#" + p.toString());
  }

  /* ---------- controls ---------- */
  function fill(select, options, value) {
    select.innerHTML = "";
    let group = null;
    options.forEach(function (o) {
      if (o.group !== undefined && (!group || group.label !== o.group)) { group = document.createElement("optgroup"); group.label = o.group; select.appendChild(group); }
      const opt = document.createElement("option");
      opt.value = o.value; opt.textContent = o.label; if (o.disabled) opt.disabled = true;
      (o.group !== undefined ? group : select).appendChild(opt);
    });
    if (options.some(function (o) { return o.value === value && !o.disabled; })) select.value = value;
    else { const first = options.find(function (o) { return !o.disabled; }); select.value = first ? first.value : ""; }
    return select.value;
  }

  function geoOptions(indicator) {
    const rows = ROWS.filter(function (r) { return r.indicator_id === indicator; });
    const names = uniq(rows.map(function (r) { return r.geo_name; }));
    const level = {}; rows.forEach(function (r) { level[r.geo_name] = r.geo_level; });
    const order = { germany: 0, city: 1, state: 2, region: 3, country: 4 };
    const groupLabel = { germany: "Bund", city: "Stadt", state: "Bundesländer", region: "Regionen", country: "Länder (international)" };
    names.sort(function (a, b) {
      const pa = a === "Bayern" ? -1 : a === "München" ? -1 : order[level[a]], pb = b === "Bayern" ? -1 : b === "München" ? -1 : order[level[b]];
      return pa - pb || a.localeCompare(b, "de");
    });
    return names.map(function (n) { return { value: n, label: n, group: (n === "Bayern" || n === "München" || n === "Deutschland") ? "Schwerpunkt" : groupLabel[level[n]] }; });
  }

  function availability(indicator, geo) {
    const rows = ROWS.filter(function (r) { return r.indicator_id === indicator; });
    const here = rows.filter(function (r) { return r.geo_name === geo; });
    const has = function (dim) { return here.some(function (r) { return r[dim] !== "gesamt" && r.group_type === ""; }); };
    return {
      none: true,
      year: uniq(here.filter(function (r) { return r.group_type === ""; }).map(function (r) { return r.year; })).length > 1,
      year_sex: uniq(here.filter(function (r) { return r.group_type === "" && r.sex !== "gesamt"; }).map(function (r) { return r.year; })).length > 1,
      sex: has("sex"), age_group: has("age_group"), education: has("education"),
      geo_name: rows.some(function (r) { return r.geo_level === "state"; }),
      group: here.some(function (r) { return r.group_type !== ""; }),
    };
  }

  function initControls() {
    const inds = Object.keys(CATALOG.indicators).filter(function (id) { return ROWS.some(function (r) { return r.indicator_id === id; }); });
    fill($("sel-indicator"), inds.map(function (id) { return { value: id, label: CATALOG.indicators[id].label }; }), state.indicator);
    syncControls();
    ["sel-indicator", "sel-geo", "sel-breakdown", "sel-source", "sel-year", "sel-sex"].forEach(function (id) {
      $(id).addEventListener("change", function () {
        const key = { "sel-indicator": "indicator", "sel-geo": "geo", "sel-breakdown": "breakdown", "sel-source": "source", "sel-year": "year", "sel-sex": "sex" }[id];
        state[key] = this.value;
        if (key === "indicator" || key === "geo" || key === "breakdown") { state.source = "auto"; state.year = "auto"; }
        syncControls(); render();
      });
    });
    $("chk-std").addEventListener("change", function () { state.std = this.checked; render(); });
    $("ask-form").addEventListener("submit", function (e) { e.preventDefault(); ask($("question").value); });
    $("examples").addEventListener("click", function (e) { if (e.target.classList.contains("chip")) { $("question").value = e.target.textContent; ask(e.target.textContent); } });
    $("btn-csv").addEventListener("click", downloadCsv);
    $("btn-link").addEventListener("click", copyLink);
    $("btn-table").addEventListener("click", function () {
      const w = $("table-wrap"); w.hidden = !w.hidden;
      this.textContent = w.hidden ? "Tabelle anzeigen" : "Tabelle ausblenden"; this.setAttribute("aria-expanded", String(!w.hidden));
    });
  }

  function syncControls() {
    state.indicator = fill($("sel-indicator"), Array.from($("sel-indicator").options).map(function (o) { return { value: o.value, label: o.textContent }; }), state.indicator);
    state.geo = fill($("sel-geo"), geoOptions(state.indicator), state.geo);
    const av = availability(state.indicator, state.geo);
    state.breakdown = fill($("sel-breakdown"), BREAKDOWNS.map(function (b) { return { value: b[0], label: b[1], disabled: !av[b[0]] }; }), state.breakdown);
    const base = baseRows();
    const srcs = uniq(base.map(function (r) { return r.source_id; }));
    state.source = fill($("sel-source"), [{ value: "auto", label: "automatisch (" + srcs.length + " verfügbar)" }].concat(srcs.map(function (s) { return { value: s, label: sourceLabel(s) }; })), state.source);
    const isTime = state.breakdown === "year" || state.breakdown === "year_sex";
    $("lbl-year").hidden = isTime;
    const years = uniq(base.filter(function (r) { return state.source === "auto" || r.source_id === state.source; }).map(function (r) { return r.year; })).sort(function (a, b) { return b - a; });
    state.year = fill($("sel-year"), [{ value: "auto", label: "neuester Stand" }].concat(years.map(function (y) { return { value: String(y), label: String(y) }; })), state.year);
    $("lbl-sex").hidden = (state.breakdown === "sex" || state.breakdown === "year_sex");
    const hasStd = base.some(function (r) { return r.standardization === "altersstandardisiert"; }) && base.some(function (r) { return r.standardization === "beobachtet"; });
    $("lbl-std").hidden = !hasStd; $("chk-std").checked = state.std;
    writeHash();
  }

  /* rows for the current indicator/geo/breakdown before source/year narrowing */
  function baseRows() {
    const b = state.breakdown === "year_sex" ? "sex" : state.breakdown === "none" ? null : state.breakdown;
    let rows = ROWS.filter(function (r) { return r.indicator_id === state.indicator; });
    rows = b === "geo_name" ? rows.filter(function (r) { return r.geo_level === "state" || r.geo_level === "germany"; }) : rows.filter(function (r) { return r.geo_name === state.geo; });
    rows = b === "group" ? rows.filter(function (r) { return r.group_type !== ""; }) : rows.filter(function (r) { return r.group_type === ""; });
    ["sex", "age_group", "education"].forEach(function (dim) {
      if (dim === b) return;
      if (dim === "sex" && state.breakdown === "year_sex") return;
      const want = dim === "sex" ? state.sex : "gesamt";
      if (rows.some(function (r) { return r[dim] === want; })) rows = rows.filter(function (r) { return r[dim] === want; });
    });
    if (b && b !== "year") {
      const real = new Set(rows.filter(function (r) { return r[b] !== "gesamt"; }).map(function (r) { return r.source_id; }));
      rows = rows.filter(function (r) { return real.has(r.source_id); });
    }
    return rows;
  }

  function currentSelection() {
    const isTime = state.breakdown === "year" || state.breakdown === "year_sex";
    const sel = { indicator: state.indicator, geo: state.geo, sex: state.sex,
      breakdown: state.breakdown === "none" ? null : state.breakdown === "year_sex" ? "sex" : state.breakdown,
      year: state.year === "auto" ? null : parseInt(state.year, 10), standardization: state.std ? "altersstandardisiert" : "beobachtet" };
    let rows;
    if (state.breakdown === "year_sex") {
      rows = TDG.select(ROWS, { indicator: state.indicator, geo: state.geo, breakdown: "sex", standardization: sel.standardization, source: state.source === "auto" ? undefined : state.source, year: null });
      // select() keeps only the latest year per source; for a time series we need all years
      rows = baseRows().filter(function (r) { return (state.source === "auto" || r.source_id === state.source) && (!rows.length || r.standardization === rows[0].standardization); });
    } else {
      rows = TDG.select(ROWS, Object.assign({}, sel, { source: state.source === "auto" ? undefined : state.source }));
    }
    if (state.source === "auto" && !isTime && sel.breakdown && sel.breakdown !== "geo_name") {
      // one source per bar chart: the one with the most recent year (ties: more categories)
      const bySrc = TDG.groupBy(rows, function (r) { return r.source_id; });
      let best = null;
      bySrc.forEach(function (g, src) { const y = Math.max.apply(null, g.map(function (r) { return r.year; })); if (!best || y > best.y || (y === best.y && g.length > best.n)) best = { src: src, y: y, n: g.length }; });
      if (best) rows = rows.filter(function (r) { return r.source_id === best.src; });
    }
    if (state.source === "auto" && sel.breakdown === "geo_name") {
      const bySrc = TDG.groupBy(rows, function (r) { return r.source_id; });
      let best = null;
      bySrc.forEach(function (g, src) { const y = Math.max.apply(null, g.map(function (r) { return r.year; })); if (!best || y > best.y) best = { src: src, y: y }; });
      if (best) rows = rows.filter(function (r) { return r.source_id === best.src; });
    }
    if (state.breakdown === "year_sex" && state.source === "auto") {
      const bySrc = TDG.groupBy(rows, function (r) { return r.source_id; });
      let best = null;
      bySrc.forEach(function (g, src) { const ys = uniq(g.map(function (r) { return r.year; })).length; if (!best || ys > best.n) best = { src: src, n: ys }; });
      if (best) rows = rows.filter(function (r) { return r.source_id === best.src; });
    }
    return { sel: sel, rows: rows };
  }

  /* ---------- question ---------- */
  function ask(q) {
    if (!q.trim()) return;
    const a = TDG.answer(q, ROWS, CATALOG);
    const s = a.selection;
    state.indicator = s.indicator; state.geo = s.geo; state.sex = s.sex; state.source = "auto"; state.std = false;
    const multiYear = uniq(a.rows.map(function (r) { return r.year; })).length > 1;
    state.breakdown = s.breakdown ? s.breakdown : (multiYear ? "year" : "none");
    state.year = (s.year && s.breakdown !== "year") ? String(s.year) : "auto";
    syncControls();
    render(a.empty ? a.text : null);
    $("explorer").scrollIntoView({ behavior: "smooth", block: "start" });
  }

  /* ---------- rendering ---------- */
  function render(overrideText) {
    const cur = currentSelection();
    current = cur;
    const meta = CATALOG.indicators[state.indicator];
    const rows = cur.rows;
    const descSel = Object.assign({}, cur.sel, { breakdown: state.breakdown === "year" || state.breakdown === "year_sex" ? "year" : cur.sel.breakdown });
    let text = overrideText || (rows.length ? TDG.describe(descSel, rows, meta, null) : "Für diese Auswahl liegen keine Werte vor. Bitte Gebiet oder Darstellung ändern.");
    if (state.breakdown === "year_sex" && rows.length) text = describeYearSex(rows, meta);
    $("answer-text").innerHTML = esc(text).replace(/Hinweis: /, '<br><span class="muted small">Hinweis: ') + (text.indexOf("Hinweis: ") !== -1 ? "</span>" : "");
    $("chart-title").textContent = meta.label;
    const srcs = uniq(rows.map(function (r) { return r.source_id; }));
    const periods = uniq(rows.map(function (r) { return r.period; })).sort();
    $("chart-sub").textContent = rows.length ? [state.breakdown === "geo_name" ? "Deutschland und Bundesländer" : state.geo,
      (state.breakdown === "year" || state.breakdown === "year_sex") ? periods[0] + " bis " + periods[periods.length - 1] : periods.join(", "),
      (state.breakdown === "sex" || state.breakdown === "year_sex") ? "" : TDG.SEX_LABEL[state.sex],
      rows[0].standardization === "altersstandardisiert" ? "altersstandardisiert" : "",
      "Quelle: " + srcs.map(sourceLabel).join("; ")].filter(Boolean).join(" · ") : "";
    $("chart-note").textContent = rows.length ? meta.population + "." : "";
    drawChart(rows);
    renderTable(rows);
  }

  function describeYearSex(rows, meta) {
    const parts = [];
    TDG.groupBy(rows, function (r) { return r.sex; }).forEach(function (g, sex) {
      g.sort(function (a, b) { return a.year - b.year; });
      const f = g[0], l = g[g.length - 1];
      parts.push(TDG.SEX_LABEL[sex] + ": " + TDG.fmt(f.value, f.unit) + " (" + f.period + ") → " + TDG.fmt(l.value, l.unit) + " (" + l.period + ")");
    });
    return meta.label + " in " + state.geo + " im Zeitverlauf nach Geschlecht – " + parts.join("; ") + ". Quelle: " + uniq(rows.map(function (r) { return r.source_id; })).map(sourceLabel).join("; ") + ".";
  }

  function drawChart(rows) {
    const el = $("chart"); el.innerHTML = ""; $("legend").innerHTML = "";
    if (!rows.length) { el.innerHTML = '<div class="empty">Keine Daten für diese Auswahl.</div>'; return; }
    const isTime = state.breakdown === "year" || state.breakdown === "year_sex";
    if (isTime) drawLines(el, rows);
    else if (state.breakdown === "none") drawStats(el, rows);
    else drawBars(el, rows);
  }

  function svgEl(tag, attrs, parent) {
    const e = document.createElementNS("http://www.w3.org/2000/svg", tag);
    Object.keys(attrs || {}).forEach(function (k) { e.setAttribute(k, attrs[k]); });
    if (parent) parent.appendChild(e);
    return e;
  }
  function niceMax(v) {
    if (v <= 0) return 1;
    const p = Math.pow(10, Math.floor(Math.log10(v)));
    const n = v / p;
    const steps = [1, 1.2, 1.5, 2, 2.5, 3, 4, 5, 6, 8, 10];
    const m = steps.find(function (s) { return n <= s + 1e-9; }) || 10;
    return m * p;
  }
  function ticks(max, count) {
    const candidates = [1, 2, 2.5, 5, 10, 20, 25, 50, 100, 200, 250, 500, 1000];
    const step = candidates.find(function (s) { return max / s <= count; }) || Math.pow(10, Math.ceil(Math.log10(max / count)));
    const out = []; for (let v = 0; v <= max + 1e-9; v += step) out.push(+v.toFixed(6)); return out;
  }

  function showTip(evt, html) { const t = $("tooltip"); t.innerHTML = html; t.hidden = false; moveTip(evt); }
  function moveTip(evt) { const t = $("tooltip"); const x = Math.min(evt.clientX + 14, window.innerWidth - t.offsetWidth - 8); t.style.left = x + "px"; t.style.top = (evt.clientY + 14) + "px"; }
  function hideTip() { $("tooltip").hidden = true; }
  function rowTip(r) {
    const ci = Number.isNaN(r.ci_lower) ? "" : "<br>95 %-KI " + TDG.fmt(r.ci_lower, r.unit) + " – " + TDG.fmt(r.ci_upper, r.unit);
    const dims = [r.geo_name, r.period, TDG.SEX_LABEL[r.sex], r.age_group !== "gesamt" ? r.age_group : "", r.education !== "gesamt" ? "Bildung " + r.education : "", r.group].filter(Boolean).join(" · ");
    return "<b>" + esc(TDG.fmt(r.value, r.unit)) + "</b>" + esc(dims) + ci + "<br>" + esc(sourceLabel(r.source_id)) + (r.n ? " · n = " + Number(r.n).toLocaleString("de-DE") : "");
  }

  /* Horizontal bars: one hue; Bayern/München emphasised, Deutschland as reference */
  function drawBars(el, rows) {
    const dim = state.breakdown;
    const unit = rows[0].unit;
    let items = rows.map(function (r) { return { label: dim === "group" ? r.group : catLabel(r[dim]), r: r }; });
    if (dim === "geo_name") items.sort(function (a, b) { return b.r.value - a.r.value; });
    else if (dim === "sex") items.sort(function (a, b) { return ["gesamt", "männlich", "weiblich"].indexOf(a.r.sex) - ["gesamt", "männlich", "weiblich"].indexOf(b.r.sex); });
    else if (dim === "education") items.sort(function (a, b) { return ["gesamt", "niedrig", "mittel", "hoch"].indexOf(a.r.education) - ["gesamt", "niedrig", "mittel", "hoch"].indexOf(b.r.education); });
    const width = Math.max(320, el.getBoundingClientRect().width), labelW = Math.min(width * 0.4, Math.max(90, Math.max.apply(null, items.map(function (i) { return i.label.length; })) * 8.2 + 14));
    const barH = 20, gap = 8, padT = 8, padB = 28, padR = 70;
    const height = padT + items.length * (barH + gap) + padB;
    const svg = svgEl("svg", { viewBox: "0 0 " + width + " " + height, width: width, height: height, role: "img", "aria-label": "Balkendiagramm" }, el);
    const max = niceMax(Math.max.apply(null, items.map(function (i) { return Number.isNaN(i.r.ci_upper) ? i.r.value : Math.max(i.r.value, i.r.ci_upper); })) * 1.02);
    const x = function (v) { return labelW + (v / max) * (width - labelW - padR); };
    const grid = svgEl("g", { class: "grid" }, svg);
    ticks(max, width < 560 ? 3 : 5).forEach(function (t) {
      svgEl("line", { x1: x(t), x2: x(t), y1: padT, y2: height - padB + 4 }, grid);
      const tx = svgEl("text", { x: x(t), y: height - 8, "text-anchor": "middle", class: "label" }, svg); tx.textContent = TDG.fmt(t, unit, 0).replace(" je 100.000", "");
    });
    const accent = cssVar("--series-1"), mutedMark = cssVar("--muted-mark"), ref = cssVar("--reference");
    items.forEach(function (it, i) {
      const y = padT + i * (barH + gap);
      const r = it.r;
      let fill = accent;
      if (dim === "geo_name") fill = (r.geo_name === "Bayern") ? accent : (r.geo_name === "Deutschland" ? ref : mutedMark);
      else if (r[dim] === "gesamt") fill = ref;
      const w = Math.max(0, x(r.value) - labelW);
      const cat = svgEl("text", { x: labelW - 8, y: y + barH / 2 + 4, "text-anchor": "end", class: "cat" }, svg); cat.textContent = it.label;
      if (dim === "geo_name" && (r.geo_name === "Bayern" || r.geo_name === "Deutschland")) cat.setAttribute("font-weight", "600");
      svgEl("path", { d: roundedRight(labelW, y, w, barH, 4), fill: fill }, svg);
      if (!Number.isNaN(r.ci_lower)) svgEl("line", { x1: x(r.ci_lower), x2: x(r.ci_upper), y1: y + barH / 2, y2: y + barH / 2, stroke: "var(--text)", "stroke-opacity": ".45", "stroke-width": 1.5 }, svg);
      const val = svgEl("text", { x: x(Number.isNaN(r.ci_upper) ? r.value : Math.max(r.value, r.ci_upper)) + 6, y: y + barH / 2 + 4, class: "value" }, svg); val.textContent = TDG.fmt(r.value, unit).replace(" je 100.000", "");
      const hit = svgEl("rect", { x: 0, y: y - gap / 2, width: width, height: barH + gap, class: "hit" }, svg);
      hit.addEventListener("mousemove", function (e) { showTip(e, rowTip(r)); });
      hit.addEventListener("mouseleave", hideTip);
    });
    if (dim === "geo_name") legend([["Bayern", accent], ["Deutschland (Referenz)", ref], ["andere Bundesländer", mutedMark]]);
  }
  function roundedRight(x, y, w, h, r) {
    r = Math.min(r, w / 2, h / 2);
    return "M" + x + "," + y + " h" + (w - r) + " a" + r + "," + r + " 0 0 1 " + r + "," + r + " v" + (h - 2 * r) + " a" + r + "," + r + " 0 0 1 " + (-r) + "," + r + " h" + (-(w - r)) + " z";
  }

  /* Lines: series = sources (Zeitverlauf) or sexes (Zeitverlauf nach Geschlecht) */
  function drawLines(el, rows) {
    const unit = rows[0].unit;
    const bySex = state.breakdown === "year_sex";
    const seriesMap = TDG.groupBy(rows, function (r) { return bySex ? r.sex : r.source_id; });
    let keys = Array.from(seriesMap.keys());
    if (bySex) keys.sort(function (a, b) { return ["gesamt", "männlich", "weiblich"].indexOf(a) - ["gesamt", "männlich", "weiblich"].indexOf(b); });
    else keys.sort(function (a, b) { return Math.min.apply(null, seriesMap.get(a).map(function (r) { return r.year; })) - Math.min.apply(null, seriesMap.get(b).map(function (r) { return r.year; })); });
    const width = Math.max(320, el.getBoundingClientRect().width), height = Math.min(380, Math.max(240, width * 0.42));
    const padL = 48, padR = width < 560 ? 90 : 130, padT = 12, padB = 32;
    const years = uniq(rows.map(function (r) { return r.year; })).sort(function (a, b) { return a - b; });
    const y0 = years[0], y1 = years[years.length - 1] === y0 ? y0 + 1 : years[years.length - 1];
    const max = niceMax(Math.max.apply(null, rows.map(function (r) { return Number.isNaN(r.ci_upper) ? r.value : Math.max(r.value, r.ci_upper); })) * 1.05);
    const x = function (yr) { return padL + (yr - y0) / (y1 - y0) * (width - padL - padR); };
    const y = function (v) { return padT + (1 - v / max) * (height - padT - padB); };
    const svg = svgEl("svg", { viewBox: "0 0 " + width + " " + height, width: width, height: height, role: "img", "aria-label": "Liniendiagramm" }, el);
    const grid = svgEl("g", { class: "grid" }, svg);
    ticks(max, width < 560 ? 3 : 4).forEach(function (t) {
      svgEl("line", { x1: padL, x2: width - padR, y1: y(t), y2: y(t) }, grid);
      const tx = svgEl("text", { x: padL - 8, y: y(t) + 4, "text-anchor": "end", class: "label" }, svg); tx.textContent = TDG.fmt(t, unit, 0).replace(" je 100.000", "");
    });
    const span = y1 - y0, step = span > 40 ? 10 : span > 16 ? 5 : span > 8 ? 2 : 1;
    for (let yr = Math.ceil(y0 / step) * step; yr <= y1; yr += step) { const tx = svgEl("text", { x: x(yr), y: height - 10, "text-anchor": "middle", class: "label" }, svg); tx.textContent = yr; }
    svgEl("line", { x1: padL, x2: width - padR, y1: y(0), y2: y(0), stroke: "var(--text-3)" }, svg);
    const colors = keys.map(function (k, i) { return cssVar(SERIES[i % SERIES.length]); });
    const labelSlots = [];
    keys.forEach(function (k, i) {
      const pts = seriesMap.get(k).slice().sort(function (a, b) { return a.year - b.year; });
      const color = colors[i];
      if (pts.length > 1) svgEl("path", { d: pts.map(function (p, j) { return (j ? "L" : "M") + x(p.year) + "," + y(p.value); }).join(" "), fill: "none", stroke: color, "stroke-width": 2, "stroke-linejoin": "round" }, svg);
      pts.forEach(function (p) {
        svgEl("circle", { cx: x(p.year), cy: y(p.value), r: 4.5, fill: color, stroke: "var(--surface)", "stroke-width": 2 }, svg);
        const hit = svgEl("circle", { cx: x(p.year), cy: y(p.value), r: 12, class: "hit" }, svg);
        hit.addEventListener("mousemove", function (e) { showTip(e, rowTip(p)); });
        hit.addEventListener("mouseleave", hideTip);
      });
      const last = pts[pts.length - 1];
      let ly = y(last.value);
      labelSlots.sort(function (a, b) { return a - b; });
      labelSlots.forEach(function (s) { if (Math.abs(s - ly) < 14) ly = s + 14; });
      labelSlots.push(ly);
      const lab = svgEl("text", { x: x(last.year) + 10, y: ly + 4, class: "value" }, svg);
      lab.textContent = (bySex ? TDG.SEX_LABEL[k] : shortSource(k)) + " " + TDG.fmt(last.value, unit).replace(" je 100.000", "");
    });
    if (keys.length > 1) legend(keys.map(function (k, i) { return [bySex ? TDG.SEX_LABEL[k] : sourceLabel(k), colors[i]]; }));
    else if (!bySex) legend([[sourceLabel(keys[0]), colors[0]]]);
  }
  function shortSource(id) { return { destatis_mikrozensus: "Mikrozensus", rki_gbe_ncd: "RKI GBE", rki_diabetes_surveillance: "RKI GEDA", bgs_bayern: "LGL Bayern", muenchen_gesundheitsbefragung: "LHM" }[id] || id; }

  /* Stat tiles: one per row (latest value per source) */
  function drawStats(el, rows) {
    const wrap = document.createElement("div"); wrap.className = "kpis"; wrap.style.marginTop = "4px";
    rows.forEach(function (r) {
      const d = document.createElement("div"); d.className = "kpi"; d.style.cursor = "default";
      const ci = Number.isNaN(r.ci_lower) ? "" : " (95 %-KI " + TDG.fmt(r.ci_lower, r.unit) + "–" + TDG.fmt(r.ci_upper, r.unit) + ")";
      d.innerHTML = '<div class="v">' + esc(TDG.fmt(r.value, r.unit)) + '</div><div class="l">' + esc([r.geo_name, TDG.SEX_LABEL[r.sex], r.age_group !== "gesamt" ? r.age_group : "", r.period].filter(Boolean).join(" · ")) + '</div><div class="s">' + esc(sourceLabel(r.source_id) + ci) + "</div>";
      d.addEventListener("mousemove", function (e) { showTip(e, rowTip(r)); }); d.addEventListener("mouseleave", hideTip);
      wrap.appendChild(d);
    });
    el.appendChild(wrap);
  }

  function legend(items) {
    $("legend").innerHTML = items.map(function (it) { return "<span><i style=\"background:" + it[1] + "\"></i>" + esc(it[0]) + "</span>"; }).join("");
  }

  function renderTable(rows) {
    const thead = $("table").querySelector("thead"), tbody = $("table").querySelector("tbody");
    thead.innerHTML = "<tr><th>Gebiet</th><th>Zeitraum</th><th>Geschlecht</th><th>Alter</th><th>Bildung</th><th>Merkmal</th><th class=\"num\">Wert</th><th class=\"num\">95 %-KI</th><th class=\"num\">n</th><th>Quelle</th><th>Beleg</th></tr>";
    tbody.innerHTML = rows.map(function (r) {
      const ci = Number.isNaN(r.ci_lower) ? "" : TDG.fmt(r.ci_lower, r.unit, 1).replace(/ .*$/, "") + "–" + TDG.fmt(r.ci_upper, r.unit, 1).replace(/ .*$/, "");
      return "<tr><td>" + esc(r.geo_name) + "</td><td>" + esc(r.period) + "</td><td>" + esc(TDG.SEX_LABEL[r.sex]) + "</td><td>" + esc(catLabel(r.age_group)) + "</td><td>" + esc(catLabel(r.education)) + "</td><td>" + esc(r.group_type ? r.group_type + ": " + r.group : "") +
        "</td><td class=\"num\">" + esc(TDG.fmt(r.value, r.unit)) + (r.standardization === "altersstandardisiert" ? " *" : "") + "</td><td class=\"num\">" + ci + "</td><td class=\"num\">" + (r.n ? Number(r.n).toLocaleString("de-DE") : "") +
        "</td><td>" + (r.source_url ? '<a href="' + esc(r.source_url) + '" rel="noopener">' + esc(sourceLabel(r.source_id)) + "</a>" : esc(sourceLabel(r.source_id))) + "</td><td class=\"note\" title=\"" + esc(r.note) + "\">" + esc(r.source_ref) + "</td></tr>";
    }).join("");
    const notes = uniq(rows.map(function (r) { return r.note; }).filter(Boolean));
    let foot = notes.map(function (n) { return "<div>" + esc(n) + "</div>"; }).join("");
    if (rows.some(function (r) { return r.standardization === "altersstandardisiert"; })) foot += "<div>* altersstandardisiert</div>";
    if (foot) tbody.innerHTML += "<tr><td colspan=\"11\" class=\"foot\">" + foot + "</td></tr>";
  }

  function downloadCsv() {
    const rows = current.rows; if (!rows.length) return;
    const cols = CATALOG.columns;
    const lines = [cols.join(",")].concat(rows.map(function (r) { return cols.map(function (c) { let v = r[c]; if (v === null || v === undefined || (typeof v === "number" && Number.isNaN(v))) v = ""; v = String(v); return /[",\n]/.test(v) ? '"' + v.replace(/"/g, '""') + '"' : v; }).join(","); }));
    const blob = new Blob(["﻿" + lines.join("\n")], { type: "text/csv;charset=utf-8" });
    const a = document.createElement("a"); a.href = URL.createObjectURL(blob); a.download = "tobacco_" + state.indicator + "_" + state.geo.replace(/[^A-Za-z0-9]/g, "_") + ".csv"; document.body.appendChild(a); a.click(); a.remove();
  }
  function copyLink() {
    const url = location.href;
    const done = function () { $("btn-link").textContent = "Link kopiert"; setTimeout(function () { $("btn-link").textContent = "Link kopieren"; }, 1500); };
    if (navigator.clipboard) navigator.clipboard.writeText(url).then(done, function () { prompt("Link", url); });
    else prompt("Link", url);
  }

  /* ---------- KPI row (hero) ---------- */
  function renderKpis() {
    const wants = [
      { i: "smoking_current", g: "München", l: "rauchen in München" },
      { i: "smoking_current", g: "Bayern", l: "rauchen in Bayern" },
      { i: "smoking_current", g: "Deutschland", l: "rauchen in Deutschland" },
      { i: "lung_cancer_mortality", g: "Bayern", l: "Lungenkrebs-Sterbefälle je 100.000 in Bayern" },
    ];
    const html = wants.map(function (w) {
      const rows = TDG.select(ROWS, { indicator: w.i, geo: w.g });
      if (!rows.length) return "";
      const r = rows.reduce(function (a, b) { return b.year > a.year ? b : a; });
      return '<button type="button" class="kpi" data-i="' + w.i + '" data-g="' + w.g + '"><div class="v">' + esc(TDG.fmt(r.value, r.unit).replace(" je 100.000", "")) + '</div><div class="l">' + esc(w.l) + '</div><div class="s">' + esc(r.period + " · " + sourceLabel(r.source_id)) + "</div></button>";
    }).join("");
    $("kpis").innerHTML = html;
    $("kpis").addEventListener("click", function (e) {
      const b = e.target.closest(".kpi"); if (!b) return;
      state.indicator = b.dataset.i; state.geo = b.dataset.g; state.breakdown = "year"; state.source = "auto"; state.year = "auto"; state.sex = "gesamt";
      syncControls(); render(); $("explorer").scrollIntoView({ behavior: "smooth" });
    });
  }

  /* ---------- sources ---------- */
  function renderSources() {
    const geoLabel = { munich: "München", bavaria: "Bayern", germany: "Deutschland", europe: "Europa" };
    $("sources").innerHTML = SOURCES.map(function (s) {
      const years = Array.isArray(s.years_available) ? (s.years_available.length > 4 ? s.years_available[0] + "–" + s.years_available[s.years_available.length - 1] : s.years_available.join(", ")) : (s.years_available || "");
      const qs = (s.sample_questions || []).slice(0, 2).map(function (q) { return "<div class=\"q\">„" + esc(q) + "“</div>"; }).join("");
      return '<article class="card source"><div><span class="badge ' + (s.in_dataset ? "good" : "") + '">' + (s.in_dataset ? "im Datensatz · " + s.dataset_rows + " Werte" : "dokumentiert") + "</span></div><h3>" + esc(s.name) + '</h3><div class="prov">' + esc(s.provider || "") + "</div><dl>" +
        "<dt>Gebiet</dt><dd>" + esc(geoLabel[s.geographic_level] || s.geographic_level || "") + "</dd><dt>Jahre</dt><dd>" + esc(years) + "</dd><dt>Zugang</dt><dd>" + esc((s.access_method || "").replace(/_/g, " ")) + (s.license ? " · " + esc(s.license) : "") + "</dd><dt>Format</dt><dd>" + esc(s.data_format || "") + "</dd></dl>" + qs +
        (s.url ? '<div><a href="' + esc(s.url) + '" rel="noopener">Zur Quelle</a> · <a href="https://github.com/FelixHagemeister/tdata/blob/main/sources/' + esc(s.id) + '/SOURCE.md" rel="noopener">SOURCE.md</a></div>' : "") + "</article>";
    }).join("");
  }
})();

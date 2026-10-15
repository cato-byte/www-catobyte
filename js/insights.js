// Insights page: charts and map drawn from the JSON the lakehouse pipeline publishes.
//
// The page ships the narrative as HTML; every element with data-viz="<name>" is filled in here
// from the files under the page's data-src (written by the pipeline's publish task, so the page
// shows the latest run without a site rebuild). Elements with data-stat="<name>" get a figure
// from the same data, so the text never goes stale. No libraries except Leaflet for the map.

(() => {
  "use strict";

  const root = document.querySelector("[data-insights]");
  if (!root) return;

  const T = JSON.parse(document.getElementById("insights-i18n").textContent);
  const lang = document.documentElement.lang || "en";
  const BASE = root.dataset.src.replace(/\/?$/, "/");
  const COUNTRIES = ["FR", "GB", "IE", "NO", "EE", "ES"];
  const SECTIONS = "ABCDEFGHIJKLMNOPQRSTU".split("");

  // ---- formatting ---------------------------------------------------------------------------
  const nf = new Intl.NumberFormat(lang);
  const nfCompact = new Intl.NumberFormat(lang, { notation: "compact", maximumFractionDigits: 1 });
  const fmt = (n) => (n == null ? "—" : nf.format(Math.round(n)));
  const compact = (n) => (n == null ? "—" : nfCompact.format(n));
  const pct = (x, digits = 1) =>
    x == null ? "—" : new Intl.NumberFormat(lang, { style: "percent", maximumFractionDigits: digits, minimumFractionDigits: digits }).format(x);
  const country = (cc) => T.countries[cc] || cc;
  const section = (s) => (s && T.sections[s]) || T.labels.unclassified;

  // Registers publish towns in capitals; show them in title case (particles stay lower case).
  const PARTICLES = new Set(["de", "du", "des", "la", "le", "les", "sur", "en", "et", "of", "on", "upon", "the", "y"]);
  function titleCase(text) {
    if (!text) return "";
    return text.toLowerCase().replace(/[^\s\-']+/g, (word, offset) =>
      offset > 0 && PARTICLES.has(word) ? word : word.charAt(0).toUpperCase() + word.slice(1));
  }

  // Fishing jobs are reported per French département (codes) and Norwegian municipality (names).
  const DEPARTEMENTS = {
    "14": "Calvados", "17": "Charente-Maritime", "22": "Côtes-d'Armor", "29": "Finistère", "33": "Gironde",
    "34": "Hérault", "35": "Ille-et-Vilaine", "44": "Loire-Atlantique", "50": "Manche", "56": "Morbihan",
    "62": "Pas-de-Calais", "64": "Pyrénées-Atlantiques", "76": "Seine-Maritime", "85": "Vendée",
  };
  const regionName = (r) =>
    r.country_code === "FR" ? (r.region === "97" ? T.labels.overseas : `${DEPARTEMENTS[r.region] || r.region} (${r.region})`)
                            : titleCase(r.region);

  // ---- tiny DOM helpers -----------------------------------------------------------------------
  function h(tag, attrs = {}, ...children) {
    const node = document.createElement(tag);
    for (const [key, value] of Object.entries(attrs)) {
      if (value == null || value === false) continue;
      if (key === "class") node.className = value;
      else if (key === "text") node.textContent = value;
      else if (key === "style") node.setAttribute("style", value);
      else if (key.startsWith("on")) node.addEventListener(key.slice(2), value);
      else node.setAttribute(key, value === true ? "" : value);
    }
    for (const child of children.flat()) if (child != null) node.append(child.nodeType ? child : String(child));
    return node;
  }
  const SVG_NS = "http://www.w3.org/2000/svg";
  function s(tag, attrs = {}) {
    const node = document.createElementNS(SVG_NS, tag);
    for (const [key, value] of Object.entries(attrs)) if (value != null) node.setAttribute(key, value);
    return node;
  }

  // ---- tooltip (one for the page) ---------------------------------------------------------------
  const tip = h("div", { class: "viz-tip", role: "status", hidden: true });
  document.body.append(tip);
  function showTip(html, x, y) {
    tip.innerHTML = html;
    tip.hidden = false;
    const pad = 12;
    const { width, height } = tip.getBoundingClientRect();
    let left = x + pad;
    let top = y + pad;
    if (left + width > window.innerWidth - 8) left = x - width - pad;
    if (top + height > window.innerHeight - 8) top = y - height - pad;
    tip.style.left = `${Math.max(8, left)}px`;
    tip.style.top = `${Math.max(8, top)}px`;
  }
  const hideTip = () => { tip.hidden = true; };
  const esc = (text) => String(text).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));

  // Hover and keyboard focus both show the mark's tooltip.
  function attachTip(node, html) {
    node.setAttribute("tabindex", "0");
    node.addEventListener("pointermove", (e) => showTip(html(), e.clientX, e.clientY));
    node.addEventListener("pointerleave", hideTip);
    node.addEventListener("focus", () => {
      const r = node.getBoundingClientRect();
      showTip(html(), r.left + r.width / 2, r.bottom);
    });
    node.addEventListener("blur", hideTip);
  }

  // ---- figure shell: title, controls, chart, note, optional table view ---------------------------
  function figure(container, { title, note, controls, table }) {
    container.replaceChildren();
    container.classList.add("viz");
    const head = h("div", { class: "viz-head" });
    if (title) head.append(h("p", { class: "viz-title", text: title }));
    if (controls) head.append(controls);
    const body = h("div", { class: "viz-body" });
    container.append(head, body);
    if (note) container.append(h("p", { class: "viz-note", text: note }));
    if (table) {
      const wrap = h("div", { class: "table-wrap viz-table", hidden: true });
      const button = h("button", { type: "button", class: "viz-toggle", "aria-expanded": "false" }, T.labels.show_table);
      button.addEventListener("click", () => {
        const open = wrap.hidden;
        if (open) wrap.replaceChildren(buildTable(table()));
        wrap.hidden = !open;
        button.setAttribute("aria-expanded", String(open));
        button.textContent = open ? T.labels.hide_table : T.labels.show_table;
      });
      container.append(button, wrap);
    }
    return body;
  }

  function buildTable({ head, rows }) {
    return h("table", {},
      h("thead", {}, h("tr", {}, head.map((cell) => h("th", { scope: "col" }, cell)))),
      h("tbody", {}, rows.map((row) => h("tr", {}, row.map((cell, i) => h(i ? "td" : "th", i ? { class: "num" } : { scope: "row" }, cell))))));
  }

  // Segmented control (radio buttons styled as pills).
  let controlId = 0;
  function segmented(options, value, onChange, label) {
    const name = `seg-${++controlId}`;
    const group = h("div", { class: "segmented", role: "radiogroup", "aria-label": label });
    for (const [key, text] of options) {
      const id = `${name}-${key}`;
      const input = h("input", { type: "radio", name, id, value: key, checked: key === value });
      input.addEventListener("change", () => onChange(key));
      group.append(input, h("label", { for: id, text }));
    }
    return group;
  }

  // ---- bar rows (horizontal bars, label | bar | value) -------------------------------------------
  // Each row: {label, sub, value, low, high, tip, segments:[{value, cls}]}. A row with low/high draws
  // a range (banded headcounts); value null means "not published", never zero.
  function barRows(body, rows, { max, format = fmt, series } = {}) {
    const peak = max || Math.max(...rows.map((r) => r.high ?? r.value ?? 0), 1e-9);
    const list = h("ul", { class: "bars" });
    for (const row of rows) {
      const track = h("span", { class: "bars-track" });
      if (row.values) {
        // Two thin bars on the same scale (e.g. two rates), stacked vertically inside the row.
        row.values.forEach((v, i) => track.append(h("span", {
          class: `bars-fill bars-fill-${i + 1}${row.values.length > 1 ? " bars-thin" : ""}`, style: `width:${((v ?? 0) / peak) * 100}%`,
        })));
      } else if (row.value == null && row.low == null) {
        track.append(h("span", { class: "bars-na", text: T.labels.not_published }));
      } else if (row.low != null && row.high != null && row.high !== row.low) {
        track.append(h("span", { class: "bars-fill", style: `width:${(row.low / peak) * 100}%` }));
        track.append(h("span", { class: "bars-range", style: `left:${(row.low / peak) * 100}%;width:${((row.high - row.low) / peak) * 100}%` }));
      } else {
        track.append(h("span", { class: `bars-fill${row.highlight ? " is-highlight" : ""}`, style: `width:${(row.value / peak) * 100}%` }));
      }
      const item = h("li", {},
        h("span", { class: "bars-label" }, row.label, row.sub ? h("small", { text: row.sub }) : null),
        track,
        h("span", { class: "bars-value", text: row.display ?? (row.value == null && row.low == null && !row.values ? "—" : format(row.value ?? row.low)) }));
      if (row.tip) attachTip(item, row.tip);
      list.append(item);
    }
    body.append(list);
    if (series) body.append(legend(series));
  }

  function legend(series) {
    return h("ul", { class: "viz-legend" }, series.map(([cls, text]) =>
      h("li", {}, h("span", { class: `swatch ${cls}`, "aria-hidden": "true" }), text)));
  }

  // ---- line chart (SVG, one y axis, crosshair tooltip) -------------------------------------------
  function lineChart(body, { series, xDomain, yMax, yFormat = fmt, xFormat = String, height = 220, labels = true, showLegend = true }) {
    // Draw at the container's real width so axis text keeps its size on phones.
    const width = Math.max(280, Math.round(body.getBoundingClientRect().width) || 640);
    const m = { top: 12, right: labels ? 40 : 12, bottom: 26, left: 44 };
    const iw = width - m.left - m.right;
    const ih = height - m.top - m.bottom;
    const [x0, x1] = xDomain;
    const x = (v) => m.left + ((v - x0) / Math.max(1, x1 - x0)) * iw;
    const y = (v) => m.top + ih - (v / yMax) * ih;

    const svg = s("svg", { viewBox: `0 0 ${width} ${height}`, class: "line-chart", role: "img", "aria-label": series.map((d) => d.name).join(", ") });
    for (let i = 0; i <= 4; i++) {
      const v = (yMax / 4) * i;
      svg.append(s("line", { x1: m.left, x2: m.left + iw, y1: y(v), y2: y(v), class: "grid" }));
      const label = s("text", { x: m.left - 8, y: y(v) + 4, class: "axis", "text-anchor": "end" });
      label.textContent = yFormat(v);
      svg.append(label);
    }
    const step = Math.max(1, Math.ceil((x1 - x0) / (width < 480 ? 4 : 6)));
    for (let v = x0; v <= x1; v += step) {
      const label = s("text", { x: x(v), y: height - 6, class: "axis", "text-anchor": "middle" });
      label.textContent = xFormat(v);
      svg.append(label);
    }
    series.forEach((d) => {
      const pts = d.points.filter((p) => p[1] != null);
      if (!pts.length) return;
      // Break the line where a value is missing instead of bridging the gap.
      let path = "";
      let pen = false;
      for (const [px, py] of d.points) {
        if (py == null) { pen = false; continue; }
        path += `${pen ? "L" : "M"}${x(px).toFixed(1)},${y(py).toFixed(1)}`;
        pen = true;
      }
      svg.append(s("path", { d: path, class: `line ${d.cls}`, ...(d.dashed ? { "stroke-dasharray": "5 4" } : {}) }));
      if (labels) {
        const [lx, ly] = pts[pts.length - 1];
        const t = s("text", { x: x(lx) + 6, y: y(ly) + 4, class: "line-label" });
        t.textContent = d.short || d.name;
        svg.append(t);
      }
    });

    // Crosshair: nearest x, every series' value at that x.
    const cross = s("line", { y1: m.top, y2: m.top + ih, class: "crosshair", visibility: "hidden" });
    const dots = series.map((d) => s("circle", { r: 4, class: `dot ${d.cls}`, visibility: "hidden" }));
    svg.append(cross, ...dots);
    const hit = s("rect", { x: m.left, y: m.top, width: iw, height: ih, fill: "transparent", tabindex: 0 });
    svg.append(hit);
    function at(clientX, clientY) {
      const box = svg.getBoundingClientRect();
      const px = ((clientX - box.left) / box.width) * width;
      const xv = Math.round(x0 + ((px - m.left) / iw) * (x1 - x0));
      if (xv < x0 || xv > x1) return hideAll();
      cross.setAttribute("x1", x(xv));
      cross.setAttribute("x2", x(xv));
      cross.setAttribute("visibility", "visible");
      const lines = [];
      series.forEach((d, i) => {
        const point = d.points.find((p) => p[0] === xv);
        if (point && point[1] != null) {
          dots[i].setAttribute("cx", x(xv));
          dots[i].setAttribute("cy", y(point[1]));
          dots[i].setAttribute("visibility", "visible");
          lines.push(`<span class="swatch ${d.cls}"></span>${esc(d.name)}: <b>${esc(yFormat(point[1]))}</b>`);
        } else dots[i].setAttribute("visibility", "hidden");
      });
      showTip(`<strong>${esc(xFormat(xv))}</strong><br>${lines.join("<br>") || T.labels.not_published}`, clientX, clientY);
    }
    function hideAll() {
      cross.setAttribute("visibility", "hidden");
      dots.forEach((d) => d.setAttribute("visibility", "hidden"));
      hideTip();
    }
    hit.addEventListener("pointermove", (e) => at(e.clientX, e.clientY));
    hit.addEventListener("pointerleave", hideAll);
    body.append(svg);
    if (showLegend && series.length > 1) body.append(legend(series.map((d) => [d.cls, d.name])));
  }

  // ---- data -------------------------------------------------------------------------------------
  async function getJSON(name) {
    const response = await fetch(BASE + name, { cache: "no-cache" });
    if (!response.ok) throw new Error(`${name}: HTTP ${response.status}`);
    return response.json();
  }
  const sum = (obj) => Object.values(obj || {}).reduce((a, b) => a + b, 0);
  const byCountry = (rows) => Object.fromEntries(COUNTRIES.map((cc) => [cc, rows.filter((r) => r.country_code === cc)]));

  // ---- stats used in the narrative ----------------------------------------------------------------
  function computeStats(D) {
    const st = D.pipeline.stages;
    const activity = Object.fromEntries(D.insights.activity.map((r) => [r.country_code, r]));
    const frSurvival = D.insights.survival.filter((r) => r.country_code === "FR" && r.survival_10y != null);
    const latest10 = frSurvival[frSurvival.length - 1];
    const precision = D.pipeline.geo_precision;
    const frTotal = Object.entries(precision).filter(([k]) => k.startsWith("FR:")).reduce((a, [, v]) => a + v, 0);
    const hub = D.insights.hotspots[0];
    return {
      records_ingested: compact(sum(st.bronze)),
      current_units: compact(sum(st.silver_current)),
      on_map: compact(sum(st.gold_on_map)),
      on_map_share: pct(sum(st.gold_on_map) / sum(st.silver_current), 0),
      quarantined: fmt(sum(st.quarantined)),
      gb_operating: pct(activity.GB?.operating_share, 0),
      gb_mass: pct(activity.GB?.mass_address_share, 0),
      gb_dormant: pct(activity.GB?.dormant_share, 0),
      gb_strike_off: pct(activity.GB?.pending_strike_off_share, 0),
      top_hotspot_companies: fmt(hub?.companies),
      top_hotspot_address: hub ? `${titleCase(hub.address_line)}, ${titleCase(hub.city)}` : "",
      fr_survival_10y: pct(latest10?.survival_10y, 0),
      fr_survival_10y_cohort: latest10 ? String(latest10.cohort_year) : "",
      fr_address_share: pct((precision["FR:ADDRESS"] || 0) / frTotal, 0),
    };
  }

  // ---- visualisations -----------------------------------------------------------------------------
  const VIZ = {};

  VIZ.kpis = (node, D) => {
    const st = D.pipeline.stages;
    const tiles = [
      [compact(sum(st.bronze)), T.kpi.records],
      [compact(sum(st.silver_current)), T.kpi.current],
      [pct(sum(st.gold_on_map) / sum(st.silver_current), 0), T.kpi.on_map],
      [fmt(sum(st.quarantined)), T.kpi.quarantined],
    ];
    node.replaceChildren(h("ul", { class: "stats" }, tiles.map(([value, label]) => h("li", {}, h("strong", { text: value }), h("span", { text: label })))));
  };

  VIZ.activity = (node, D) => {
    const rows = COUNTRIES.map((cc) => D.insights.activity.find((r) => r.country_code === cc)).filter(Boolean);
    const body = figure(node, {
      title: T.charts.activity_title, note: T.charts.activity_note,
      table: () => ({
        head: [T.labels.country, T.labels.active, T.labels.operating, T.labels.mass_address, T.labels.dormant, T.labels.strike_off],
        rows: rows.map((r) => [country(r.country_code), fmt(r.active_companies), pct(r.operating_share), pct(r.mass_address_share), pct(r.dormant_share), pct(r.pending_strike_off_share)]),
      }),
    });
    barRows(body, rows.map((r) => ({
      label: country(r.country_code),
      sub: [
        `${T.labels.mass_address} ${pct(r.mass_address_share, 0)}`,
        r.dormant_share != null ? `${T.labels.dormant} ${pct(r.dormant_share, 0)}` : null,
        r.pending_strike_off_share != null ? `${T.labels.strike_off} ${pct(r.pending_strike_off_share, 0)}` : null,
      ].filter(Boolean).join(" · "),
      value: r.operating_share,
      highlight: r.operating_share < 0.75,
      tip: () => `<strong>${esc(country(r.country_code))}</strong><br>${T.labels.active}: <b>${fmt(r.active_companies)}</b><br>${T.labels.operating}: <b>${fmt(r.operating_estimate)}</b> (${pct(r.operating_share)})`,
    })), { max: 1, format: (v) => pct(v, 0) });
  };

  VIZ.hotspots = (node, D) => {
    const rows = D.insights.hotspots.slice(0, 10);
    const body = figure(node, { title: T.charts.hotspots_title, note: T.charts.hotspots_note });
    body.append(h("div", { class: "table-wrap" }, h("table", {},
      h("thead", {}, h("tr", {}, [T.labels.address, T.labels.companies, T.labels.dormant_h, T.labels.strike_off_h].map((c) => h("th", { scope: "col" }, c)))),
      h("tbody", {}, rows.map((r) => h("tr", {},
        h("th", { scope: "row" }, `${titleCase(r.address_line)}, ${r.postal_code} ${titleCase(r.city)}`, h("small", { class: "rule-desc", text: country(r.country_code) })),
        h("td", { class: "num", text: fmt(r.companies) }),
        h("td", { class: "num", text: r.country_code === "GB" ? fmt(r.dormant_companies) : "—" }),
        h("td", { class: "num", text: r.country_code === "GB" ? fmt(r.pending_strike_off) : "—" })))))));
  };

  VIZ.industry_mix = (node, D) => {
    // Share of each country's active companies per NACE section: a heatmap, one hue light -> dark.
    const totals = {};
    const cells = {};
    for (const r of D.industry) {
      if (!r.nace_section) continue;
      totals[r.country_code] = (totals[r.country_code] || 0) + r.active_companies;
      cells[`${r.country_code}:${r.nace_section}`] = r.active_companies;
    }
    const countries = COUNTRIES.filter((cc) => totals[cc]);
    const missing = COUNTRIES.filter((cc) => !totals[cc]);
    const shown = SECTIONS.filter((sec) => countries.some((cc) => (cells[`${cc}:${sec}`] || 0) / totals[cc] >= 0.005));
    let peak = 0;
    for (const cc of countries) for (const sec of shown) peak = Math.max(peak, (cells[`${cc}:${sec}`] || 0) / totals[cc]);
    const note = missing.length ? `${T.charts.industry_note} ${missing.map(country).join(", ")}: ${T.labels.no_activity_codes}.` : T.charts.industry_note;
    const body = figure(node, {
      title: T.charts.industry_title, note,
      table: () => ({
        head: [T.labels.industry, ...countries.map(country)],
        rows: shown.map((sec) => [section(sec), ...countries.map((cc) => pct((cells[`${cc}:${sec}`] || 0) / totals[cc]))]),
      }),
    });
    const grid = h("div", { class: "heatmap", style: `--cols:${countries.length}` });
    grid.append(h("span", { class: "heatmap-corner" }));
    countries.forEach((cc) => grid.append(h("span", { class: "heatmap-col", text: cc, title: country(cc) })));
    for (const sec of shown) {
      grid.append(h("span", { class: "heatmap-row", text: section(sec) }));
      for (const cc of countries) {
        const share = (cells[`${cc}:${sec}`] || 0) / totals[cc];
        const level = Math.min(6, Math.floor((share / peak) * 7));
        const cell = h("span", { class: `heatmap-cell lvl-${level}` }, share >= 0.1 ? pct(share, 0) : "");
        attachTip(cell, () => `<strong>${esc(country(cc))}</strong><br>${esc(section(sec))}: <b>${pct(share)}</b><br>${fmt(cells[`${cc}:${sec}`] || 0)} ${T.labels.companies_lc}`);
        grid.append(cell);
      }
    }
    body.append(grid);
  };

  VIZ.fishing_hubs = (node, D) => {
    const MIN_ACTIVE = 30;  // below this, a handful of boats makes the ratio meaningless
    const rows = D.insights.fishing_hubs.filter((r) => r.active_companies >= MIN_ACTIVE).slice(0, 15);
    const body = figure(node, {
      title: T.charts.hubs_title,
      note: T.charts.hubs_note.replace("{n}", MIN_ACTIVE),
      table: () => ({
        head: [T.labels.town, T.labels.country, T.labels.fishing_companies, T.labels.active, T.labels.lq, T.labels.per_10k],
        rows: rows.map((r) => [titleCase(r.city), country(r.country_code), fmt(r.fishing_companies), fmt(r.active_companies),
          nf.format(r.location_quotient), r.fishing_per_10k_inhabitants == null ? "—" : nf.format(r.fishing_per_10k_inhabitants)]),
      }),
    });
    barRows(body, rows.map((r) => ({
      label: titleCase(r.city), sub: `${country(r.country_code)} · ${fmt(r.fishing_companies)} / ${fmt(r.active_companies)}`,
      value: r.location_quotient, display: `×${nf.format(Math.round(r.location_quotient))}`,
      tip: () => `<strong>${esc(titleCase(r.city))}</strong> (${esc(country(r.country_code))})<br>${T.labels.fishing_companies}: <b>${fmt(r.fishing_companies)}</b> / ${fmt(r.active_companies)}<br>${T.labels.lq}: <b>×${nf.format(r.location_quotient)}</b>`
        + (r.fishing_per_10k_inhabitants != null ? `<br>${T.labels.per_10k}: <b>${nf.format(r.fishing_per_10k_inhabitants)}</b>` : ""),
    })));
  };

  VIZ.fishing_jobs = (node, D) => {
    const rows = [...D.insights.fishing_employment].sort((a, b) => b.employees_high - a.employees_high).slice(0, 16);
    const body = figure(node, {
      title: T.charts.fishing_jobs_title, note: T.charts.fishing_jobs_note,
      table: () => ({
        head: [T.labels.region, T.labels.country, T.labels.companies, T.labels.jobs],
        rows: rows.map((r) => [regionName(r), country(r.country_code), fmt(r.companies),
          r.employees_low === r.employees_high ? fmt(r.employees_low) : `${fmt(r.employees_low)}–${fmt(r.employees_high)}`]),
      }),
    });
    barRows(body, rows.map((r) => ({
      label: regionName(r), sub: country(r.country_code),
      low: r.employees_low, high: r.employees_high, value: r.employees_low,
      display: r.employees_low === r.employees_high ? fmt(r.employees_low) : `${compact(r.employees_low)}–${compact(r.employees_high)}`,
      tip: () => `<strong>${esc(regionName(r))}</strong><br>${T.labels.jobs}: <b>${r.employees_low === r.employees_high ? fmt(r.employees_low) : `${fmt(r.employees_low)}–${fmt(r.employees_high)}`}</b><br>${T.labels.companies}: ${fmt(r.companies)}`,
    })), { series: [["sw-1", T.labels.jobs_exact_or_low], ["sw-range", T.labels.jobs_band]] });
  };

  VIZ.demography = (node, D, asOf) => {
    const lastFull = asOf.getFullYear() - 1;  // the current year is still running
    const grouped = byCountry(D.insights.demography);
    const body = figure(node, {
      title: T.charts.demography_title, note: T.charts.demography_note.replace("{year}", asOf.getFullYear()),
      table: () => ({
        head: [T.labels.country, T.labels.year, T.labels.births, T.labels.deaths],
        rows: COUNTRIES.flatMap((cc) => grouped[cc].filter((r) => r.year <= lastFull && r.year >= 2005).map((r) =>
          [country(cc), String(r.year), fmt(r.births), r.survivorship_biased ? "—" : fmt(r.deaths)])),
      }),
    });
    const grid = h("div", { class: "multiples" });
    body.append(grid);
    for (const cc of COUNTRIES) {
      const rows = grouped[cc].filter((r) => r.year <= lastFull && r.year >= 2005);
      if (!rows.length) continue;
      const biased = rows.some((r) => r.survivorship_biased);
      const yMax = niceMax(Math.max(...rows.map((r) => Math.max(r.births, biased ? 0 : r.deaths))));
      const cell = h("div", { class: "multiple" }, h("p", { class: "multiple-title" }, country(cc),
        biased ? h("span", { class: "flag", text: T.labels.live_only }) : null));
      grid.append(cell);
      const series = [{ name: T.labels.births, cls: "s-1", points: rows.map((r) => [r.year, r.births]) }];
      if (!biased) series.push({ name: T.labels.deaths, cls: "s-2", points: rows.map((r) => [r.year, r.deaths]) });
      lineChart(cell, { series, xDomain: [rows[0].year, rows[rows.length - 1].year], yMax, yFormat: compact, height: 200, labels: false, showLegend: false });
    }
    body.append(legend([["s-1", T.labels.births], ["s-2", T.labels.deaths]]));
  };

  VIZ.survival = (node, D) => {
    let current = "FR";
    const horizons = [["survival_1y", "1y", "s-1"], ["survival_3y", "3y", "s-2"], ["survival_5y", "5y", "s-3"], ["survival_10y", "10y", "s-4"]];
    const draw = () => {
      const rows = D.insights.survival.filter((r) => r.country_code === current && r.cohort_year >= 1995);
      const controls = segmented([["FR", country("FR")], ["IE", country("IE")]], current, (v) => { current = v; draw(); }, T.labels.country);
      const body = figure(node, {
        title: T.charts.survival_title, note: T.charts.survival_note, controls,
        table: () => ({
          head: [T.labels.cohort, T.labels.cohort_size, ...horizons.map(([, short]) => T.labels.after.replace("{h}", T.horizons[short]))],
          rows: rows.map((r) => [String(r.cohort_year), fmt(r.cohort_size), ...horizons.map(([key]) => pct(r[key]))]),
        }),
      });
      lineChart(body, {
        series: horizons.map(([key, short, cls]) => ({ name: T.labels.after.replace("{h}", T.horizons[short]), short, cls, points: rows.map((r) => [r.cohort_year, r[key]]) })),
        xDomain: [rows[0].cohort_year, rows[rows.length - 1].cohort_year], yMax: 1, yFormat: (v) => pct(v, 0),
      });
    };
    draw();
  };

  VIZ.survival_sections = (node, D) => {
    let current = "FR";
    const draw = () => {
      const rows = D.insights.survival_by_section
        .filter((r) => r.country_code === current && r.cohort_size >= 1000 && r.survival_5y != null)
        .sort((a, b) => b.survival_5y - a.survival_5y);
      const controls = segmented([["FR", country("FR")], ["IE", country("IE")]], current, (v) => { current = v; draw(); }, T.labels.country);
      const body = figure(node, {
        title: T.charts.survival_sections_title, note: T.charts.survival_sections_note, controls,
        table: () => ({
          head: [T.labels.industry, T.labels.cohort_size, T.labels.after.replace("{h}", T.horizons["1y"]), T.labels.after.replace("{h}", T.horizons["5y"]), T.labels.after.replace("{h}", T.horizons["10y"])],
          rows: rows.map((r) => [section(r.nace_section), fmt(r.cohort_size), pct(r.survival_1y), pct(r.survival_5y), pct(r.survival_10y)]),
        }),
      });
      barRows(body, rows.map((r) => ({
        label: section(r.nace_section), value: r.survival_5y, format: pct,
        tip: () => `<strong>${esc(section(r.nace_section))}</strong><br>${T.labels.after.replace("{h}", T.horizons["5y"])}: <b>${pct(r.survival_5y)}</b><br>${T.labels.after.replace("{h}", T.horizons["10y"])}: <b>${pct(r.survival_10y)}</b><br>${T.labels.cohort_size}: ${fmt(r.cohort_size)}`,
      })), { max: 1, format: (v) => pct(v, 0) });
    };
    draw();
  };

  VIZ.distress = (node, D) => {
    const available = ["GB", "IE", "NO"].filter((cc) => D.insights.distress.some((r) => r.country_code === cc && r.nace_section));
    let current = available[0];
    const draw = () => {
      const rows = D.insights.distress.filter((r) => r.country_code === current && r.nace_section && r.registered >= 1000)
        .sort((a, b) => b.distress_rate - a.distress_rate);
      const withStrikeOff = rows.some((r) => r.strike_off_rate > 0);
      const controls = segmented(available.map((cc) => [cc, country(cc)]), current, (v) => { current = v; draw(); }, T.labels.country);
      const body = figure(node, {
        title: T.charts.distress_title, note: T.charts.distress_note, controls,
        table: () => ({
          head: [T.labels.industry, T.labels.registered, T.labels.distress, T.labels.strike_off],
          rows: rows.map((r) => [section(r.nace_section), fmt(r.registered), pct(r.distress_rate), withStrikeOff ? pct(r.strike_off_rate) : "—"]),
        }),
      });
      const peak = Math.max(...rows.map((r) => Math.max(r.distress_rate, withStrikeOff ? r.strike_off_rate : 0)));
      barRows(body, rows.map((r) => ({
        label: section(r.nace_section),
        values: withStrikeOff ? [r.distress_rate, r.strike_off_rate] : [r.distress_rate],
        display: withStrikeOff ? `${pct(r.distress_rate)} · ${pct(r.strike_off_rate)}` : pct(r.distress_rate),
        tip: () => `<strong>${esc(section(r.nace_section))}</strong><br>${T.labels.distress}: <b>${pct(r.distress_rate)}</b> (${fmt(r.in_liquidation + r.insolvent)})`
          + (withStrikeOff ? `<br>${T.labels.strike_off}: <b>${pct(r.strike_off_rate)}</b> (${fmt(r.pending_strike_off)})` : "")
          + `<br>${T.labels.registered}: ${fmt(r.registered)}`,
      })), {
        max: peak,
        series: withStrikeOff ? [["sw-1", T.labels.distress], ["sw-2", T.labels.strike_off]] : [["sw-1", T.labels.distress]],
      });
    };
    draw();
  };

  VIZ.employment = (node, D) => {
    const available = ["NO", "FR", "ES"].filter((cc) => D.insights.employment.some((r) => r.country_code === cc));
    let current = available[0];
    const draw = () => {
      const rows = D.insights.employment.filter((r) => r.country_code === current && r.nace_section)
        .sort((a, b) => b.employees_high - a.employees_high).slice(0, 12);
      const exact = rows.every((r) => r.employees_low === r.employees_high);
      const controls = segmented(available.map((cc) => [cc, country(cc)]), current, (v) => { current = v; draw(); }, T.labels.country);
      const body = figure(node, {
        title: T.charts.employment_title, note: exact ? T.charts.employment_note_exact : T.charts.employment_note_bands, controls,
        table: () => ({
          head: [T.labels.industry, T.labels.jobs, T.labels.companies_reporting],
          rows: rows.map((r) => [section(r.nace_section), r.employees_low === r.employees_high ? fmt(r.employees_low) : `${fmt(r.employees_low)}–${fmt(r.employees_high)}`, fmt(r.companies_reporting)]),
        }),
      });
      barRows(body, rows.map((r) => ({
        label: section(r.nace_section), low: r.employees_low, high: r.employees_high, value: r.employees_low,
        display: r.employees_low === r.employees_high ? compact(r.employees_low) : `${compact(r.employees_low)}–${compact(r.employees_high)}`,
        tip: () => `<strong>${esc(section(r.nace_section))}</strong><br>${T.labels.jobs}: <b>${r.employees_low === r.employees_high ? fmt(r.employees_low) : `${fmt(r.employees_low)}–${fmt(r.employees_high)}`}</b><br>${T.labels.companies_reporting}: ${fmt(r.companies_reporting)}`,
      })), exact ? {} : { series: [["sw-1", T.labels.jobs_exact_or_low], ["sw-range", T.labels.jobs_band]] });
    };
    draw();
  };

  VIZ.funnel = (node, D) => {
    const st = D.pipeline.stages;
    const rows = COUNTRIES.map((cc) => ({ cc, bronze: st.bronze[cc], silver: st.silver_current[cc], quarantined: st.quarantined?.[cc] || 0, map: st.gold_on_map[cc] }));
    const body = figure(node, {
      title: T.charts.funnel_title, note: T.charts.funnel_note,
      table: () => ({
        head: [T.labels.country, T.labels.bronze_rows, T.labels.silver_rows, T.labels.quarantined, T.labels.on_map],
        rows: rows.map((r) => [country(r.cc), fmt(r.bronze), fmt(r.silver), fmt(r.quarantined), `${fmt(r.map)} (${pct(r.map / r.silver)})`]),
      }),
    });
    barRows(body, rows.map((r) => ({
      label: country(r.cc), sub: `${compact(r.bronze)} → ${compact(r.silver)} → ${compact(r.map)}`,
      value: r.map / r.silver, display: pct(r.map / r.silver),
      tip: () => `<strong>${esc(country(r.cc))}</strong><br>${T.labels.bronze_rows}: <b>${fmt(r.bronze)}</b><br>${T.labels.silver_rows}: <b>${fmt(r.silver)}</b><br>${T.labels.quarantined}: <b>${fmt(r.quarantined)}</b><br>${T.labels.on_map}: <b>${fmt(r.map)}</b>`,
    })), { max: 1, format: (v) => pct(v, 0) });
  };

  VIZ.precision = (node, D) => {
    const levels = ["ADDRESS", "POSTCODE", "DISTRICT", "CITY", "NONE"];
    const P = D.pipeline.geo_precision;
    const rows = COUNTRIES.map((cc) => {
      const counts = levels.map((lv) => P[`${cc}:${lv}`] || 0);
      return { cc, counts, total: counts.reduce((a, b) => a + b, 0) };
    });
    const body = figure(node, {
      title: T.charts.precision_title, note: T.charts.precision_note,
      table: () => ({
        head: [T.labels.country, ...levels.map((lv) => T.precision[lv])],
        rows: rows.map((r) => [country(r.cc), ...r.counts.map((c) => `${fmt(c)} (${pct(c / r.total, 0)})`)]),
      }),
    });
    const list = h("ul", { class: "stack-rows" });
    for (const r of rows) {
      const bar = h("span", { class: "stack" });
      r.counts.forEach((c, i) => {
        if (!c) return;
        const seg = h("span", { class: `stack-seg p-${i}`, style: `flex-grow:${c}` });
        attachTip(seg, () => `<strong>${esc(country(r.cc))}</strong><br>${esc(T.precision[levels[i]])}: <b>${pct(c / r.total)}</b> (${fmt(c)})`);
        bar.append(seg);
      });
      list.append(h("li", {}, h("span", { class: "bars-label", text: country(r.cc) }), bar));
    }
    body.append(list, legend(levels.map((lv, i) => [`p-${i}`, T.precision[lv]])));
  };

  VIZ.dq = (node, D) => {
    const rows = D.pipeline.data_quality.filter((r) => r.failed_rows > 0)
      .sort((a, b) => b.failure_rate - a.failure_rate);
    const body = figure(node, { title: T.charts.dq_title, note: T.charts.dq_note });
    body.append(h("div", { class: "table-wrap" }, h("table", {},
      h("thead", {}, h("tr", {}, [T.labels.country, T.labels.rule, T.labels.severity, T.labels.failed_rows, T.labels.failure_rate].map((c) => h("th", { scope: "col" }, c)))),
      h("tbody", {}, rows.map((r) => h("tr", {},
        h("th", { scope: "row" }, country(r.country_code)),
        h("td", {}, h("code", { text: r.rule }), h("small", { class: "rule-desc", text: T.rules[r.rule] || "" })),
        h("td", {}, h("span", { class: `severity severity-${r.severity.toLowerCase()}`, text: r.severity === "ERROR" ? T.labels.quarantine : T.labels.warning })),
        h("td", { class: "num", text: fmt(r.failed_rows) }),
        h("td", { class: "num", text: r.failure_rate < 0.00001 ? `< ${pct(0.00001, 3)}` : pct(r.failure_rate, r.failure_rate < 0.001 ? 3 : 1) })))))));
  };

  VIZ.coverage = (node, D) => {
    const insights = [...new Set(D.insights.coverage.map((r) => r.insight))];
    const lookup = Object.fromEntries(D.insights.coverage.map((r) => [`${r.insight}:${r.country_code}`, r]));
    const body = figure(node, { title: T.charts.coverage_title, note: T.charts.coverage_note });
    const table = h("table", { class: "coverage" },
      h("thead", {}, h("tr", {}, h("th", { scope: "col", text: T.labels.insight }), COUNTRIES.map((cc) => h("th", { scope: "col", title: country(cc), text: cc })))),
      h("tbody", {}, insights.map((name) => h("tr", {},
        h("th", { scope: "row", text: T.insight_names[name] || name }),
        COUNTRIES.map((cc) => {
          const r = lookup[`${name}:${cc}`];
          // No row means the register feeds the insight with no caveat worth stating.
          const included = r ? r.included : true;
          const reason = r ? (T.reasons[r.reason] || r.reason) : "";
          const cell = h("td", { class: included ? "cov-yes" : "cov-no" },
            h("span", { "aria-hidden": "true", text: included ? "✓" : "–" }),
            h("span", { class: "visually-hidden", text: `${included ? T.labels.included : T.labels.excluded}${reason ? `: ${reason}` : ""}` }));
          if (reason) attachTip(cell, () => `<strong>${esc(country(cc))}</strong> · ${included ? T.labels.included : T.labels.excluded}<br>${esc(reason)}`);
          return cell;
        })))));
    body.append(h("div", { class: "table-wrap" }, table));
  };

  // ---- map ---------------------------------------------------------------------------------------
  VIZ.map = (node) => {
    node.classList.add("viz", "viz-map");
    const state = { layer: "companies", metric: "active", country: "ALL" };
    const metricSelect = h("select", { id: "map-metric" });
    const countrySelect = h("select", { id: "map-country" },
      h("option", { value: "ALL", text: T.map.all_countries }), COUNTRIES.map((cc) => h("option", { value: cc, text: country(cc) })));
    const layerControl = segmented([["companies", T.map.layer_companies], ["fishing", T.map.layer_fishing]], state.layer, (v) => {
      state.layer = v;
      state.metric = v === "companies" ? "active" : "fishing_companies";
      fillMetrics();
      redraw();
    }, T.map.layer);
    const controls = h("div", { class: "map-controls" }, layerControl,
      h("label", { class: "field" }, h("span", { text: T.map.show }), metricSelect),
      h("label", { class: "field" }, h("span", { text: T.labels.country }), countrySelect));
    const mapEl = h("div", { class: "map-canvas", role: "region", "aria-label": T.map.aria });
    const status = h("p", { class: "viz-note map-status", text: T.labels.loading });
    const topList = h("div", { class: "map-top" });
    node.replaceChildren(controls, mapEl, status, topList);

    function fillMetrics() {
      const options = state.layer === "companies"
        ? [["active", T.map.metric_active], ["operating", T.map.metric_operating], ...SECTIONS.map((sec) => [sec, `${sec} · ${section(sec)}`])]
        : [["fishing_companies", T.map.metric_fishing_all], ["marine_fishing", T.map.marine_fishing], ["freshwater_fishing", T.map.freshwater_fishing],
           ["marine_aquaculture", T.map.marine_aquaculture], ["freshwater_aquaculture", T.map.freshwater_aquaculture]];
      metricSelect.replaceChildren(...options.map(([value, text]) => h("option", { value, text, selected: value === state.metric })));
    }
    fillMetrics();
    metricSelect.addEventListener("change", () => { state.metric = metricSelect.value; redraw(); });
    countrySelect.addEventListener("change", () => { state.country = countrySelect.value; redraw(true); });

    let map; let points; let geo = {};
    const value = (p) => {
      if (state.layer === "fishing") return p[state.metric] || 0;
      if (state.metric === "active") return p.active_companies;
      if (state.metric === "operating") return p.operating_companies;
      return (p.by_section && p.by_section[state.metric]) || 0;
    };

    function redraw(fit = false) {
      if (!map) return;
      points.clearLayers();
      const features = geo[state.layer].features.filter((f) => state.country === "ALL" || f.properties.country_code === state.country);
      const rows = features.map((f) => ({ f, v: value(f.properties) })).filter((r) => r.v > 0).sort((a, b) => b.v - a.v);
      const peak = rows.length ? rows[0].v : 1;
      const maxRadius = state.layer === "fishing" ? 18 : 26;
      const colour = getComputedStyle(document.documentElement).getPropertyValue(state.layer === "fishing" ? "--viz-fishing" : "--viz-1").trim();
      // Area proportional to the count: radius grows with the square root.
      for (const { f, v } of [...rows].reverse()) {
        const [lon, lat] = f.geometry.coordinates;
        const marker = L.circleMarker([lat, lon], {
          radius: Math.max(1.5, Math.sqrt(v / peak) * maxRadius),
          // The canvas renderer ignores CSS classes, so the colour comes from the site's tokens.
          color: colour, fillColor: colour, fillOpacity: state.layer === "fishing" ? 0.4 : 0.3, opacity: 0.85,
          weight: 0.75,
        });
        marker.bindPopup(() => popup(f.properties, v));
        points.addLayer(marker);
      }
      if (fit && rows.length) {
        const bounds = L.latLngBounds(rows.slice(0, 400).map(({ f }) => [f.geometry.coordinates[1], f.geometry.coordinates[0]]));
        map.fitBounds(bounds.pad(0.1), { maxZoom: 8 });
      } else if (fit) map.fitBounds(EUROPE);
      status.textContent = T.map.status.replace("{n}", fmt(rows.length)).replace("{total}", fmt(rows.reduce((a, r) => a + r.v, 0)));
      renderTop(rows.slice(0, 10));
    }

    function popup(p, v) {
      const name = `<strong>${esc(titleCase(p.city))}</strong> · ${esc(country(p.country_code))}`;
      if (state.layer === "fishing") {
        return `${name}<br>${T.map.metric_fishing_all}: <b>${fmt(p.fishing_companies)}</b>`
          + ["marine_fishing", "freshwater_fishing", "marine_aquaculture", "freshwater_aquaculture"]
            .filter((k) => p[k]).map((k) => `<br>${esc(T.map[k])}: ${fmt(p[k])}`).join("");
      }
      const top = Object.entries(p.by_section || {}).filter(([k]) => k !== "?").sort((a, b) => b[1] - a[1]).slice(0, 3);
      return `${name}<br>${T.map.metric_active}: <b>${fmt(p.active_companies)}</b><br>${T.map.metric_operating}: <b>${fmt(p.operating_companies)}</b>`
        + (/^[A-U]$/.test(state.metric) ? `<br>${esc(section(state.metric))}: <b>${fmt(v)}</b>` : "")
        + `<br><span class="muted">${T.map.top_industries}</span><br>` + top.map(([k, n]) => `${esc(section(k))}: ${fmt(n)}`).join("<br>");
    }

    function renderTop(rows) {
      topList.replaceChildren(h("p", { class: "viz-title", text: T.map.top_title }), h("ol", { class: "map-top-list" }, rows.map(({ f, v }) =>
        h("li", {}, h("button", {
          type: "button",
          onclick: () => map.setView([f.geometry.coordinates[1], f.geometry.coordinates[0]], 10),
        }, h("span", { text: titleCase(f.properties.city) }), h("small", { text: ` ${f.properties.country_code}` })), h("span", { class: "num", text: fmt(v) })))));
    }

    const EUROPE = [[41.5, -11], [70.5, 31]];
    async function init() {
      try {
        const [cities, fishing] = await Promise.all([getJSON("cities.geojson"), getJSON("fishing.geojson")]);
        geo = { companies: cities, fishing };
      } catch (error) {
        status.textContent = T.labels.error;
        return;
      }
      if (typeof L === "undefined") { status.textContent = T.labels.error; return; }
      // OpenStreetMap tiles, muted by CSS to match the site (and inverted in dark mode).
      map = L.map(mapEl, { preferCanvas: true, scrollWheelZoom: false, worldCopyJump: true, zoomSnap: 0.25 });
      L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
        maxZoom: 14,
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors · <a href="https://www.geonames.org/">GeoNames</a> (CC BY 4.0)',
      }).addTo(map);
      map.fitBounds(EUROPE);
      // Scroll-wheel zoom only after the map is clicked, so the page still scrolls past it.
      map.on("click", () => map.scrollWheelZoom.enable());
      map.on("mouseout", () => map.scrollWheelZoom.disable());
      points = L.layerGroup().addTo(map);
      redraw();
    }

    // The two GeoJSON files are ~3 MB: load them only when the map comes into view.
    const io = new IntersectionObserver((entries) => {
      if (entries.some((e) => e.isIntersecting)) { io.disconnect(); init(); }
    }, { rootMargin: "300px" });
    io.observe(node);
  };

  function niceMax(v) {
    if (v <= 0) return 1;
    const p = 10 ** Math.floor(Math.log10(v));
    for (const m of [1, 1.5, 2, 2.5, 3, 4, 5, 6, 8, 10]) if (m * p >= v) return m * p;
    return 10 * p;
  }

  // ---- boot --------------------------------------------------------------------------------------
  async function main() {
    let D;
    try {
      const [meta, pipeline, insights, industry] = await Promise.all(
        ["meta.json", "pipeline.json", "insights.json", "industry_by_country.json"].map(getJSON));
      D = { meta, pipeline, insights, industry };
    } catch (error) {
      root.querySelectorAll("[data-viz]").forEach((node) => {
        node.replaceChildren(h("p", { class: "viz-error", text: T.labels.error }));
      });
      console.error(error);
      return;
    }
    const asOf = new Date(D.meta.generated_at);
    const dateText = new Intl.DateTimeFormat(lang, { day: "numeric", month: "long", year: "numeric" }).format(asOf);
    root.querySelectorAll("[data-asof]").forEach((node) => { node.textContent = dateText; });
    const stats = computeStats(D);
    root.querySelectorAll("[data-stat]").forEach((node) => {
      const value = stats[node.dataset.stat];
      if (value) node.textContent = value;
    });
    root.querySelectorAll("[data-viz]").forEach((node) => {
      const draw = VIZ[node.dataset.viz];
      if (!draw) return;
      try {
        draw(node, D, asOf);
      } catch (error) {
        node.replaceChildren(h("p", { class: "viz-error", text: T.labels.error }));
        console.error(node.dataset.viz, error);
      }
    });
  }

  main();
})();

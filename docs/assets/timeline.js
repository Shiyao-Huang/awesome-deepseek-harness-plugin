(function () {
  "use strict";

  const allowedSorts = new Set(["time", "influence", "trend", "source", "record", "topic"]);
  const allowedDirections = new Set(["asc", "desc"]);
  const defaultDirections = Object.freeze({
    time: "desc",
    influence: "asc",
    trend: "desc",
    source: "asc",
    record: "asc",
    topic: "asc",
  });
  const collator = new Intl.Collator(undefined, { numeric: true, sensitivity: "base" });
  const dateValue = (value) => {
    const parsed = Date.parse(value || "");
    return Number.isFinite(parsed) ? parsed : Number.NEGATIVE_INFINITY;
  };
  const trendValue = (record, key, fallback) => {
    const value = record.trend?.hasEvidence ? Number(record.trend[key]) : fallback;
    return Number.isFinite(value) ? value : fallback;
  };
  const compareNumber = (left, right) => left === right ? 0 : left < right ? -1 : 1;

  function defaultDirection(sort) {
    return defaultDirections[sort] || "asc";
  }

  function compareRecords(left, right, sort, direction) {
    let comparison = 0;
    if (sort === "influence") {
      comparison = compareNumber(Number(left.rank), Number(right.rank));
    } else if (sort === "trend") {
      comparison = compareNumber(Number(Boolean(left.trend?.hasEvidence)), Number(Boolean(right.trend?.hasEvidence)));
      if (!comparison) comparison = compareNumber(trendValue(left, "percent", Number.NEGATIVE_INFINITY), trendValue(right, "percent", Number.NEGATIVE_INFINITY));
      if (!comparison) comparison = compareNumber(trendValue(left, "delta", Number.NEGATIVE_INFINITY), trendValue(right, "delta", Number.NEGATIVE_INFINITY));
    } else if (sort === "source") {
      comparison = collator.compare(String(left.sourceLabel || ""), String(right.sourceLabel || ""));
    } else if (sort === "record") {
      comparison = collator.compare(String(left.title || ""), String(right.title || ""));
    } else if (sort === "topic") {
      comparison = collator.compare(String(left.categoryLabel || ""), String(right.categoryLabel || ""));
    } else {
      comparison = compareNumber(dateValue(left.eventAt), dateValue(right.eventAt));
    }
    if (comparison) return comparison * (direction === "desc" ? -1 : 1);
    return Number(left.rank) - Number(right.rank);
  }

  if (typeof module !== "undefined" && module.exports) {
    module.exports = { compareRecords, defaultDirection };
  }
  if (typeof document === "undefined") return;

  const dataElement = document.getElementById("timeline-data");
  if (!dataElement) return;

  const payload = JSON.parse(dataElement.textContent || "{}");
  const records = Array.isArray(payload.records) ? payload.records : [];
  const referenceTime = Date.parse(payload.referenceTime || "");
  const batchSize = 100;
  const allowedWindows = new Set(["1", "7", "30", "365", "all"]);
  const sortButtons = Array.from(document.querySelectorAll("[data-timeline-sort]"));
  const search = document.getElementById("timeline-search");
  const source = document.getElementById("timeline-source");
  const category = document.getElementById("timeline-category");
  const windowSelect = document.getElementById("timeline-window");
  const trendingOnly = document.getElementById("timeline-trending-only");
  const summary = document.getElementById("timeline-summary");
  const body = document.getElementById("timeline-body");
  const empty = document.getElementById("timeline-empty");
  const more = document.getElementById("timeline-more");
  const trendGrid = document.getElementById("timeline-trend-grid");

  if (!search || !source || !category || !windowSelect || !trendingOnly || !summary || !body || !empty || !more || !trendGrid) return;

  const params = new URLSearchParams(window.location.search);
  const requestedSort = params.get("sort") || "time";
  const requestedWindow = params.get("window") || "30";
  const sort = allowedSorts.has(requestedSort) ? requestedSort : "time";
  const requestedDirection = params.get("direction") || defaultDirection(sort);
  const state = {
    sort,
    direction: allowedDirections.has(requestedDirection) ? requestedDirection : defaultDirection(sort),
    query: params.get("q") || "",
    source: params.get("source") || "all",
    category: params.get("category") || "all",
    window: allowedWindows.has(requestedWindow) ? requestedWindow : "30",
    trendingOnly: params.get("trending") === "1",
    visible: batchSize,
  };

  const escapeHtml = (value) => String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
  const number = (value) => Number(value).toLocaleString();
  const signed = (value) => `${Number(value) >= 0 ? "+" : ""}${number(value)}`;
  const percent = (value) => value === null || value === undefined
    ? "rate n/a"
    : `${Number(value) >= 0 ? "+" : ""}${Number(value).toFixed(1)}%`;
  const elapsed = (hours) => `${Number(hours).toLocaleString(undefined, { maximumFractionDigits: 1 })}h`;

  function selectedRecords() {
    const query = state.query.trim().toLocaleLowerCase();
    const minimumTime = state.window === "all" || !Number.isFinite(referenceTime)
      ? Number.NEGATIVE_INFINITY
      : referenceTime - Number(state.window) * 24 * 60 * 60 * 1000;
    const filtered = records.filter((record) => {
      if (state.source !== "all" && record.source !== state.source) return false;
      if (state.category !== "all" && record.category !== state.category) return false;
      if (state.trendingOnly && !record.trend?.hasEvidence) return false;
      if (dateValue(record.eventAt) < minimumTime) return false;
      if (!query) return true;
      return [record.title, record.author, record.sourceLabel, record.categoryLabel, record.itemType]
        .some((value) => String(value || "").toLocaleLowerCase().includes(query));
    });
    return filtered.sort((left, right) => compareRecords(left, right, state.sort, state.direction));
  }

  function signal(record) {
    const trend = record.trend;
    if (!trend?.hasEvidence) return '<span class="timeline-no-trend">暂无趋势证据</span>';
    return `<span class="timeline-trend-signal"><strong>${escapeHtml(trend.metricLabel)} ${number(trend.current)}</strong><span>${signed(trend.delta)} · ${percent(trend.percent)} · ${elapsed(trend.elapsedHours)}</span><small>${escapeHtml(trend.source)} · ${escapeHtml(String(trend.from || "").slice(0, 10))} → ${escapeHtml(String(trend.to || "").slice(0, 10))}</small></span>`;
  }

  function row(record) {
    const id = encodeURIComponent(record.id);
    return `<tr class="timeline-row" data-record-id="${escapeHtml(record.id)}"><td class="timeline-rank">#${number(record.rank)}</td><td><time datetime="${escapeHtml(record.eventAt)}">${escapeHtml(record.timeLabel)}</time></td><td>${escapeHtml(record.sourceLabel)}</td><td><a href="skills/${id}.html">${escapeHtml(record.title)}</a><small>${escapeHtml(record.author)} · ${escapeHtml(record.itemType)}</small></td><td>${signal(record)}</td><td>${escapeHtml(record.categoryLabel)}</td></tr>`;
  }

  function renderTrending(matches) {
    const rising = matches
      .filter((record) => record.trend?.hasEvidence && Number(record.trend.delta) > 0)
      .sort((left, right) => (
        trendValue(right, "percent", Number.NEGATIVE_INFINITY) - trendValue(left, "percent", Number.NEGATIVE_INFINITY)
        || trendValue(right, "delta", 0) - trendValue(left, "delta", 0)
        || Number(left.rank) - Number(right.rank)
      ))
      .slice(0, 4);
    trendGrid.innerHTML = rising.length
      ? rising.map((record) => `<article class="timeline-trend-card"><p>${escapeHtml(record.sourceLabel)} · rank #${number(record.rank)}</p><h3><a href="skills/${encodeURIComponent(record.id)}.html">${escapeHtml(record.title)}</a></h3>${signal(record)}</article>`).join("")
      : '<p class="timeline-empty-trend">当前筛选中暂无可展示的正增长证据。</p>';
  }

  function syncUrl() {
    const next = new URLSearchParams();
    next.set("sort", state.sort);
    next.set("direction", state.direction);
    if (state.query) next.set("q", state.query);
    if (state.source !== "all") next.set("source", state.source);
    if (state.category !== "all") next.set("category", state.category);
    next.set("window", state.window);
    if (state.trendingOnly) next.set("trending", "1");
    window.history.replaceState(null, "", `${window.location.pathname}?${next.toString()}${window.location.hash}`);
  }

  function render({ updateUrl = false } = {}) {
    const matches = selectedRecords();
    const visible = matches.slice(0, state.visible);
    body.innerHTML = visible.map(row).join("");
    empty.hidden = matches.length !== 0;
    more.hidden = visible.length >= matches.length;
    const labels = { time: "时间", influence: "影响力（Registry rank）", trend: "趋势证据", source: "来源", record: "记录名称", topic: "分类" };
    const directionLabel = state.direction === "asc" ? "升序" : "降序";
    summary.innerHTML = `<strong>${number(matches.length)}</strong> matches · showing ${number(visible.length)} · ${labels[state.sort]} ${directionLabel}`;
    sortButtons.forEach((button) => {
      const selected = button.dataset.timelineSort === state.sort;
      button.classList.toggle("is-selected", selected);
      button.setAttribute("aria-pressed", String(selected));
      if (selected) button.dataset.sortDirection = state.direction;
      else delete button.dataset.sortDirection;
      const header = button.closest("th");
      if (header) header.setAttribute("aria-sort", selected ? (state.direction === "asc" ? "ascending" : "descending") : "none");
    });
    renderTrending(matches);
    if (updateUrl) syncUrl();
  }

  function resetAndRender() {
    state.visible = batchSize;
    render({ updateUrl: true });
  }

  if (![...source.options].some((option) => option.value === state.source)) state.source = "all";
  if (![...category.options].some((option) => option.value === state.category)) state.category = "all";
  search.value = state.query;
  source.value = state.source;
  category.value = state.category;
  windowSelect.value = state.window;
  trendingOnly.checked = state.trendingOnly;

  sortButtons.forEach((button) => button.addEventListener("click", () => {
    const nextSort = button.dataset.timelineSort;
    if (!allowedSorts.has(nextSort)) return;
    if (state.sort === nextSort) state.direction = state.direction === "asc" ? "desc" : "asc";
    else {
      state.sort = nextSort;
      state.direction = defaultDirection(nextSort);
    }
    resetAndRender();
  }));
  search.addEventListener("input", () => {
    state.query = search.value;
    resetAndRender();
  });
  source.addEventListener("change", () => {
    state.source = source.value;
    resetAndRender();
  });
  category.addEventListener("change", () => {
    state.category = category.value;
    resetAndRender();
  });
  windowSelect.addEventListener("change", () => {
    state.window = windowSelect.value;
    resetAndRender();
  });
  trendingOnly.addEventListener("change", () => {
    state.trendingOnly = trendingOnly.checked;
    resetAndRender();
  });
  more.addEventListener("click", () => {
    state.visible += batchSize;
    render();
  });
  document.addEventListener("keydown", (event) => {
    if (event.key === "/" && document.activeElement !== search) {
      event.preventDefault();
      search.focus();
    }
    if (event.key === "Escape" && document.activeElement === search) search.blur();
  });

  render();
})();

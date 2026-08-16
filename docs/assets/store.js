(function () {
  "use strict";

  const wordSegmenter = typeof Intl.Segmenter === "function"
    ? new Intl.Segmenter(undefined, { granularity: "word" })
    : null;
  const queryStopWords = new Set([
    "a", "an", "and", "can", "find", "for", "i", "install", "me", "need", "please",
    "plugin", "plugins", "show", "that", "the", "to", "want", "with",
    "一个", "一款", "可以", "帮", "帮我", "我", "找", "查找", "的", "能", "请", "需要", "想要", "安装", "插件",
  ]);

  function queryTerms(value) {
    const query = String(value || "").trim().toLocaleLowerCase();
    const segments = wordSegmenter
      ? Array.from(wordSegmenter.segment(query)).filter((part) => part.isWordLike).map((part) => part.segment)
      : query.split(/\s+/u);
    return segments.filter((term) => (
      !queryStopWords.has(term) && (term.length > 1 || /^[a-z0-9]$/u.test(term))
    ));
  }

  function searchText(haystackValue, queryValue) {
    const haystack = String(haystackValue || "").toLocaleLowerCase();
    const query = String(queryValue || "").trim().toLocaleLowerCase();
    const terms = queryTerms(query);
    if (!query || terms.length === 0) return { matched: true, score: 0 };
    const matchedTerms = terms.filter((term) => haystack.includes(term)).length;
    const minimumTerms = terms.length <= 1 ? terms.length : Math.min(2, Math.ceil(terms.length / 2));
    if (matchedTerms < minimumTerms) return { matched: false, score: 0 };
    const phraseScore = haystack.includes(query) ? 80 : 0;
    const coverageScore = Math.round(60 * matchedTerms / terms.length);
    return { matched: true, score: phraseScore + matchedTerms * 20 + coverageScore };
  }

  if (typeof module !== "undefined" && module.exports) {
    module.exports = { queryTerms, searchText };
  }
  if (typeof document === "undefined") return;

  const catalogPage = ["home", "market"].includes(document.body.dataset.page)
    && ["catalog-grid", "search-input", "sort-select", "result-summary", "no-results", "clear-filters"]
      .every((id) => document.getElementById(id));
  if (catalogPage) {
    const cards = Array.from(document.querySelectorAll(".skill-card"));
    const grid = document.getElementById("catalog-grid");
    const search = document.getElementById("search-input");
    const sort = document.getElementById("sort-select");
    const summary = document.getElementById("result-summary");
    const empty = document.getElementById("no-results");
    const clear = document.getElementById("clear-filters");
    const resultNoun = document.body.dataset.resultNoun || "records";
    let active = { type: "all", value: "all" };
    const initialQuery = new URLSearchParams(window.location.search).get("q");
    if (initialQuery) search.value = initialQuery;

    function apply() {
      const query = (search.value || "").trim().toLowerCase();
      const visible = cards.flatMap((card) => {
        const matchesFilter = active.type === "all" || card.dataset[active.type] === active.value;
        const match = searchText(`${card.dataset.title || ""} ${card.textContent || ""}`, query);
        card.hidden = !(matchesFilter && match.matched);
        return matchesFilter && match.matched ? [{ card, relevance: match.score }] : [];
      });
      const ordered = visible.slice().sort((a, b) => {
        if (query && b.relevance !== a.relevance) return b.relevance - a.relevance;
        if (sort.value === "score") return Number(b.card.dataset.score) - Number(a.card.dataset.score);
        if (sort.value === "latest") return b.card.dataset.seen.localeCompare(a.card.dataset.seen);
        if (sort.value === "title") return a.card.dataset.title.localeCompare(b.card.dataset.title);
        return Number(a.card.dataset.rank) - Number(b.card.dataset.rank);
      });
      ordered.forEach(({ card }) => grid.appendChild(card));
      summary.textContent = `Showing ${visible.length.toLocaleString()} ${resultNoun}`;
      empty.hidden = visible.length !== 0;
    }

    document.querySelectorAll(".filter-option").forEach((button) => {
      button.addEventListener("click", () => {
        active = { type: button.dataset.filterType, value: button.dataset.filterValue };
        document.querySelectorAll(".filter-option").forEach((candidate) => candidate.classList.remove("is-selected"));
        button.classList.add("is-selected");
        apply();
      });
    });
    clear.addEventListener("click", () => {
      active = { type: "all", value: "all" };
      search.value = "";
      document.querySelectorAll(".filter-option").forEach((candidate) => candidate.classList.remove("is-selected"));
      document.querySelector('[data-filter-type="all"]').classList.add("is-selected");
      apply();
    });
    search.addEventListener("input", apply);
    sort.addEventListener("change", apply);
    document.addEventListener("keydown", (event) => {
      if (event.key === "/" && document.activeElement !== search) {
        event.preventDefault();
        search.focus();
      }
      if (event.key === "Escape" && document.activeElement === search) search.blur();
    });
    apply();
  }

  async function copyText(value) {
    if (navigator.clipboard?.writeText) {
      try {
        await Promise.race([
          navigator.clipboard.writeText(value),
          new Promise((_, reject) => window.setTimeout(() => reject(new Error("clipboard timeout")), 1000)),
        ]);
        return;
      } catch {
        // Fall through when the browser does not resolve clipboard writes.
      }
    }
    const textarea = document.createElement("textarea");
    textarea.value = value;
    textarea.setAttribute("readonly", "");
    textarea.style.position = "fixed";
    textarea.style.opacity = "0";
    document.body.appendChild(textarea);
    textarea.select();
    const copied = document.execCommand("copy");
    textarea.remove();
    if (!copied) throw new Error("copy failed");
  }

  document.addEventListener("click", (event) => {
    const button = event.target.closest("[data-market-language]");
    if (!button) return;
    const guide = button.closest("[data-market-i18n]");
    const language = button.dataset.marketLanguage;
    if (!guide || !["zh", "en"].includes(language)) return;
    guide.dataset.marketLang = language;
    guide.querySelectorAll("[data-market-language]").forEach((candidate) => {
      candidate.setAttribute("aria-pressed", String(candidate === button));
    });
  });

  document.addEventListener("click", async (event) => {
    const button = event.target.closest(".copy-install");
    if (!button) return;
    const command = button.dataset.install;
    if (!command || button.disabled) return;
    const original = button.innerHTML;
    const language = button.closest("[data-market-i18n]")?.dataset.marketLang || "en";
    const labels = language === "zh"
      ? { loading: "复制中...", success: "已复制", error: "复制失败" }
      : { loading: "Copying...", success: "Copied", error: "Copy failed" };
    button.disabled = true;
    button.setAttribute("aria-busy", "true");
    button.dataset.copyState = "loading";
    button.textContent = labels.loading;
    try {
      await copyText(command);
      button.dataset.copyState = "success";
      button.textContent = labels.success;
    } catch {
      button.dataset.copyState = "error";
      button.textContent = labels.error;
    }
    window.setTimeout(() => {
      button.disabled = false;
      button.removeAttribute("aria-busy");
      delete button.dataset.copyState;
      button.innerHTML = original;
    }, 1400);
  });
})();

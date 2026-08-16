(function () {
  "use strict";

  const catalogPage = ["home", "market"].includes(document.body.dataset.page);
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

    function apply() {
      const query = (search.value || "").trim().toLowerCase();
      const visible = cards.filter((card) => {
        const matchesFilter = active.type === "all" || card.dataset[active.type] === active.value;
        const matchesQuery = !query || card.dataset.title.includes(query) || card.textContent.toLowerCase().includes(query);
        card.hidden = !(matchesFilter && matchesQuery);
        return matchesFilter && matchesQuery;
      });
      const ordered = visible.slice().sort((a, b) => {
        if (sort.value === "score") return Number(b.dataset.score) - Number(a.dataset.score);
        if (sort.value === "latest") return b.dataset.seen.localeCompare(a.dataset.seen);
        if (sort.value === "title") return a.dataset.title.localeCompare(b.dataset.title);
        return Number(a.dataset.rank) - Number(b.dataset.rank);
      });
      ordered.forEach((card) => grid.appendChild(card));
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

  document.addEventListener("click", async (event) => {
    const button = event.target.closest(".copy-install");
    if (!button) return;
    const command = button.dataset.install;
    if (!command || button.disabled) return;
    const original = button.textContent;
    button.disabled = true;
    button.textContent = "Copying...";
    try {
      await copyText(command);
      button.textContent = "Copied";
    } catch {
      button.textContent = "Copy failed";
    }
    window.setTimeout(() => { button.disabled = false; button.textContent = original; }, 1400);
  });
})();

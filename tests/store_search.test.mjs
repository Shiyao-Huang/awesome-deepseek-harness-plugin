import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { createRequire } from "node:module";
import test from "node:test";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";
import { runInNewContext } from "node:vm";

const require = createRequire(import.meta.url);
const { queryTerms, searchText } = require("../docs/assets/store.js");
const root = dirname(dirname(fileURLToPath(import.meta.url)));

test("search ignores request boilerplate and requires meaningful multi-word coverage", () => {
  assert.deepEqual(queryTerms("find a plugin for public web search"), ["public", "web", "search"]);
  assert.equal(searchText("web search bridge for dsh", "find a plugin for public web search").matched, true);
  assert.equal(searchText("public profile manager", "find a plugin for public web search").matched, false);
});

test("real Store cards match English and Chinese capability phrases", () => {
  const market = readFileSync(join(root, "docs", "market.html"), "utf8");
  const searchableCards = Array.from(
    market.matchAll(/class="skill-card market-plugin-card"[^>]*data-title="([^"]+)"/g),
    (match) => match[1],
  );

  assert.equal(searchableCards.length > 900, true);
  assert.equal(searchableCards.some((card) => searchText(card, "public web search").matched), true);
  assert.equal(searchableCards.some((card) => searchText(card, "浏览器 搜索").matched), true);
});

test("homepage without catalog controls still wires global language controls", () => {
  const clickListeners = [];
  const document = {
    body: { dataset: { page: "home" } },
    getElementById: () => null,
    addEventListener: (type, listener) => {
      if (type === "click") clickListeners.push(listener);
    },
  };
  const source = readFileSync(join(root, "docs", "assets", "store.js"), "utf8");
  runInNewContext(source, { document, Intl, module: { exports: {} }, URLSearchParams });

  assert.equal(clickListeners.length, 2);
  const pressed = new Map();
  const guide = {
    dataset: { marketLang: "zh" },
    querySelectorAll: () => [chinese, english],
  };
  const button = (language) => ({
    dataset: { marketLanguage: language },
    closest: (selector) => selector === "[data-market-language]" ? buttonByLanguage[language] : guide,
    setAttribute: (name, value) => pressed.set(language, [name, value]),
  });
  const buttonByLanguage = {};
  const chinese = buttonByLanguage.zh = button("zh");
  const english = buttonByLanguage.en = button("en");

  clickListeners[0]({ target: english });

  assert.equal(guide.dataset.marketLang, "en");
  assert.deepEqual(pressed.get("zh"), ["aria-pressed", "false"]);
  assert.deepEqual(pressed.get("en"), ["aria-pressed", "true"]);
});

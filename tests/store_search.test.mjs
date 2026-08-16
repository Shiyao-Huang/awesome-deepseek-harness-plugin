import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { createRequire } from "node:module";
import test from "node:test";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

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

import assert from "node:assert/strict";
import { createRequire } from "node:module";
import test from "node:test";

const require = createRequire(import.meta.url);
const { compareRecords, defaultDirection } = require("../docs/assets/timeline.js");

const records = [
  { rank: 9, eventAt: "2026-08-15T00:00:00Z", sourceLabel: "小红书", title: "Beta", categoryLabel: "界面", trend: { hasEvidence: false } },
  { rank: 2, eventAt: "2026-08-16T00:00:00Z", sourceLabel: "GitHub", title: "Alpha 10", categoryLabel: "安全", trend: { hasEvidence: true, percent: 10, delta: 2 } },
  { rank: 4, eventAt: "2026-08-14T00:00:00Z", sourceLabel: "Hacker News", title: "Alpha 2", categoryLabel: "编排", trend: { hasEvidence: true, percent: 50, delta: 1 } },
];

const order = (sort, direction = defaultDirection(sort)) => records
  .slice()
  .sort((left, right) => compareRecords(left, right, sort, direction))
  .map((record) => record.rank);

test("each Timeline column has a deterministic default sort", () => {
  assert.deepEqual(order("influence"), [2, 4, 9]);
  assert.deepEqual(order("time"), [2, 9, 4]);
  assert.deepEqual(order("source"), [2, 4, 9]);
  assert.deepEqual(order("record"), [4, 2, 9]);
  assert.deepEqual(order("trend"), [4, 2, 9]);
  assert.deepEqual(order("topic"), [2, 9, 4]);
});

test("clicking the selected Timeline column can reverse its order", () => {
  assert.deepEqual(order("time", "asc"), [4, 9, 2]);
  assert.deepEqual(order("influence", "desc"), [9, 4, 2]);
  assert.deepEqual(order("trend", "asc"), [9, 2, 4]);
});

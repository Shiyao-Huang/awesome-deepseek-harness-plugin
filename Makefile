PYTHON ?= python3

.PHONY: init seed update sources forks forks-filtered fork-index restore-full archive-full public-db value market index build test check core-refresh schedule trends enrich readme

init:
	$(PYTHON) scripts/collect.py init

seed:
	$(PYTHON) scripts/collect.py seed

update:
	$(PYTHON) scripts/collect.py update

core-refresh:
	stamp="$$(date -u +%Y%m%dT%H%M%SZ)"; $(PYTHON) scripts/monitor_sources.py --raw-output "data/raw/upstreams/$${stamp}.json"
	stamp="$$(date -u +%Y%m%dT%H%M%SZ)"; $(PYTHON) scripts/collect.py update --trigger scheduled --raw-output "data/raw/api/$${stamp}.json"
	$(MAKE) build
	$(MAKE) archive-full
	$(MAKE) public-db
	$(PYTHON) scripts/validate.py

schedule:
	stamp="$$(date -u +%Y%m%dT%H%M%SZ)"; $(PYTHON) scripts/monitor_sources.py --raw-output "data/raw/upstreams/$${stamp}.json"
	$(PYTHON) scripts/collect_forks.py
	$(PYTHON) scripts/collect.py update --trigger scheduled
	$(PYTHON) scripts/build_fork_index.py
	$(MAKE) build
	$(MAKE) archive-full
	$(MAKE) public-db
	$(PYTHON) scripts/validate.py

index:
	$(PYTHON) scripts/build_index.py

trends:
	$(PYTHON) scripts/build_trends.py

enrich:
	$(PYTHON) scripts/enrich_content.py

sources:
	stamp="$$(date -u +%Y%m%dT%H%M%SZ)"; $(PYTHON) scripts/monitor_sources.py --raw-output "data/raw/upstreams/$${stamp}.json"

forks:
	$(PYTHON) scripts/collect_forks.py

forks-filtered:
	$(PYTHON) scripts/collect_forks.py --min-stars 10

fork-index:
	$(PYTHON) scripts/build_fork_index.py

archive-full:
	zstd -q -T0 -19 -f data/aggregator.sqlite3 -o data/aggregator-full.sqlite3.zst

restore-full:
	zstd -q -d -f data/aggregator-full.sqlite3.zst -o data/aggregator.sqlite3

public-db:
	$(PYTHON) scripts/build_public_db.py --source data/aggregator.sqlite3 --output data/aggregator.sqlite3 --full-archive data/aggregator-full.sqlite3.zst --in-place

value:
	$(PYTHON) scripts/build_value_matrix.py

market:
	$(PYTHON) scripts/build_market_registry.py

build:
	$(PYTHON) scripts/build_value_matrix.py
	$(PYTHON) scripts/build_index.py
	$(PYTHON) scripts/build_market_registry.py
	$(PYTHON) scripts/build_views.py
	$(PYTHON) scripts/build_trends.py
	$(PYTHON) scripts/build_readme.py

readme:
	$(PYTHON) scripts/build_readme.py

test:
	$(PYTHON) -m unittest discover -s tests -p 'test_*.py'
	pnpm --dir plugin test

check: test
	$(PYTHON) -m json.tool data/raw/2026-08-15-egolite.json >/dev/null
	$(PYTHON) -m py_compile scripts/collect.py scripts/build_public_db.py scripts/build_index.py scripts/build_fork_index.py scripts/build_site.py scripts/build_views.py scripts/build_trends.py scripts/build_readme.py scripts/build_value_matrix.py scripts/build_market_registry.py scripts/monitor_sources.py scripts/collect_forks.py scripts/enrich_content.py scripts/materialize_raw_snapshots.py scripts/score.py
	$(PYTHON) scripts/validate.py

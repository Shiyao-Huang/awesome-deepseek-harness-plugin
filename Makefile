PYTHON ?= python3

.PHONY: init seed update sources forks fork-index archive-full value index build check schedule trends enrich readme

init:
	$(PYTHON) scripts/collect.py init

seed:
	$(PYTHON) scripts/collect.py seed

update:
	$(PYTHON) scripts/collect.py update

schedule:
	stamp="$$(date -u +%Y%m%dT%H%M%SZ)"; $(PYTHON) scripts/monitor_sources.py --raw-output "data/raw/upstreams/$${stamp}.json"
	$(PYTHON) scripts/collect_forks.py
	$(PYTHON) scripts/collect.py update --trigger scheduled
	$(MAKE) archive-full
	$(PYTHON) scripts/build_fork_index.py
	$(PYTHON) scripts/build_value_matrix.py
	$(PYTHON) scripts/build_index.py
	$(PYTHON) scripts/build_views.py
	$(PYTHON) scripts/build_trends.py
	$(PYTHON) scripts/build_readme.py
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

fork-index:
	$(PYTHON) scripts/build_fork_index.py

archive-full:
	zstd -q -T0 -19 -f data/aggregator.sqlite3 -o data/aggregator-full.sqlite3.zst

value:
	$(PYTHON) scripts/build_value_matrix.py

build:
	$(PYTHON) scripts/build_value_matrix.py
	$(PYTHON) scripts/build_index.py
	$(PYTHON) scripts/build_views.py
	$(PYTHON) scripts/build_trends.py
	$(PYTHON) scripts/build_readme.py

readme:
	$(PYTHON) scripts/build_readme.py

check:
	$(PYTHON) -m json.tool data/raw/2026-08-15-egolite.json >/dev/null
	$(PYTHON) -m py_compile scripts/collect.py scripts/build_index.py scripts/build_fork_index.py scripts/build_views.py scripts/build_trends.py scripts/build_readme.py scripts/build_value_matrix.py scripts/monitor_sources.py scripts/collect_forks.py scripts/enrich_content.py scripts/score.py
	$(PYTHON) scripts/validate.py

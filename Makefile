PYTHON ?= python3

.PHONY: init seed update sources value index build check schedule trends enrich

init:
	$(PYTHON) scripts/collect.py init

seed:
	$(PYTHON) scripts/collect.py seed

update:
	$(PYTHON) scripts/collect.py update

schedule:
	stamp="$$(date -u +%Y%m%dT%H%M%SZ)"; $(PYTHON) scripts/monitor_sources.py --raw-output "data/raw/upstreams/$${stamp}.json"
	$(PYTHON) scripts/collect.py update --trigger scheduled
	$(PYTHON) scripts/build_value_matrix.py
	$(PYTHON) scripts/build_index.py
	$(PYTHON) scripts/build_views.py
	$(PYTHON) scripts/build_trends.py
	$(PYTHON) scripts/validate.py

index:
	$(PYTHON) scripts/build_index.py

trends:
	$(PYTHON) scripts/build_trends.py

enrich:
	$(PYTHON) scripts/enrich_content.py

sources:
	stamp="$$(date -u +%Y%m%dT%H%M%SZ)"; $(PYTHON) scripts/monitor_sources.py --raw-output "data/raw/upstreams/$${stamp}.json"

value:
	$(PYTHON) scripts/build_value_matrix.py

build:
	$(PYTHON) scripts/build_value_matrix.py
	$(PYTHON) scripts/build_index.py
	$(PYTHON) scripts/build_views.py
	$(PYTHON) scripts/build_trends.py

check:
	$(PYTHON) -m json.tool data/raw/2026-08-15-egolite.json >/dev/null
	$(PYTHON) -m py_compile scripts/collect.py scripts/build_index.py scripts/build_views.py scripts/build_trends.py scripts/build_value_matrix.py scripts/monitor_sources.py scripts/enrich_content.py scripts/score.py
	$(PYTHON) scripts/validate.py

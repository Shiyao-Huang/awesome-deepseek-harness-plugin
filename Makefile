PYTHON ?= python3

.PHONY: init seed update build check

init:
	$(PYTHON) scripts/collect.py init

seed:
	$(PYTHON) scripts/collect.py seed

update:
	$(PYTHON) scripts/collect.py update

build:
	$(PYTHON) scripts/build_views.py

check:
	$(PYTHON) -m json.tool data/raw/2026-08-15-egolite.json >/dev/null
	$(PYTHON) -m py_compile scripts/collect.py scripts/build_views.py
	$(PYTHON) scripts/validate.py

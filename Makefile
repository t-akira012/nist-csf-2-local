SHELL := /bin/sh
PY := uv run python

.PHONY: run sync validate clean

run: sync
	$(PY) scripts/build.py
	$(MAKE) validate

sync:
	uv sync

validate:
	$(PY) scripts/build.py --validate

clean:
	rm -rf generated

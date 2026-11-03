SHELL := /bin/sh
PY := uv run python

.PHONY: run sync validate ja clean

run: sync
	$(PY) scripts/build.py
	$(MAKE) validate

sync:
	uv sync

validate:
	$(PY) scripts/build.py --validate

# Usage: make ja ID=GV.OC-01
ja:
	@test -n "$(ID)" || { echo 'Usage: make ja ID=GV.OC-01' >&2; exit 2; }
	$(PY) scripts/ja.py --id '$(ID)'

clean:
	rm -rf generated

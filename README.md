# NIST CSF 2.0 local reference for coding agents

[日本語](README.ja.md)

This repository provides a fixed source manifest, `make run`, English Markdown sections, a JSON index, and links to NIST's official Japanese translation.

## Build

Requirements: `uv` and `curl`. Run when you want to download the English source:

```sh
make run
```

This downloads the English Reference Tool export to `generated/source/`, creates one Markdown file per active CSF 2.0 ID in `generated/sections/`, and writes `generated/index.json`. Withdrawn IDs included in the export are excluded. `make validate` checks the expected 6 functions, 22 categories, 106 subcategories, section files, the English source hash, and the Japanese links. Downloads and generated files stay local and are ignored by Git.

## Read one item

Find an ID in `generated/index.json`, then read `generated/sections/GV.OC-01.md`. For Japanese, find the same ID in [`ja/index.md`](ja/index.md) and open its link to the corresponding page of NIST's official Japanese PDF. Search the ID on that page because several items can share a page.

The Japanese PDF covers the CSF core. The English Reference Tool's implementation examples are not part of that Japanese publication. This repository does not translate or copy the Japanese text.

## Sources

See `sources.json` for the original URLs. The official Japanese publication is [NIST CSWP 29 jpn](https://www.nist.gov/publications/nist-cybersecurity-framework-csf-20-japanese-translation).

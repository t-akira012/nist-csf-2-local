# NIST CSF 2.0 local reference for coding agents

[日本語](README.ja.md)

This repository provides a fixed source manifest, `make run`, generated Markdown sections, a JSON index, and agent lookup rules. The sources are NIST's English CSF 2.0 Reference Tool export and official Japanese translation.

## Build

Requirements: `uv`, `curl`, and `pdftotext` (Poppler). Run once when you want to download the sources:

```sh
make run
```

This downloads both originals to `generated/source/`, creates one English Markdown file per active CSF 2.0 ID in `generated/sections/`, and writes `generated/index.json`. Withdrawn IDs included in the English export are excluded. `make validate` checks the expected 6 functions, 22 categories, 106 subcategories, section files, and source hashes. Downloads and generated files stay local and are ignored by Git.

## Read or translate one item

Find an ID in `generated/index.json`, then read `generated/sections/GV.OC-01.md`. For Japanese:

```sh
make ja ID=GV.OC-01
```

The command writes only `ja/GV.OC-01.md`. It extracts the CSF core wording from NIST's official Japanese PDF without translating it. If the English item has implementation examples, it asks the local Codex CLI to translate only those examples and labels them as an unofficial translation. No bulk translation runs during `make run`. Existing Japanese files are left untouched; delete one file to regenerate that item.

`ja/` is ignored by Git. Review an unofficial translation before quoting or publishing it. The official PDF states that rights in its translation are reserved, so this repository does not commit the PDF or extracted text.

## Sources

See `sources.json` for the original URLs. The official Japanese publication is [NIST CSWP 29 jpn](https://www.nist.gov/publications/nist-cybersecurity-framework-csf-20-japanese-translation).

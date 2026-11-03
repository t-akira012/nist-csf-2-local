# NIST CSF 2.0 local reference

[日本語](AGENTS.ja.md)

Use `generated/index.json` to find an exact CSF ID, then read its `generated/sections/<ID>.md` file. Read only the items needed for the current design. Do not infer a control from its ID or from memory.

For Japanese, find the ID in `ja/index.md` and open its link to NIST's official Japanese PDF. The link points to a PDF page; locate the ID on that page. The Japanese publication does not include the English Reference Tool's implementation examples.

Do not run `make run` during ordinary reference work. It downloads and rebuilds the English corpus and is an explicit maintenance action.

CSF outcomes describe desired results, not mandatory AWS resources or products. Select relevant outcomes for the task, then choose the least complex implementation that meets them.

# NIST CSF 2.0 local reference

[日本語](AGENTS.ja.md)

Use `generated/index.json` to find an exact CSF ID, then read its `generated/sections/<ID>.md` file. Read only the items needed for the current design. Do not infer a control from its ID or from memory.

For Japanese, read `ja/<ID>.md` if present. If absent and the user needs Japanese, run `make ja ID=<ID>` for that item only. The CSF core wording in this file comes from NIST's official Japanese translation. Implementation examples, if present, are translated by Codex on demand and labeled as unofficial. Do not present them as NIST's official Japanese wording.

Do not run `make run` during ordinary reference work. It downloads and rebuilds the corpus and is an explicit maintenance action. Do not translate the full corpus in advance.

CSF outcomes describe desired results, not mandatory AWS resources or products. Select relevant outcomes for the task, then choose the least complex implementation that meets them.

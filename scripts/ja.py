"""Write one Japanese CSF item, using NIST wording and translating examples on demand."""

import argparse
import json
import re
import subprocess
import tempfile
from pathlib import Path

from build import ROOT, OUT, ID_RE


FUNCTION = re.compile(r"^(?:統治|識別|防御|検知|対応|復旧)（([A-Z]{2})）[:：]")
CATEGORY = re.compile(r"^•\s+.+?（([A-Z]{2}\.[A-Z]{2})）[:：]")
SUBCATEGORY = re.compile(r"^\s+o\s+([A-Z]{2}\.[A-Z]{2}-\d{2})[:：]")
PAGE_NOISE = re.compile(r"^(?:NIST CSWP 29 jpn|2024年2月26日|\s*\d+\s*)$")


def official_japanese(pdf):
    text = subprocess.run(["pdftotext", "-layout", str(pdf), "-"],
                          check=True, capture_output=True, text=True).stdout
    start = text.find("統治（GV）：")
    end = text.find("附属書 B. CSF ティア", start)
    if start < 0 or end < 0:
        raise ValueError("Could not locate the official Japanese CSF core in the PDF")
    result = {}
    current = None
    for line in text[start:end].splitlines():
        if "NIST CSWP 29 jpn" in line or PAGE_NOISE.fullmatch(line.strip()):
            continue
        marker = FUNCTION.match(line) or CATEGORY.match(line) or SUBCATEGORY.match(line)
        if marker:
            current = marker.group(1)
            result[current] = [line.strip()]
        elif current and line.strip():
            result[current].append(line.strip())
    return {ident: "".join(parts) for ident, parts in result.items()}


def translate_examples(ident, english):
    prompt = ("Translate only the following NIST CSF 2.0 implementation examples into Japanese. "
              "Preserve example labels (Ex1, Ex2, etc.), IDs, order, and meaning. "
              "Return only the translated examples as Markdown; no preface, commentary, or core outcome. "
              "This is an unofficial translation of examples, separate from NIST's official Japanese core.\n\n"
              f"ID: {ident}\n\n{english}\n")
    with tempfile.TemporaryDirectory() as temp:
        output = Path(temp) / "translation.md"
        print(f"Translating examples for {ident} with Codex", flush=True)
        subprocess.run(["codex", "exec", "--sandbox", "read-only",
                        "--output-last-message", str(output), "-"],
                       input=prompt, text=True, cwd=ROOT, check=True)
        result = output.read_text(encoding="utf-8").strip()
    if not result or not set(re.findall(r"Ex\d+", english)).issubset(set(re.findall(r"Ex\d+", result))):
        raise ValueError("Codex translation is empty or omitted an example label")
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", required=True)
    args = parser.parse_args()
    ident = args.id.upper()
    if not ID_RE.fullmatch(ident):
        parser.error("ID must be a CSF Function, Category, or Subcategory ID")
    index = json.loads((OUT / "index.json").read_text(encoding="utf-8"))
    if ident not in index["items"]:
        parser.error(f"ID not found in local CSF core: {ident}")
    destination = ROOT / "ja" / f"{ident}.md"
    if destination.exists():
        print(f"Already exists: {destination}. Delete it to regenerate.", flush=True)
        return
    japanese = official_japanese(OUT / "source" / "csf2-jpn.pdf")
    if ident not in japanese:
        raise ValueError(f"Official Japanese wording not found for {ident}; no translation was substituted")
    english = (ROOT / index["items"][ident]["path"]).read_text(encoding="utf-8")
    match = re.search(r"^## Implementation examples\n\n(.+)$", english, re.M | re.S)
    lines = [f"# {ident}", "", "## CSF コア（NIST 公式和訳）", "", japanese[ident], "",
             f"出典: {index['sources']['japanese_core']['landing_page']}", ""]
    if match:
        translated = translate_examples(ident, match.group(1).strip())
        lines += ["## 実装例（Codex による非公式訳）", "", translated, "",
                  f"英語原文: {index['sources']['english_core']['url']}", ""]
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {destination}", flush=True)


if __name__ == "__main__":
    main()

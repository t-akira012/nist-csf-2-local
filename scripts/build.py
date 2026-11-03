"""Fetch official CSF 2.0 sources and make an ID-addressable local core."""

import argparse
import hashlib
import json
import re
import subprocess
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "generated"
NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
ID_RE = re.compile(r"^[A-Z]{2}(?:\.[A-Z]{2}(?:-\d{2})?)?$")


def fetch(url, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    print(f"Downloading {url} -> {path}", flush=True)
    subprocess.run(["curl", "--fail", "--location", "--show-error", url, "--output", str(path)], check=True)
    print(f"Saved {path} ({path.stat().st_size} bytes)", flush=True)


def workbook_rows(path):
    with zipfile.ZipFile(path) as archive:
        strings_root = ET.fromstring(archive.read("xl/sharedStrings.xml"))
        strings = ["".join(t.text or "" for t in node.findall(".//m:t", NS))
                   for node in strings_root.findall("m:si", NS)]
        sheet = ET.fromstring(archive.read("xl/worksheets/sheet2.xml"))
        for row in sheet.findall(".//m:sheetData/m:row", NS):
            values = {}
            for cell in row.findall("m:c", NS):
                value = cell.find("m:v", NS)
                if value is None:
                    continue
                column = re.match(r"[A-Z]+", cell.attrib["r"]).group()
                values[column] = strings[int(value.text)] if cell.get("t") == "s" else value.text
            yield values


def parse_core(path):
    entries = []
    function = category = None
    for row in workbook_rows(path):
        if "A" in row:
            match = re.match(r"^(.+?) \(([A-Z]{2})\):\s*(.+)$", row["A"], re.S)
            if match:
                title, ident, statement = match.groups()
                function, category = ident, None
                entries.append(dict(id=ident, level="function", title=title, statement=statement.strip(), parent=None))
        if "B" in row:
            match = re.match(r"^(.+?) \(([A-Z]{2}\.[A-Z]{2})\):\s*(.+)$", row["B"], re.S)
            if match:
                title, ident, statement = match.groups()
                if ident.split(".")[0] != function:
                    raise ValueError(f"Category without matching function: {ident}")
                category = ident
                if not statement.startswith("[Withdrawn:"):
                    entries.append(dict(id=ident, level="category", title=title, statement=statement.strip(), parent=function))
        if "C" in row:
            match = re.match(r"^([A-Z]{2}\.[A-Z]{2}-\d{2}):\s*(.+)$", row["C"], re.S)
            if match:
                ident, statement = match.groups()
                if ident.split("-")[0] != category:
                    raise ValueError(f"Subcategory without matching category: {ident}")
                if not statement.startswith("[Withdrawn:"):
                    entries.append(dict(id=ident, level="subcategory", title=ident,
                                        statement=statement.strip(), parent=category,
                                        examples=(row.get("D") or "").strip()))
    ids = [item["id"] for item in entries]
    if len(ids) != len(set(ids)) or any(not ID_RE.fullmatch(x) for x in ids):
        raise ValueError("Invalid or duplicate CSF IDs")
    counts = {level: sum(x["level"] == level for x in entries)
              for level in ("function", "category", "subcategory")}
    if counts != {"function": 6, "category": 22, "subcategory": 106}:
        raise ValueError(f"Unexpected CSF 2.0 core size: {counts}")
    return entries


def write_core(entries, sources, source_hashes):
    sections = OUT / "sections"
    sections.mkdir(parents=True, exist_ok=True)
    index = {"schema_version": 1, "sources": sources, "sha256": source_hashes, "items": {}}
    for item in entries:
        ident = item["id"]
        path = sections / f"{ident}.md"
        lines = [f"# {ident} — {item['title']}", "", f"Level: {item['level']}"]
        if item["parent"]:
            lines.append(f"Parent: {item['parent']}")
        lines += [f"Source: {sources['english_core']['url']}", "", item["statement"], ""]
        if item.get("examples"):
            lines += ["## Implementation examples", "", item["examples"], ""]
        path.write_text("\n".join(lines), encoding="utf-8")
        index["items"][ident] = {"level": item["level"], "title": item["title"],
                                  "parent": item["parent"], "path": str(path.relative_to(ROOT))}
    (OUT / "index.json").write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(entries)} ID-addressable sections and generated/index.json", flush=True)


def validate():
    index = json.loads((OUT / "index.json").read_text(encoding="utf-8"))
    entries = parse_core(OUT / "source" / "csf2.xlsx")
    if set(index["items"]) != {item["id"] for item in entries}:
        raise ValueError("Index does not match English source")
    from ja import official_japanese
    if set(official_japanese(OUT / "source" / "csf2-jpn.pdf")) != set(index["items"]):
        raise ValueError("Japanese CSF core IDs do not match the English CSF 2.0 core")
    for ident, meta in index["items"].items():
        if not (ROOT / meta["path"]).is_file():
            raise ValueError(f"Missing section: {ident}")
    for key, filename in (("english_core", "csf2.xlsx"), ("japanese_core", "csf2-jpn.pdf")):
        digest = hashlib.sha256((OUT / "source" / filename).read_bytes()).hexdigest()
        if digest != index["sha256"][key]:
            raise ValueError(f"Source hash changed: {filename}")
    print(f"Validated {len(entries)} sections, Japanese IDs, and both source hashes", flush=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--validate", action="store_true")
    args = parser.parse_args()
    if args.validate:
        validate()
        return
    sources = json.loads((ROOT / "sources.json").read_text(encoding="utf-8"))
    filenames = {"english_core": "csf2.xlsx", "japanese_core": "csf2-jpn.pdf"}
    hashes = {}
    for key, filename in filenames.items():
        path = OUT / "source" / filename
        fetch(sources[key]["url"], path)
        hashes[key] = hashlib.sha256(path.read_bytes()).hexdigest()
    entries = parse_core(OUT / "source" / "csf2.xlsx")
    write_core(entries, sources, hashes)


if __name__ == "__main__":
    main()

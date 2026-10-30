"""Offline documentation integrity: local links/anchors, fences and linked SVG XML."""

from __future__ import annotations
import html
from html.parser import HTMLParser
from pathlib import Path
import re
import unicodedata
from urllib.parse import unquote, urlsplit
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
DOCUMENTS = [
    "README.md",
    "docs/architecture.md",
    "docs/evaluation.md",
    "docs/limitations.md",
    "docs/methodology.md",
    "docs/trade-offs.md",
    "examples/README.md",
]


def prose(text: str, path: Path) -> str:
    lines = []
    opened = None
    for line in text.splitlines():
        match = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line)
        if match:
            marker, tail = match.groups()
            if opened is None:
                opened = (marker[0], len(marker))
            elif (
                marker[0] == opened[0] and len(marker) >= opened[1] and not tail.strip()
            ):
                opened = None
            continue
        if opened is None:
            lines.append(line)
    if opened is not None:
        raise ValueError(f"{path}: unclosed code fence")
    return "\n".join(lines)


def anchors(text: str) -> set[str]:
    result = set()
    counts = {}
    for line in text.splitlines():
        heading = re.match(r"^ {0,3}#{1,6}\s+(.+?)(?:\s+#+)?$", line)
        if not heading:
            continue
        slug = html.unescape(re.sub(r"<[^>]+>", "", heading[1])).lower()
        slug = "".join(
            c
            for c in slug
            if c in "_-" or c.isspace() or unicodedata.category(c)[0] in {"L", "N", "M"}
        ).replace(" ", "-")
        count = counts.get(slug, 0)
        counts[slug] = count + 1
        result.add(f"{slug}-{count}" if count else slug)
    return result


class Targets(HTMLParser):
    def __init__(self):
        super().__init__()
        self.paths = []

    def handle_starttag(self, tag, attrs):
        for key, value in attrs:
            if value and key in {"href", "src"}:
                self.paths.append(value)
            elif value and key == "srcset":
                self.paths.extend(v.strip().split()[0] for v in value.split(","))


def validate(root: Path, documents: list[str]) -> tuple[int, int]:
    count = 0
    svg = set()
    for name in documents:
        path = root / name
        text = prose(path.read_text(encoding="utf-8"), path)
        parser = Targets()
        parser.feed(text)
        links = parser.paths + re.findall(r"!?\[[^\]\n]*\]\(([^\n)]+)\)", text)
        for target in links:
            target = html.unescape(target.strip().strip("<>"))
            url = urlsplit(target)
            if url.scheme or url.netloc:
                continue
            destination = (
                (path.parent / unquote(url.path)).resolve()
                if url.path
                else path.resolve()
            )
            if not destination.is_relative_to(root.resolve()):
                raise ValueError(f"{name}: link leaves repository: {target}")
            if not destination.exists():
                raise ValueError(f"{name}: missing target {target}")
            if url.fragment and destination.suffix.lower() == ".md":
                available = anchors(
                    prose(destination.read_text(encoding="utf-8"), destination)
                )
                if unquote(url.fragment) not in available:
                    raise ValueError(f"{name}: missing anchor {target}")
            if destination.suffix.lower() == ".svg":
                svg.add(destination)
            count += 1
    for path in svg:
        ET.parse(path)
    return count, len(svg)


if __name__ == "__main__":
    count, svg = validate(ROOT, DOCUMENTS)
    print(
        f"Validated {len(DOCUMENTS)} documents, {count} local links/anchors and {svg} SVG assets; balanced fences. External URLs and factual/private claims are not validated."
    )

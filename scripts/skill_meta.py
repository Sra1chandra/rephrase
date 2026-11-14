"""Read SKILL.md as the source of truth. Hooks and sync import this."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "SKILL.md"


def skill_text() -> str:
    return SKILL.read_text(encoding="utf-8")


def frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end < 0:
        return {}
    block = text[3:end]
    out: dict[str, str] = {}
    key = None
    chunks: list[str] = []
    for line in block.splitlines():
        if line.startswith("  ") and key:
            chunks.append(line.strip())
            continue
        if ":" in line and not line.startswith(" "):
            if key:
                out[key] = " ".join(chunks).strip()
            key, _, rest = line.partition(":")
            key = key.strip()
            chunks = [rest.strip().strip(">").strip()]
    if key:
        out[key] = " ".join(chunks).strip()
    return out


def description() -> str:
    return re.sub(r"\s+", " ", frontmatter(skill_text()).get("description", ""))


def trigger_phrases() -> list[str]:
    desc = description()
    m = re.search(
        r"Use when the user says (.+?)(?:,? or asks\b|\. Invoke|\.\s|$)",
        desc,
        re.I,
    )
    if not m:
        return []
    parts = [p.strip().strip(".") for p in m.group(1).split(",")]
    return [p for p in parts if p]


def trigger_regex() -> re.Pattern[str]:
    alts = [re.escape(p) for p in trigger_phrases()]
    if not alts:
        alts = ["rephrase"]
    return re.compile(r"(?:^|[^\w])(" + "|".join(alts) + r")(?:[^\w]|$)", re.I)


def stock_phrases() -> list[str]:
    body = skill_text()
    for line in body.splitlines():
        if line.startswith("- `delve`"):
            return [p.strip() for p in re.findall(r"`([^`]+)`", line)]
    return []


def knobs() -> dict[str, str]:
    out: dict[str, str] = {}
    in_table = False
    for line in skill_text().splitlines():
        if line.startswith("| Knob"):
            in_table = True
            continue
        if in_table and line.startswith("|---"):
            continue
        if in_table and line.startswith("|"):
            cells = [c.strip() for c in line.strip("|").split("|")]
            if len(cells) >= 2:
                out[cells[0]] = cells[1]
        elif in_table:
            break
    return out

#!/usr/bin/env python3
"""Fail-open hook: if the user asked to rephrase, point the agent at SKILL.md.

Trigger phrases come from SKILL.md (Use when the user says ...).
Edit the skill description, not this file.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


def _load_meta():
    root = Path(__file__).resolve().parent.parent
    sys.path.insert(0, str(root / "scripts"))
    from skill_meta import SKILL, trigger_regex  # noqa: WPS433

    return SKILL, trigger_regex()


def prompt_from(data: dict) -> str:
    chunks: list[str] = []

    def walk(obj) -> None:
        if isinstance(obj, str):
            chunks.append(obj)
        elif isinstance(obj, dict):
            for v in obj.values():
                walk(v)
        elif isinstance(obj, list):
            for v in obj:
                walk(v)

    for key in ("prompt", "content", "text", "user_prompt", "message"):
        if key in data:
            walk(data[key])
    return "\n".join(chunks)


def main() -> int:
    raw = sys.stdin.read()
    try:
        data = json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError:
        print("{}")
        return 0
    if not isinstance(data, dict):
        print("{}")
        return 0
    try:
        skill, trigger = _load_meta()
    except Exception:
        print("{}")
        return 0
    if not trigger.search(prompt_from(data)):
        print("{}")
        return 0
    ctx = (
        "rephrase is on for this turn. Read and follow "
        f"{skill}. Prose only. Keep every number, identifier, quote, and fact. "
        "Do not invent work. Load references/ai-tells.md, "
        "references/ste-structure.md, and references/scan.md before you write."
    )
    print(json.dumps({"additional_context": ctx}))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception:
        print("{}")
        raise SystemExit(0)

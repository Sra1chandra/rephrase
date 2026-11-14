#!/usr/bin/env python3
"""Fail if SKILL.md, hooks, and evals drifted.

Same job as SimpleEnglish evals/check_numbers.py: the published contract
must match the files. Run after you edit SKILL.md.

  python3 scripts/check_sync.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from skill_meta import description, knobs, stock_phrases, trigger_phrases  # noqa: E402

EVALS = ROOT / "evals"
problems: list[str] = []


def expect(ok: bool, msg: str) -> None:
    if not ok:
        problems.append(msg)


def keep_in_text(text: str, item: str) -> bool:
    if re.search(r"\s", item) or any(ch in item for ch in "%./()`"):
        return item in text
    return re.search(rf"\b{re.escape(item)}\b", text) is not None


def eval_dirs() -> list[Path]:
    return sorted(p for p in EVALS.iterdir() if p.is_dir() and (p / "keep.json").is_file())


def check_install() -> None:
    project = ROOT / ".cursor" / "skills" / "rephrase" / "SKILL.md"
    expect(project.is_file(), "missing .cursor/skills/rephrase/SKILL.md; run ./scripts/install.sh")
    expect(
        not project.is_symlink(),
        ".cursor/skills/rephrase/SKILL.md is a symlink; slash picker skips it. run ./scripts/install.sh (hard link)",
    )
    claude = Path.home() / ".claude" / "skills" / "rephrase" / "SKILL.md"
    expect(
        claude.is_file(),
        "missing ~/.claude/skills/rephrase/SKILL.md (this is how /humanizer loads). run ./scripts/install.sh",
    )


def check_triggers() -> None:
    phrases = trigger_phrases()
    expect(bool(phrases), "SKILL.md description has no 'Use when the user says' list")
    desc = description().lower()
    for p in phrases:
        expect(p.lower() in desc, f"trigger {p!r} missing from parsed description")
    inject = (ROOT / "hooks" / "inject.py").read_text(encoding="utf-8")
    expect(
        "trigger_regex" in inject and "skill_meta" in inject,
        "hooks/inject.py must build TRIGGER from skill_meta (SKILL.md), not a private regex",
    )


def check_stock() -> None:
    phrases = stock_phrases()
    expect("leverage" in phrases, "SKILL.md Don't-list must still include leverage")
    check_py = (ROOT / "scripts" / "check.py").read_text(encoding="utf-8")
    for p in phrases:
        stem = p.split()[0].lower()
        expect(stem in check_py.lower(), f"scripts/check.py STOCK missing skill word {p!r}")


def check_knobs() -> None:
    k = knobs()
    expect(k.get("Instruction sentence", "").startswith("20"), f"instruction knob drifted: {k}")
    expect(k.get("Description sentence", "").startswith("25"), f"description knob drifted: {k}")
    expect("6" in k.get("Paragraph", ""), f"paragraph knob drifted: {k}")
    expect("never" in k.get("Em dash / en dash / `;`", "").lower(), "dash knob must stay never, or update check.py")


def check_evals() -> None:
    ids = []
    for folder in eval_dirs():
        ids.append(folder.name)
        keep = json.loads((folder / "keep.json").read_text(encoding="utf-8"))
        source = (folder / "source.md").read_text(encoding="utf-8")
        expect((folder / "prompt.md").is_file(), f"{folder.name}: missing prompt.md")
        expect((folder / "case.yaml").is_file(), f"{folder.name}: missing case.yaml")
        for item in keep.get("must_keep", []):
            expect(
                keep_in_text(source, item),
                f"{folder.name}: must_keep {item!r} not in source.md",
            )
        for item in keep.get("must_not_invent", []):
            expect(
                not keep_in_text(source, item),
                f"{folder.name}: must_not_invent {item!r} is already in source.md",
            )
        yaml = (folder / "case.yaml").read_text(encoding="utf-8")
        yaml_l = yaml.lower()
        for item in keep.get("must_keep", []):
            token = item.strip("`")
            expect(
                token.lower() in yaml_l or item.lower() in yaml_l,
                f"{folder.name}: case.yaml does not mention must_keep {item!r}",
            )
    jsonl_path = EVALS / "cases.jsonl"
    jsonl_ids = []
    for line in jsonl_path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            jsonl_ids.append(json.loads(line)["id"])
    expect(
        sorted(ids) == sorted(jsonl_ids),
        f"cases.jsonl ids {sorted(jsonl_ids)} != eval folders {sorted(ids)}",
    )
    readme = (EVALS / "README.md").read_text(encoding="utf-8")
    for name in ids:
        expect(name in readme, f"evals/README.md does not list {name}")


def main() -> int:
    check_install()
    check_triggers()
    check_stock()
    check_knobs()
    check_evals()
    if problems:
        print("SYNC MISMATCH")
        for p in problems:
            print(f" - {p}")
        print("Edit SKILL.md knobs/triggers, then keep.json / inject via skill_meta, then re-run.")
        return 1
    print("check_sync OK: SKILL.md, hooks, and evals agree")
    return 0


if __name__ == "__main__":
    sys.exit(main())

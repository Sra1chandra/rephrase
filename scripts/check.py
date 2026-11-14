#!/usr/bin/env python3
"""Heuristic linter + fidelity check for rephrase.

Not an AI detector. Not ASD-STE100 compliance.

  python3 scripts/check.py FILE
  python3 scripts/check.py --against source.md rewritten.md
  python3 scripts/check.py --keep evals/rewrite-cache-readme/keep.json rewritten.md
  python3 scripts/check.py --self-test
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

STOCK = re.compile(
    r"\b(?:delve|leverag(?:e|es|ing)|utilize|utilise|utilizing|robust|"
    r"seamless|seamlessly|pivotal|tapestry|landscape|testament|underscore|"
    r"showcase|groundbreaking|it's worth noting|it should be noted|"
    r"let's dive in)\b",
    re.I,
)
NOT_X_BUT_Y = re.compile(
    r"\b(?:it'?s|it is|this is|that'?s)\s+not\s+(?:just|only|merely|simply)\b"
    r"|\bnot\s+(?:just|only|merely)\b[^.]{0,80}\bbut\b",
    re.I,
)
CHATBOT = re.compile(
    r"\b(?:great question|i hope this helps|let me know if|"
    r"would you like me to|here'?s what you need to know|let'?s dive)\b",
    re.I,
)
NUMBER = re.compile(
    r"\b\d[\d,]*(?:\.\d+)?%|\b\d[\d,]*(?:\.\d+)?\s*(?:ms|s|kb|mb|gb|tb|px)\b|\b\d[\d,]*(?:\.\d+)?\b",
    re.I,
)
BACKTICK = re.compile(r"`[^`]+`")
ENVISH = re.compile(r"\b[A-Z][A-Z0-9_]{2,}\b")


def prose_only(text: str) -> str:
    return BACKTICK.sub(" CODE ", text)


def has_item(text: str, item: str) -> bool:
    if re.search(r"\s", item) or any(ch in item for ch in "%./()`"):
        return item.lower() in text.lower()
    return re.search(rf"\b{re.escape(item)}\b", text, re.I) is not None


def findings(text: str) -> list[str]:
    out = []
    prose = prose_only(text)
    if "—" in prose or "–" in prose or " -- " in prose:
        out.append("dash: em/en dash or ' -- ' in prose")
    if ";" in prose:
        out.append("semicolon")
    if STOCK.search(text):
        out.append(f"stock-word: {STOCK.search(text).group(0)}")
    if NOT_X_BUT_Y.search(text):
        out.append("not-x-but-y")
    if CHATBOT.search(text):
        out.append(f"chatbot: {CHATBOT.search(text).group(0)}")
    return out


def tokens_from_source(source: str) -> list[str]:
    found = []
    for rx in (BACKTICK, NUMBER, ENVISH):
        for m in rx.findall(source):
            if m in found:
                continue
            found.append(m)
    return found


def missing_keep(text: str, items: list[str]) -> list[str]:
    return [item for item in items if not has_item(text, item)]


def unexpected(text: str, items: list[str]) -> list[str]:
    return [item for item in items if has_item(text, item)]


def load_keep(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def check_pair(source: str, dest: str, keep: dict | None) -> list[str]:
    problems = findings(dest)
    items = list(keep.get("must_keep", []) if keep else [])
    if keep is None or keep.get("auto_from_source", True):
        for tok in tokens_from_source(source):
            if tok not in items:
                items.append(tok)
    problems.extend(f"lost-fact: {x}" for x in missing_keep(dest, items))
    if keep:
        problems.extend(f"forbidden: {x}" for x in unexpected(dest, keep.get("must_absent", [])))
        problems.extend(f"invented: {x}" for x in unexpected(dest, keep.get("must_not_invent", [])))
    return problems


def self_test() -> int:
    source = (
        "sqlpipe stops with `dial tcp: i/o timeout` on port 5432. "
        "TTL is 300 seconds. Set CACHE_TTL."
    )
    good = (
        "sqlpipe stops with `dial tcp: i/o timeout` when it cannot reach port 5432. "
        "The TTL is 300 seconds. Override it with CACHE_TTL."
    )
    bad_num = good.replace("5432", "5433")
    bad_dash = "Auth is done — then we ship."
    bad_invent = good + " Next we continue to iterate."
    keep = {
        "must_keep": ["5432", "`dial tcp: i/o timeout`", "300", "CACHE_TTL"],
        "must_absent": ["leverage"],
        "must_not_invent": ["continue to iterate"],
        "auto_from_source": False,
    }
    assert check_pair(source, good, keep) == [], check_pair(source, good, keep)
    lost = check_pair(source, bad_num, keep)
    assert any(x.startswith("lost-fact: 5432") for x in lost), lost
    dash = findings(bad_dash)
    assert any("dash" in x for x in dash), dash
    inv = check_pair(source, bad_invent, keep)
    assert any(x.startswith("invented:") for x in inv), inv
    from check_sync import main as sync_main

    sync = sync_main()
    if sync != 0:
        return sync
    print("self-test OK")
    return 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="*")
    ap.add_argument("--against", help="source file; dest must keep its numbers, ticks, ENV names")
    ap.add_argument("--keep", help="keep.json path")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args(argv)
    if args.self_test:
        return self_test()
    if not args.files:
        ap.error("FILE required")
    dest = Path(args.files[-1]).read_text(encoding="utf-8")
    source = Path(args.against).read_text(encoding="utf-8") if args.against else ""
    keep = load_keep(Path(args.keep)) if args.keep else None
    if args.against or keep:
        problems = check_pair(source, dest, keep)
    else:
        problems = findings(dest)
    for p in problems:
        print(p)
    if problems:
        print(f"{len(problems)} problem(s)")
        return 1
    print("OK")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

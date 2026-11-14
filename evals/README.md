# Evals

Same job as ste80-humanizer and SimpleEnglish `check_numbers`: the rewrite must keep every number and fact. Style graders sit next to that.

This is not a live model harness. You run the skill by hand (or in Cursor), save the rewrite, then score it.

## 1. Deterministic check (facts + numbers)

```bash
python3 scripts/check.py --self-test

python3 scripts/check.py --keep evals/rewrite-cache-readme/keep.json \
  --against evals/rewrite-cache-readme/source.md rewritten.md
```

Exit 1 if a keep-token is missing, a number changed, a forbidden phrase appeared, or the dest invented a listed phrase.

## 2. Case folders (ste80 layout)

Each folder:

| File | Role |
|---|---|
| `prompt.md` | What you paste into the agent |
| `source.md` | The source prose (same facts as the prompt) |
| `keep.json` | Tokens that must survive; phrases that must not appear |
| `case.yaml` | Human summary of expected outcome |
| `graders/*.md` | Extra pass/fail questions (LLM or eyeball) |

Cases:

1. `rewrite-cache-readme` - numbers and identifiers stay
2. `slack-no-invent` - empty Next stays empty
3. `procedure-timeout` - error string and port stay exact
4. `code-hands-off` - TypeScript body stays; comment is cleaned

After you edit `SKILL.md` (knobs, triggers, banned words):

```bash
python3 scripts/check_sync.py
```

## 3. Blind rubric

`cases.jsonl` + `rubric.md` are for a later model judge (i-have-adhd style). Do not publish scores until baseline and candidate used the same cases.

## Release bar

A case passes only if:

1. `scripts/check.py --keep ... --against source.md dest` exits 0
2. Every grader in that folder is a yes
3. No invented Next/Blocked/source

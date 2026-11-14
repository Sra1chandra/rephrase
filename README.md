# rephrase

Owned writing skill. 80% STE structure, anti-slop tells, scan-first layout.
Text only. Facts and numbers stay. Invoke with `/rephrase`.

## Why `/rephrase` was missing

`/humanizer` shows in `/` because it is a **real folder**:

```text
~/.claude/skills/humanizer/SKILL.md
```

Cursor (and Claude Code) load skills from that path. This repo had only a
**symlink** at `.cursor/skills/rephrase/SKILL.md`. The slash picker skips that.

`scripts/install.sh` matches the humanizer install: `SKILL.md` is a regular
file (hard link), and `~/.claude/skills/rephrase` points at this repo.

## Installation

From this repo:

```bash
chmod +x scripts/install.sh
./scripts/install.sh
```

That does what humanizer's README does, locally:

```bash
mkdir -p ~/.claude/skills
ln -sfn /absolute/path/to/rephrase ~/.claude/skills/rephrase
```

Also installs:

| Path | Why |
|---|---|
| `~/.claude/skills/rephrase` | Same discovery path as `/humanizer` |
| `~/.cursor/skills/rephrase` | Cursor user skills |
| `.cursor/skills/rephrase/SKILL.md` | Project skill, hard-linked file |
| `.claude/skills/rephrase/SKILL.md` | Claude Code project skill |

Then **new Agent chat**. Type `/reph`. Pick **rephrase**. Paste text.

Keep it on for the session: `/rephrase` then Option+Enter (Custom Mode).

## Usage

```text
/rephrase

[paste text]
```

Optional: `Slack` or `doc` in the same message. That only changes length, not a heading kit.

After you edit `SKILL.md` knobs or triggers:

```bash
python3 scripts/check_sync.py
python3 scripts/check.py --self-test
```

## Layout

```text
SKILL.md                 # you own this
references/
examples.md
scripts/check.py
scripts/check_sync.py
scripts/install.sh
evals/
hooks/
```

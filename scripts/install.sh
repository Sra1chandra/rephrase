#!/bin/sh
# Install rephrase the same way /humanizer is loaded: a real SKILL.md
# under ~/.claude/skills/<name>/ (Cursor also scans that path).
set -e
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)

link_skill_dir() {
  dest=$1
  mkdir -p "$dest"
  rm -f "$dest/SKILL.md"
  ln "$ROOT/SKILL.md" "$dest/SKILL.md"
  rm -f "$dest/examples.md" "$dest/references" "$dest/scripts"
  ln -sfn "$ROOT/examples.md" "$dest/examples.md"
  ln -sfn "$ROOT/references" "$dest/references"
  ln -sfn "$ROOT/scripts" "$dest/scripts"
}

# Project (Cursor + Claude Code in-repo discovery). Hard-link SKILL.md so
# the indexer sees a regular file, not a 17-byte symlink.
link_skill_dir "$ROOT/.cursor/skills/rephrase"
link_skill_dir "$ROOT/.claude/skills/rephrase"
link_skill_dir "$ROOT/.agents/skills/rephrase"

# User (this is why /humanizer appears: ~/.claude/skills/humanizer/SKILL.md).
mkdir -p "$HOME/.claude/skills" "$HOME/.cursor/skills" "$HOME/.agents/skills"
ln -sfn "$ROOT" "$HOME/.claude/skills/rephrase"
ln -sfn "$ROOT" "$HOME/.cursor/skills/rephrase"
ln -sfn "$ROOT" "$HOME/.agents/skills/rephrase"

echo "installed:"
echo "  $HOME/.claude/skills/rephrase -> $ROOT"
echo "  $HOME/.cursor/skills/rephrase -> $ROOT"
echo "  $ROOT/.cursor/skills/rephrase/SKILL.md (hard link)"
echo "Restart Agent chat, type /reph"

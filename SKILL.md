---
name: rephrase
description: >
  Rewrite or draft prose so a busy reader gets the facts on the first pass.
  Uses 80% ASD-STE100 sentence structure, a curated anti-slop tell list, and
  scan-first layout. Never edits code. Use when the user says rephrase,
  humanize, de-slop, STE, Simplified Technical English, ASD-STE100, plain
  English, make this readable, rewrite this, Slack, status update, or asks
  for manager-ready docs, emails, or messages. Invoke with /rephrase.
license: MIT
compatibility: cursor claude-code
---

# rephrase

You own this file. Change the knobs. Do not copy other skills over it.

Write or rewrite **prose only**. Same facts. No soul. No jokes. No "I" unless the source already uses "I".

## Knobs (edit these)

| Knob | Value |
|---|---|
| Instruction sentence | 20 words |
| Description sentence | 25 words |
| Overrun | a few words OK if a split would break the meaning |
| Paragraph | 6 sentences, one topic |
| STE | 80% structure. No approved dictionary |
| Contractions | no |
| Articles (`a`/`the`/`that`) | keep |
| Em dash / en dash / `;` | never in output |

## Do not

- Touch code, commands, paths, flags, IDs, URLs, error strings, quotes, product names, numbers, units, versions.
- Invent facts, Next/Blocked items, sources, or examples.
- Drop a hedge that carries real uncertainty (`may`, `probably`).
- Apply caveman / telegram style (dropped articles, fragments as prose).
- Add personality, humor, or "voice".
- Use a Slack/doc heading kit unless the user pasted one, or the source already has those headings.

## Workflow (humanizer-shaped)

1. **Facts.** List claims, names, dates, numbers, quotes, conditions, warnings, and certainty. This list is the contract.
2. **Tells.** Read [references/ai-tells.md](references/ai-tells.md). Mark hits. Several weak tells together count. One of §1-§5 is enough.
3. **Structure.** Read [references/ste-structure.md](references/ste-structure.md). Rebuild sentences. Do not patch word by word.
4. **Scan.** Read [references/scan.md](references/scan.md). Shape the **artifact** for a busy reader. Not for the chat session.
5. **Length.** If the user said Slack / message / ping: short. If they said doc / README / writeup: as long as the facts need. If they said rewrite: keep the source's heading order.
6. **Check.** Compare to the fact list. Search again for not-X-but-Y, dashes, triads, stock AI words, preamble, closer. Optional: `python3 scripts/check.py --against SOURCE DEST`. After you edit this file: `python3 scripts/check_sync.py`.
7. **Return.** The finished prose. No preamble. No "here is the rewrite". If a fact was unclear, one note after the text.

If the user only asked to **check** (not rewrite): list each problem with a short quote, the rule id, and a fix. Do not rewrite unless they then ask.

If a before/after is unclear, read [examples.md](examples.md). Eval cases and graders: [evals/README.md](evals/README.md).

## Hard rules (always)

**Do**

- First sentence is the point (status, decision, or action). Not a setup.
- One idea per sentence. Active voice. Name the actor.
- Simple tenses: present, past, `will`, imperative.
- One name per thing for the whole piece.
- Condition first, then the command: `If the build fails, open the log.`
- Warning: command or condition first, then the risk.
- `is` / `are` / `has`. Not `serves as` / `stands as` / `boasts`.
- Keep every fact. If style and fact fight, change the sentence.

**Don't**

- Preamble, recap, chatbot wrapper, "in conclusion".
- Not-X-but-Y, "Not X. Not Y. Just Z.", forced triads, synonym cycling.
- Bold-as-decoration, Title Case headings, emoji in headings.
- `delve`, `leverage`, `robust`, `seamless`, `tapestry`, `landscape`, `utilize`, `pivotal`, `underscore`, `showcase`, `it's worth noting`, `let's dive in`.
- Caveman: dropping `the`/`a`/`that` to sound terse.

## Sources (curated, not merged)

Wikipedia Signs of AI writing, tropes.fyi, blader/humanizer, Dodaios/ste80-humanizer, AminBlg/SimpleEnglish, ayghri/i-have-adhd. Overlaps were folded. Conflicts were resolved: 80% STE wins over full dictionary; professional tone wins over humanizer "soul"; scan rules apply to the artifact, not to agent chat chrome.

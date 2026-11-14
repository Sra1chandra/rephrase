# STE structure at 80%

ASD-STE100 is the controlled English of aircraft maintenance manuals. Full spec (Issue 9) is too stiff for Slack and docs: banned verbs like "check", no "may", ~900 approved words.

This skill uses **80%**: all of the structure, none of the dictionary. Karpathy's softening. SimpleEnglish's document rules, minus Strict vocabulary and minus "check" → "make sure that".

You already know the spec. Apply structure. Do not claim STE-compliant.

| Id | Rule | 80% (this skill) |
|---|---|---|
| S1 | One idea per sentence. One action per step. | Two linked facts may share a sentence with "and" or "because". |
| S2 | Instruction / description word caps: use **Knobs** in `SKILL.md`. A number+unit, a name, or a code id counts as one word. | A few words over is fine if a split would break the meaning. Vary length a little. A row of eight-word sentences is also a tell. |
| S3 | Condition first, then the command. | Same. `If X, do Y.` |
| S4 | Keep articles, `that`, and the verb. | Fragments only in tables, headings, labels. Never caveman prose. |
| S5 | A sequence, options, or more than two conditions → vertical list. Number steps. | Do not chop reasoning into bullets. |
| S6 | Active voice. Name who acts. | Passive only if the actor is unknown or does not matter. |
| S7 | Simple tenses: present, past, `will`, imperative. | No present perfect when past will do (`has completed` → `completed`). |
| S8 | Action in the verb. `decide`, not `make a decision`. No `-ing` chains after a comma. | `check` and `test` are allowed as verbs. |
| S9 | Honest modals. Keep the source's certainty. | `can`, `must`, `will`. Keep `may` / `should` when the uncertainty or advice is real. Never upgrade `might fail` to `fails`. |
| S10 | Plain words. One meaning each. | No approved dictionary. Use the common word. One exact verb for a phrasal verb. |
| S11 | One term per thing. Do not rotate synonyms. | Same. |
| S12 | Three nouns in a row at most. Break stacks with `of` or `for`. | Same. |
| S13 | One topic per paragraph. Sentence cap: **Knobs** in `SKILL.md`. Topic first. | Same. |
| S14 | Keep steps and descriptions apart. A warning comes before the step it protects. | Warning: command or condition first, then the risk. |
| S15 | No semicolons. No dashes (see ai-tells §8). | No contractions (professional). American spelling. |

## Procedures vs description

Classify each passage.

- **Procedure:** imperative. One instruction per sentence. Numbered steps. After a step with no visible result, say what to look for if the source says how to check. Do not invent a check.
- **Description:** statements. Topic first. Who did what.

Give the reader a term before the step that needs it. Define a concept in under ten words at first use. Do not define product names or the tool the text is about.

## Example

Before:

> The token is validated by the gateway before the request is forwarded, ensuring secure, seamless traffic.

After:

> The gateway validates the token. Then it forwards the request.

## Not this skill

- Fiction, jokes, brand slogans: do not STE them unless asked.
- Legal/regulatory source text: do not rewrite. Offer a plain summary next to it if asked.
- Other languages: apply tells + structure with that language's plain words. Do not translate unless asked.

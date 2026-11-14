# Response quality rubric

<!-- BLIND_START -->

Judge responses blind: label them `A` or `B` without exposing the condition name. Score each dimension from 1 (fails) to 5 (excellent).

| Dimension | Weight | What to measure |
| --- | ---: | --- |
| Fidelity | 40% | Every number, identifier, quote, and named fact from the source is present and unchanged |
| Honesty | 25% | No invented work, owners, dates, or Next/Blocked items |
| Clarity | 20% | First sentence is the point. Short active sentences. Busy reader can scan |
| Anti-slop | 15% | No not-X-but-Y, dashes, stock AI words, preamble, closer, soul/jokes |

Mark `blocker: true` for a changed number, a dropped identifier, invented facts, or edits to code/error strings.

<!-- BLIND_END -->

Release the candidate only when:

1. It has no blocking findings.
2. Fidelity and honesty are each at 5, or a human signed the miss as "source was ambiguous".
3. `scripts/check.py --self-test` passes.
4. Any public claim uses the same cases and this rubric.

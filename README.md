# rephrase

Turns fluffy writing into something a busy person can read. Keeps the facts. Drops the padding.

Type `/rephrase`, paste your text, send.

## Before and after

**Update**

Before:

> I wanted to take a moment to share a quick update. It's not just a small fix — it's a pivotal step in our broader reliability journey. We leveraged the new gateway to ensure seamless, robust auth, highlighting our commitment to security. Next, we'll continue to iterate. Let me know if you have any questions!

After:

> Auth now goes through the new gateway. The gateway validates the token, then forwards the request.

**Slack**

Before:

> finished the auth PR. waiting on review from Sam. then ship behind the flag.

After:

> Auth PR is up. Waiting on Sam's review. After that, ship behind the flag.

**Cold email**

Before:

> In the realm of modern enterprise solutions, companies often struggle to streamline operations and elevate efficiency. I'd love to connect for a quick 15-minute sync to discuss how we can leverage synergy to drive robust results for your organization.

After:

> Many companies that buy enterprise software still find it hard to simplify operations and raise efficiency. I would like a 15-minute call to see if we can help your organization.

Numbers, names, and error messages stay as they were. Empty claims (like "we will continue to iterate") get dropped, not filled in.

## Install

In Cursor, open a new Agent chat and paste this:

```text
Install the writing skill from https://github.com/Sra1chandra/rephrase so I can use /rephrase.
Follow the install script in that repo. Then tell me when it is ready.
```

Open a **new** Agent chat after that. Type `/rephrase`. Paste your draft.

## Use

```text
/rephrase

[your text]
```

Add the word `Slack` if you want it short. Add `doc` if you want it longer. The facts stay the same either way.

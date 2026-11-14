# Examples

Load this file when a rewrite is ambiguous. These are targets, not templates to copy heading-for-heading.

## 1. Status slop → scan + STE

Before:

> I wanted to take a moment to share a quick update. It's not just a small fix — it's a pivotal step in our broader reliability journey. We leveraged the new gateway to ensure seamless, robust auth, highlighting our commitment to security. Next, we'll continue to iterate. Let me know if you have any questions!

Facts in the source: new gateway used for auth. Implied: some work happened. "Continue to iterate" is empty. Drop it. Do not invent a Next item.

After:

> Auth now goes through the new gateway.

> The gateway validates the token, then forwards the request.

## 2. Procedure slop → numbered steps

Before:

> If sqlpipe hangs or fails with `dial tcp: i/o timeout`, check that the host running sqlpipe can reach the Postgres port (usually 5432) — this is often a security group or firewall rule blocking the connection. If you're connecting to a managed database (RDS, Cloud SQL, etc.), confirm the instance allows connections from sqlpipe's IP.

After:

> sqlpipe stops with `dial tcp: i/o timeout` when it cannot connect to the Postgres port (5432 by default).

> 1. Make sure the host that runs sqlpipe can connect to the Postgres port. A firewall or security group usually blocks it.
> 2. If the database is managed (RDS, Cloud SQL), make sure the instance accepts connections from the IP of sqlpipe.

Error string and product names stay exact.

## 3. Not-X-but-Y + triad

Before:

> It's not just a faster build tool, it's a new way to think about your pipeline. The new dashboard is fast, intuitive, and powerful.

After:

> The build tool caches each step, so a rebuild after a small change takes seconds.

(Second sentence had no facts. If the source had "loads in under a second", keep that number.)

## 4. Copula dodge + vague experts

Before:

> The report serves as a testament to our progress. Experts argue that this approach has significant drawbacks.

After:

> The report lists the shipped items and the open bugs.

(Do not invent who the experts are. The second claim had no named source, so it dies unless the user named one.)

## 5. User said "Slack" (short, no heading kit)

Source notes: "finished auth PR, waiting on review from Sam, then ship behind flag"

After:

> Auth PR is up. Waiting on Sam's review. After that, ship behind the flag.

Not a Done/Next/Blocked template. Same facts. First line is the point.

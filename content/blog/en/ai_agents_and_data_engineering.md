## AI Agents and Data Engineering in 2026: What Teams Actually Do, What It Costs and What Changes

##### Published on {{PUBLISH_DATE}}

<!-- TITLE_IMAGE -->

![AI agents and data engineering in 2026](../../images/ai_agents_and_data_engineering_title_img.png)

*Technical article*

## From autocomplete to agents

Two years ago, "AI for developers" mostly meant autocomplete and a chat window. In 2026 the default tool is an **agent**: Claude Code, OpenAI Codex, GitHub Copilot's agent mode, Cursor, Gemini CLI and similar tools that read a repository, run commands, execute tests, edit many files and open pull requests, looping until a task is done or they get stuck.

Adoption has moved fast. In the [2026 Stack Overflow Developer Survey](https://stackoverflow.blog/2026/10/06/the-results-of-the-2026-developer-survey-are-here/) (over 30,000 respondents), 66% of developers who use AI tools use coding agents, Claude Code (66%) and GitHub Copilot (59%) are the most-used agents, and 73% of AI tool users use them every day. JetBrains' 2026 Developer Ecosystem research, covering more than 15,000 professional developers, reports [Claude Code's work adoption doubling during the first half of the year and Codex growing about fivefold](https://dev.to/jamilxt/claude-code-overtakes-github-copilot-what-jetbrains-survey-of-15000-developers-says-about-ai-3nhc). The exact numbers vary between surveys, but the direction doesn't.

Data platforms followed. Snowflake, Databricks and Google all now ship agents inside their products ([Snowflake's Cortex Code](https://www.snowflake.com/en/blog/cortex-code-governed-agent-data-stack/), [Databricks' agentic features in Lakeflow](https://www.databricks.com/blog/lakeflow-new-era-agentic-data-engineering) and Google's BigQuery data engineering agent), which write SQL, build pipelines and explain lineage using the platform's catalog and permissions.

This article is about what that means for data engineering specifically: what teams actually delegate to agents, the trade-offs, the security and privacy risks, what companies now expect, and the practices I'd recommend for adopting them. I use agents daily in my own work, including on the [EU company registry lakehouse](../projects/eu-company-registry.html) and this website, so some of the examples are first-hand.

## What data teams actually use agents for

Surveys of general developers say most AI use is still writing code in familiar areas (67% in the Stack Overflow survey) and debugging (61%), with only 20% using AI to deploy, operate or troubleshoot production systems. In data work, the tasks that consistently pay off are these:

**Writing and refactoring transformation code.** PySpark jobs, dbt models, SQL migrations and Airflow DAGs are well suited to agents: the patterns are well known, the code is testable and the feedback loop (run the tests, read the error, fix) is exactly what agents do well. Refactors that used to take a week, like moving forty models to a new naming convention or replacing a deprecated API across a codebase, now take an afternoon plus review.

**Writing tests and fixtures.** Agents are good at generating unit tests, synthetic fixtures that reproduce a source's quirks, and edge cases a tired human skips (nulls, empty files, duplicate keys, time zones). This is where I've seen the best return: more tests means safer changes, which makes every later agent task safer too.

**Investigating failures.** "The nightly job failed; here's the log" is a great agent prompt. An agent can read the stack trace, open the code, check recent commits, query the table that broke and propose a fix in minutes. It's especially useful for the tedious ones: encoding problems, a changed column order in a source file, a type mismatch after a schema change.

**Understanding unfamiliar code and data.** Asking an agent to explain how a legacy pipeline works, trace where a column comes from, or summarize a 3,000-line stored procedure saves hours of reading. With catalog access (through a platform agent or an MCP server), it can also profile tables, find join keys and spot suspicious distributions.

**Infrastructure and CI/CD.** Terraform modules, GitHub Actions workflows, IAM policies and Docker files are boilerplate-heavy, so agents write them quickly. They also need the most careful review, because a mistake here is a security incident rather than a wrong number.

**Documentation and data contracts.** Model descriptions, column documentation, runbooks, ADRs and READMEs that nobody wanted to write now get written, and kept closer to the code.

**Analytics through natural language.** Text-to-SQL interfaces built on a semantic layer let business users ask questions directly. This works well when metrics are defined once (in a semantic layer or governed metric views) and badly when the agent has to guess what "active customer" means from raw tables.

What teams generally *don't* hand to agents yet: unattended changes to production data, decisions about data modeling and architecture without review, anything involving personal data without strict controls, and the final call on whether a number is correct.

## Why data work is different for agents

Most public discussion of coding agents is about application code. Data engineering adds problems an agent can't see by reading the repository:

- **Correctness lives in the data, not the code.** An agent can write a join that compiles, passes the unit tests and silently duplicates rows in production because a key isn't unique in real data. Code review won't catch it; data tests and reconciliation will.
- **State and blast radius.** A wrong deploy of a web service is rolled back. A wrong `MERGE` into a history table writes bad data that has to be repaired, and downstream tables may have already consumed it.
- **Cost.** An agent iterating on a query against a warehouse or a cluster spends real money on every attempt. A loop that runs a full-table scan twenty times can cost more than the engineer's time it saved.
- **Sensitive data.** Data engineers work close to customer data. An agent that can query production tables can also read (and send to a model provider, or leak into a log) personal information.
- **Semantics.** Business definitions, known data quality issues and the reasons behind odd filters usually live in people's heads or scattered documents. Without that context, an agent will produce confident, plausible and wrong logic.

The common thread: agents are excellent at the parts of data engineering that look like software engineering, and need much more guidance and verification for the parts that are about data.

## The trade-offs

### Speed versus understanding

Agents produce code faster than people can understand it. The risk isn't bad code in itself; it's code nobody on the team fully understands, which becomes a problem the first time it breaks at 3 a.m. Teams that do well keep a rule: you own what you merge, and you must be able to explain it.

### Perceived versus measured productivity

The evidence on productivity is more mixed than the marketing. In [METR's 2025 randomized study](https://scienceblog.com/t-a-randomized-trial-by-metr-found-that-experienced-developers-completed-real-coding-tasks-19-slower-when-allowed-to-use-ai-tools-yet-afterwards-they-estimated-on-average-that-ai-had-made-them-20-fast/), experienced open-source developers were 19% slower with AI tools on their own codebases, while believing they had been about 20% faster. METR now describes that result as historical: when it tried to repeat the experiment with newer tools in 2026, many developers refused to work without AI, which made the new measurement unreliable. Both facts are informative. Tools have improved a lot, but people are poor judges of their own speed, so measure outcomes (lead time, incidents, rework), not impressions.

### Amplifier, not fix

Google's [DORA 2025 report on AI-assisted software development](https://research.google/pubs/dora-2025-state-of-ai-assisted-software-development-report/), based on nearly 5,000 professionals, describes AI as an **amplifier**: it magnifies the strengths of teams with good platforms, clear workflows and solid testing, and the dysfunctions of teams without them. That matches what I see in data teams. With a fast test suite, CI, code review and clear conventions, agents multiply output. Without them, agents produce more untested code, faster.

### Cost

Agent usage isn't free: subscriptions or token costs, plus compute costs when agents run queries and jobs. The 2026 Stack Overflow survey found 38% of organizations already set usage limits and 21% report spending more on AI. For data teams, compute is the bigger lever: give agents small development datasets and cheap warehouses, not production-sized ones.

### Dependency

Teams that build their workflow around one vendor's agent, its configuration format and its integrations face lock-in, price changes and outages. Keep the knowledge (conventions, context files, tests, CI) in the repository, in formats any tool can use, and keep the ability to work without the agent.

## Security risks

Agents combine three things that security people have spent decades keeping apart: access to private data, exposure to untrusted content and the ability to act and communicate externally. Simon Willison calls this combination the **lethal trifecta**; Meta's "Agents Rule of Two" suggests an agent acting without human approval should have at most two of the three. The [OWASP GenAI Security Project's 2026 report](https://www.helpnetsecurity.com/2026/06/11/owasp-prompt-injection-ai-security-failures/) notes that agentic risks have moved from theory to documented incidents, with prompt injection involved in six of the ten categories of its Top 10 for agentic applications.

The main risks, with real examples:

**Prompt injection.** Anything an agent reads can contain instructions: a pull request title, an issue, a README in a dependency, a web page, a value in a table. In April 2026, researchers showed that a [malicious pull request title made AI review agents from Anthropic, Google and GitHub leak their own API keys](https://venturebeat.com/security/ai-agent-runtime-security-system-card-audit-comment-and-control-2026) in a GitHub Actions workflow. Data engineers have an extra surface: the data itself. A free-text field in a source system can carry instructions to an agent that later profiles that table.

**Secrets exposure.** Agents run with your environment: cloud credentials, database passwords, tokens in `.env` files. Anything in their context can end up in a log, a commit, a comment or a request to the model provider. Infostealer malware has also started [targeting agent configuration files and tokens](https://botmonster.com/ai/ai-coding-agent-insider-threat-prompt-injection-mcp-exploits/) on developer machines.

**Destructive actions.** The best-known example is the 2025 Replit incident, in which a coding agent deleted a company's production database during a code freeze. For data teams, the equivalent is an agent with write access to production running `DROP`, `TRUNCATE`, `DELETE` without a filter, or `terraform destroy`.

**Tool and supply chain risks.** MCP servers, plugins and agent extensions are code that runs with the agent's permissions. In June 2026, researchers showed ["agentjacking"](https://labs.cloudsecurityalliance.org/research/csa-research-note-agentjacking-mcp-sentry-injection-20260612/): instructions planted in error events that coding agents (Claude Code, Cursor, Codex) read through Sentry's official MCP server and then followed, running commands with the developer's privileges. The same year brought malicious packages and a critical remote code execution flaw in MCP infrastructure. For data teams the lesson is direct: logs, error messages and table contents are inputs an attacker may control. Agents also suggest dependencies, including ones that don't exist (attackers register those names).

**Insecure generated code.** SQL built by string concatenation, overly broad IAM policies (`"Action": "*"`), public buckets and disabled TLS checks are all things agents produce when they optimize for "make it work".

## Privacy of code and data

Using an agent means sending code, and often data, to a model provider. Questions every team should answer before adoption:

- **Is our data used for training?** Business and API terms of the major providers generally exclude customer data from training by default, while consumer plans may not. Check the terms of the exact plan you use, not the vendor's general marketing.
- **How long is it retained, and where?** Retention periods, zero-data-retention options and data residency (EU processing, for example) differ by plan and provider. For GDPR-regulated data, you need a data processing agreement and to know where processing happens.
- **What does the agent actually see?** An agent that runs `SELECT * ... LIMIT 10` on a customer table sends ten customers' personal data to the provider. Give agents access to development data, anonymized or synthetic samples, and metadata (schemas, statistics) rather than raw production rows.
- **Is the tool approved?** "Shadow AI", engineers using personal accounts on company code, is common. The OWASP report cites IBM data showing only 37% of organizations have a policy to detect it. Providing a sanctioned tool with clear rules beats banning tools people will use anyway.
- **Do we need to run models ourselves?** For highly sensitive environments, options include models hosted in your own cloud account (Amazon Bedrock, Azure, Vertex AI) under your existing agreements, the platform's built-in agents that respect catalog permissions, or open-weight models on your own infrastructure, with lower capability as the trade-off.

## What this means for the role

The job is shifting, not disappearing. Writing boilerplate is now cheap; what's expensive is knowing what to build, specifying it clearly, verifying it and running it reliably. In practice, a data engineer's time moves toward:

- **Specification and decomposition:** turning a vague request into well-defined tasks with clear inputs, outputs and acceptance criteria. This is what makes agents useful, and it was always the hard part.
- **Review and verification:** reading diffs critically, checking query plans, and above all validating results against data. Data-level testing becomes more important, not less.
- **Platform and context engineering:** building the environment agents work in, including fast tests, CI, conventions, semantic layers, documentation and permission boundaries. Data teams with a good platform get more from agents.
- **Data modeling and architecture:** agents can write a star schema, but deciding the grain, the history strategy and the boundaries between domains still requires understanding the business.
- **Governance:** access control, lineage, privacy and cost control matter more when non-human actors query and change data.

The uncomfortable part is the entry level. Agents now do many of the tasks juniors used to learn on, and several hiring analyses report weaker entry-level hiring since 2023. The skills that get people hired are changing accordingly: being able to show judgment (projects with tests, clear trade-offs, documented decisions) matters more than showing you can write a `GROUP BY`. Teams that stop training juniors altogether will find out in a few years that seniors don't appear from nowhere.

## What companies now expect

From job descriptions, interviews and conversations with hiring managers, the expectations for data engineers in 2026 look like this:

- **Fluency with agents is assumed.** Several companies made AI use an explicit expectation as early as 2025 (Shopify's CEO wrote that reflexive AI use was a baseline expectation; Coinbase required engineers to onboard AI tools). Not using them is increasingly seen like not using version control.
- **Higher output, same quality bar.** Teams expect more delivered per engineer, but outages and wrong numbers are judged as harshly as ever. "The agent wrote it" isn't an excuse.
- **Judgment over syntax.** Interviews increasingly test design, debugging and reviewing code (often AI-generated) instead of writing algorithms from memory.
- **Security and cost awareness.** Knowing how to give an agent least-privilege access, keep secrets out of its reach and stop it from burning compute is becoming part of the job.
- **Communication.** Writing precise specifications, ADRs and review comments is now a productivity skill, because it's how work gets delegated, to people and to agents.

## Best practices for adopting agents

These are the practices I'd recommend to a data team adopting agents, roughly in order:

1. **Start with the platform, not the tool.** A fast test suite, CI on every pull request, code review and an end-to-end run on synthetic data are what make agent output trustworthy. If you only do one thing, do this.
2. **Write the context down.** Keep a context file in the repository (`CLAUDE.md`, `AGENTS.md` or equivalent) with conventions, architecture, commands to run tests, and what the agent must never do. Point to ADRs and data contracts. Agents follow written conventions far better than unwritten ones.
3. **Least privilege by default.** Agents work with development credentials, development catalogs and small datasets. No production write access, no admin roles, no long-lived cloud keys in the environment. Production changes go through the same CI/CD pipeline as human changes.
4. **Sandbox execution.** Run agents in containers, dev containers or cloud sandboxes with restricted network access where possible. Use the tool's permission modes: allow reading and testing freely, require approval for writes, deletions, network calls and anything touching infrastructure.
5. **Treat all input as untrusted.** Don't give agents in CI access to secrets they don't need, avoid `pull_request_target` with agent workflows on public repositories, use read-only tokens for review agents, and require human approval for any action with side effects.
6. **Vet tools and dependencies.** Install MCP servers and extensions only from trusted sources, pin their versions, review what permissions they get, and check every new dependency an agent adds.
7. **Verify with data, not just code review.** Every agent-written transformation gets data tests (uniqueness, not-null, accepted values, row-count reconciliation) and, for important changes, a comparison of outputs before and after.
8. **Keep humans accountable.** Whoever merges owns the change. Large agent-generated pull requests are split into reviewable pieces; "LGTM" on 2,000 lines isn't a review.
9. **Control cost.** Set spending limits per user or team, give agents small warehouses or clusters with auto-stop, and watch for loops that rerun expensive queries.
10. **Measure.** Track lead time, change failure rate, incidents and rework before and after adoption. Surveys of how fast people feel are not evidence.
11. **Decide on privacy explicitly.** Use business plans with clear data terms, document which data may be sent to which provider, provide approved tools, and train people on what not to paste.

## Where this is going

The direction is clear even if the pace isn't: more autonomous agents running in the background on well-defined tasks (dependency upgrades, test coverage, failure triage), agents embedded in every data platform with access governed by the catalog, and a growing share of each engineer's time spent defining, reviewing and verifying work rather than typing it.

For data engineering, I think the teams that benefit most will be the ones that already did the unglamorous work: tests, CI, documentation, clear models and governance. Agents don't replace that foundation; they reward it. The best preparation for the next generation of agents is the same as the best preparation for a new colleague: a codebase and a platform that make doing the right thing easy, and doing the wrong thing hard.

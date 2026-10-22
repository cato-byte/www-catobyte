## AI Agents in 2026: How They Work and How to Use Them Effectively, With Claude, Codex and Others

##### Published on {{PUBLISH_DATE}}

<!-- TITLE_IMAGE -->

![AI agents in 2026](../../images/ai_agents_how_to_use_them_title_img.png)

*Technical article*

## From chatbots to agents

A chatbot answers and waits. An agent takes a goal, decides what to do, uses tools, looks at the results and keeps going until the goal is reached or it gets stuck. Coding agents such as Claude Code and Codex now edit repositories, run tests and open pull requests on their own, and every cloud provider sells a platform to build agents for customer support, operations and data work.

In an [earlier article](ai_agents_and_data_engineering.html) I looked at what agents mean for data engineering teams: what they delegate, the risks and how the role changes. This one is more practical. It explains how agents work and which design patterns the main labs recommend, then how to use the two tools I work with daily, Claude Code and Codex, effectively. It draws on Anthropic's [Building effective agents](https://www.anthropic.com/research/building-effective-agents), OpenAI's [agents guide](https://developers.openai.com/api/docs/guides/agents), AWS's [agentic AI overview](https://aws.amazon.com/ai/agentic-ai/) and the official documentation of each tool.

## What an agent is

Anthropic draws a useful line between two kinds of "agentic" systems:

- **Workflows** are systems where language models and tools are orchestrated through predefined code paths. Your code decides the steps; the model fills them in.
- **Agents** are systems where the model dynamically directs its own process and tool use, keeping control over how it accomplishes the task.

OpenAI's definition matches the second one: systems that can plan and complete tasks using tools, work with other agents and keep context across steps. Underneath, an agent is surprisingly simple. In Anthropic's words, agents are "typically just LLMs using tools based on environmental feedback in a loop":

```python
def run_agent(goal: str, tools: dict, max_steps: int = 30) -> str:
    messages = [{"role": "user", "content": goal}]
    for _ in range(max_steps):                      # a stopping condition
        reply = call_model(messages, tools=list(tools))
        messages.append(reply)
        if not reply.tool_calls:                    # the model considers the goal reached
            return reply.text
        for call in reply.tool_calls:               # act, then observe the result
            result = tools[call.name](**call.arguments)
            messages.append({"role": "tool", "id": call.id, "content": result})
    return "Stopped: step limit reached"
```

Everything that makes real agents good or bad happens around this loop: which tools exist and how they're described, what the model sees in its context, how it checks its own work, what it is allowed to do without asking, and when it stops.

## Start simple: when you need an agent

Both Anthropic and OpenAI give the same first advice: use the simplest solution that works. A single well-prompted model call with retrieval and a few examples is enough for many applications. Agents trade latency and cost for flexibility, and Anthropic warns that their autonomy brings "higher costs, and the potential for compounding errors": a wrong step early on is built upon by every step after it.

Agents earn their cost on open-ended problems where the number of steps can't be predicted and a fixed path can't be hard-coded, and where results can be checked. That's why coding is the strongest use case today: tests and builds tell the agent whether it succeeded. Customer support is the other one Anthropic highlights, because success is measurable as a resolved request.

## The patterns

Anthropic's article describes a ladder of patterns, from fixed workflows to autonomous agents. They are building blocks to combine, not a framework:

| Pattern | How it works | Use it when | Data engineering example |
|---|---|---|---|
| Augmented LLM | One model call with retrieval, tools and memory | Most tasks; the base of everything else | Answer questions about a table using the catalog |
| Prompt chaining | Fixed sequence of calls, with checks between steps | The task splits cleanly into steps | Draft dbt docs, check them against the SQL, fix |
| Routing | Classify the input, send it to a specialized path | Distinct categories handled differently | Send schema errors and infrastructure errors to different runbooks |
| Parallelization | Independent subtasks at once, or several votes on one | Speed, or more confidence from several views | Review a migration for correctness, performance and security in parallel |
| Orchestrator-workers | A model splits the task and delegates subtasks it decides on | Subtasks can't be known in advance | Change a column name across every model and dashboard that uses it |
| Evaluator-optimizer | One model produces, another critiques, in a loop | Clear criteria and measurable gains from iterating | Tune a slow query until the benchmark passes |
| Autonomous agent | The model plans and acts in a loop with tools | Open-ended tasks in a trusted, testable environment | Investigate and fix a failed nightly job |

Anthropic's three principles for building them are worth keeping in mind with any tool: keep the design **simple**, make the agent's planning **transparent**, and invest in the **agent-computer interface** through documentation and testing of tools.

## Tools are the agent's interface

An agent can only be as good as its tools. Anthropic says that while building its SWE-bench coding agent, the team spent more time optimizing tools than the overall prompt. Its advice is to design tools for the model the way you'd design a function for a junior developer: a clear name, a description with example usage and edge cases, and parameters that make mistakes hard (what it calls *poka-yoke*). In one case, the model made errors with relative file paths after changing directories; requiring absolute paths fixed it completely.

A tool definition written with that care:

```json
{
  "name": "run_sql_readonly",
  "description": "Run a read-only SQL query on the analytics warehouse and return at most 200 rows as CSV. Use it to inspect data, check row counts or validate a transformation. Only SELECT and WITH statements are accepted; anything else is rejected. Always filter large fact tables by date, because unfiltered scans time out after 60 seconds. Table names must be fully qualified, for example analytics.marts.fct_orders.",
  "input_schema": {
    "type": "object",
    "properties": {
      "query": {"type": "string", "description": "A single SELECT or WITH statement with fully qualified table names."},
      "reason": {"type": "string", "description": "One sentence on what you expect to learn from this query."}
    },
    "required": ["query", "reason"]
  }
}
```

The read-only constraint lives in the tool, not only in the description; the row limit protects the context window; the `reason` field makes the agent's intent visible in logs.

## The shared building blocks

A few standards now work across tools, and they're worth learning once:

- **MCP (Model Context Protocol)** connects agents to tools and data (issue trackers, databases, design files, internal APIs) through servers that any compatible agent can use. Anthropic created it and in December 2025 donated it to the Linux Foundation's new [Agentic AI Foundation](https://sdtimes.com/ai/linux-foundation-forms-agentic-ai-foundation-to-be-new-home-for-mcp-goose-and-agents-md/).
- **Context files** hold the instructions an agent reads at the start of every session: `CLAUDE.md` for Claude Code, `AGENTS.md` for Codex and many other agents. AGENTS.md, created by OpenAI, went to the same foundation.
- **Skills** package domain knowledge or a repeatable workflow in a folder with a `SKILL.md` file that the agent loads only when relevant. Claude Code and Codex both support them.
- **Subagents** run part of a task in their own context window and report back a summary, which keeps the main conversation focused.

For building your own agents, each lab offers layers that trade control for convenience. Anthropic has the Messages API (you write the loop), the [Claude Agent SDK](https://code.claude.com/docs/en/agent-sdk/overview) (the loop, tools and context management behind Claude Code, as a Python or TypeScript library) and [Claude Managed Agents](https://platform.claude.com/docs/en/managed-agents/overview) (a hosted harness where Anthropic runs the agent and its sandbox, for long-running work). OpenAI has the Responses API, the Agents SDK (your application runs the loop, with tools and handoffs) and the Agents API (a hosted Codex harness with compaction and multi-agent orchestration). AWS offers [Amazon Bedrock AgentCore](https://aws.amazon.com/ai/agentic-ai/) for running agents built with any framework or model at scale, with memory, governance and security, plus the open-source Strands Agents SDK. Anthropic's caution about frameworks applies to all of them: many patterns take a few lines of code on the raw API, and if you use a framework, understand what it does underneath, because wrong assumptions about it are a common source of bugs.

## Claude: using Claude Code effectively

Claude Code is Anthropic's agentic coding tool, available in the terminal, IDEs, a desktop app and the web. Its [best practices guide](https://code.claude.com/docs/en/best-practices) starts from one constraint that explains most of its advice: the context window fills up fast, and performance degrades as it fills. Every file read and command output takes space, so managing context is the core skill.

**Give it a way to verify its work.** This is the single most important habit. Without a check it can run, "looks done" is the only signal Claude has, and you become the verification loop. With tests, a build, a linter or a screenshot to compare, it can iterate until the check passes. The guide's examples:

```text
Before: implement a function that validates email addresses

After:  write a validateEmail function. example test cases: user@example.com is
        true, invalid is false, user@.com is false. run the tests after implementing
```

```text
Before: the build is failing

After:  the build fails with this error: [paste error]. fix it and verify the build
        succeeds. address the root cause, don't suppress the error
```

For longer runs you can make the check stick: `/goal` keeps Claude working until a condition is met, a Stop hook can block it from finishing until a script passes, and a verification subagent can try to refute the result with fresh eyes. Ask for evidence, the commands and their output, rather than claims of success.

**Explore, plan, then code.** For changes that touch several files or code you don't know, use plan mode (`Shift+Tab`, or `claude --permission-mode plan`): Claude reads and proposes a plan without editing anything. Review and edit the plan, then let it implement and commit. The guide's rule of thumb for skipping this: if you could describe the diff in one sentence, ask for it directly.

**Be specific.** Name files, scenarios and constraints, and point to existing patterns:

```text
users report that login fails after session timeout. check the auth flow in
src/auth/, especially token refresh. write a failing test that reproduces the
issue, then fix it
```

For larger features, the guide suggests having Claude interview you first and write a spec to a file, then implementing it in a fresh session.

**Keep CLAUDE.md short and useful.** Claude reads it at the start of every session. Run `/init` to generate a first version, then keep only what Claude can't infer from the code: commands, style rules that differ from defaults, test instructions, repository etiquette, project-specific gotchas. For each line, ask whether removing it would cause mistakes. A long file makes Claude ignore half of it.

```markdown
# Commands
- Tests: ./kunturvenv/bin/pytest -q (builds the site first)
- Never run scripts/deploy.sh; deployment happens in CI from master

# Conventions
- Content is written in US English first, then translated to es and fr
- Study guides live in content/guides, articles in content/blog
```

**Use the extension points for what they're good at.** Hooks are deterministic, unlike instructions: use them for things that must happen every time, such as running a linter after each edit or blocking writes to a migrations folder. Skills (`.claude/skills/<name>/SKILL.md`) hold knowledge or workflows needed only sometimes. Subagents (`.claude/agents/`) handle investigation in a separate context ("use subagents to investigate how our authentication handles token refresh"). MCP servers and CLI tools such as `gh` or `aws` connect it to external systems; the guide notes CLIs are the most context-efficient way to do so.

**Manage the session.** Press `Esc` to stop and redirect; `Esc Esc` or `/rewind` restores earlier code and conversation from checkpoints. Run `/clear` between unrelated tasks. If you've corrected the same mistake twice, the context is cluttered with failed attempts: clear it and start again with a better prompt.

**Set permissions deliberately.** Recent versions start in auto mode, where a separate classifier reviews actions and blocks risky ones, such as scope escalation or actions driven by hostile content. Allowlists pre-approve commands you trust, and sandboxing restricts filesystem and network access at the operating system level. Manual mode asks before every write or command.

**Scale out when you're ready.** `claude -p` runs non-interactively in scripts and CI, with JSON output. You can fan a migration out over many files, run sessions in parallel in separate git worktrees, or use a writer/reviewer pair where a second session, with fresh context, reviews what the first one wrote:

```bash
for file in $(cat files.txt); do
  claude -p "Migrate $file from Python 2 to Python 3. Return OK or FAIL." \
    --allowedTools "Edit,Bash(git commit *)" \
    --permission-mode dontAsk
done
```

Test the prompt on two or three files first, fix what goes wrong, then run the rest. Before treating unattended work as done, have a subagent review the diff against the plan, reporting only gaps that affect correctness or requirements, so the review doesn't push the code toward over-engineering.

## Codex: using OpenAI's coding agent effectively

Codex is OpenAI's software engineering agent, available in ChatGPT, a desktop app, a CLI, an IDE extension and Codex Cloud, with code review on GitHub. Its [prompting guide](https://learn.chatgpt.com/codex/prompting) recommends the same core habits, in its own vocabulary.

**Name the behavior, the code and the constraints.** A useful Codex prompt says what should change, points to the relevant files or reproduction steps, and states what must not change:

```text
Users get a 500 when exporting reports with more than 10,000 rows. Start by
reproducing the bug locally with the fixture in tests/fixtures/big_report.csv, then
propose a patch and run checks. Do not change the API shape. Keep the fix minimal
and add a regression test if feasible.
```

In the CLI, reference paths with `@`; in the IDE, open files are included automatically and selected lines scope the request. For UI work, attach screenshots and state the framework and component conventions, which a picture doesn't show.

**Plan, then work in milestones.** For multi-step tasks, `/plan` has Codex investigate and propose an approach before editing; you can ask for revisions, such as which files move in each milestone and a rollback strategy. `/goal` sets a persistent goal when available. Large work goes one milestone at a time, each reviewed before the next.

**Ask it to verify and to report.** The guide's examples: re-run the reproduction after the fix, run lint and the smallest relevant test suite and report the commands and results, start the dev server and give the URL to check. After addressing review feedback, run `/review` again.

**Write AGENTS.md.** Codex reads a global file from `~/.codex` and then every `AGENTS.md` from the repository root down to the current directory, with files closer to your working directory overriding earlier ones, up to 32 KiB by default. Put working agreements in it (package manager, which tests to run), repository expectations (lint before pull requests) and code review rules near the code they govern; nested files can override commands for a specific service.

```markdown
# AGENTS.md
- Use uv; never pip install into the system Python.
- After changing pipeline code, run: uv run pytest tests/unit -q
- Run uv run ruff check . before opening a pull request.
- Never edit files under migrations/ by hand; generate them with make migration.

## Code Review Rules
- Flag any query on fct_* tables without a date filter.
```

**Choose the permission mode.** "Ask for approval" works inside the workspace and pauses before editing outside it or using the internet; it's the recommended default. "Approve for me" keeps the same sandbox but sends approval requests to an automatic reviewer that only stops for potentially unsafe actions. "Full access" removes the restrictions. The sandbox defines what Codex can reach; approvals define when it pauses.

**Delegate in parallel.** Codex Cloud runs tasks in isolated environments while you keep working: plan locally, then hand off "Implement Milestone 1 from the plan", review the diff and open a pull request. `codex exec` runs it non-interactively from scripts. As a small first-hand example, the cover images of this article and the previous two were generated by calling `codex exec` from another agent, with a prompt describing each article and a scratch directory to write to, then reviewed before being added to the site.

## Other agents worth knowing

The same habits transfer to the rest of the field. GitHub Copilot has an agent mode in the editor and a coding agent that works from issues to pull requests. Cursor is an AI-first editor with background agents. Google's Gemini CLI is an open-source terminal agent. AWS's Kiro is an IDE built around spec-driven development, where requirements and design documents come before code. And the data platforms ship their own agents inside the product, such as Snowflake's Cortex Code and Databricks' agentic features in Lakeflow, which work with the platform's catalog and permissions. Most of them read `AGENTS.md` or their own context file, support MCP, and offer some mix of plan mode, permission levels and background execution.

## Practices that work with any agent

Across Anthropic's, OpenAI's and AWS's material and my own use, these are the habits that make the difference:

1. **Give the agent a check it can run.** Tests, builds, linters, data validations, screenshots. No check, no unattended work.
2. **Write the context down, briefly.** A short context file with commands and non-obvious rules, plus skills for occasional knowledge. Prune it when the agent ignores it.
3. **Plan before large changes.** Separate exploration from editing, and review the plan; it's cheaper to fix than the diff.
4. **Be specific about scope and constraints.** Files, scenarios, what must not change, what "done" means.
5. **Keep the context clean.** One task per session, subagents for investigation, a fresh start after repeated corrections.
6. **Least privilege.** Sandboxes, development credentials, approvals for anything with side effects; never production write access for an agent.
7. **Treat external content as untrusted.** Issues, web pages and files can carry prompt injection; the agent's permissions, not its prompt, are the real limit.
8. **Review with fresh eyes.** A second session or subagent, or a human, reviews the diff against the requirements before it merges.
9. **Parallelize independent work.** Worktrees, cloud tasks and fan-out scripts, each with its own check.
10. **Measure the outcome.** Lead time, defects and rework, not how fast it feels. AWS reports internal teams that redesigned their workflows around agents delivering a project scoped for 30 developers in 76 days with six engineers; results like that come from changing the workflow, not just adding a tool.

The direction is clear: agents are moving from assistants you watch to colleagues you delegate to. What makes delegation safe is the same as with people: a clear task, the right context, limited permissions, a way to check the result and a review before it counts.

## Sources

- Anthropic: [Building effective agents](https://www.anthropic.com/research/building-effective-agents), [Claude Code best practices](https://code.claude.com/docs/en/best-practices), [Claude Agent SDK](https://code.claude.com/docs/en/agent-sdk/overview), [Claude Managed Agents](https://platform.claude.com/docs/en/managed-agents/overview)
- OpenAI: [Agents guide](https://developers.openai.com/api/docs/guides/agents), [Codex prompting](https://learn.chatgpt.com/codex/prompting), [Codex AGENTS.md](https://learn.chatgpt.com/codex/agent-configuration/agents-md), [Codex permissions](https://learn.chatgpt.com/codex/permission-modes)
- AWS: [Agentic AI on AWS](https://aws.amazon.com/ai/agentic-ai/)
- Linux Foundation: [Agentic AI Foundation, new home for MCP and AGENTS.md (SD Times)](https://sdtimes.com/ai/linux-foundation-forms-agentic-ai-foundation-to-be-new-home-for-mcp-goose-and-agents-md/)

# Agents Analysis

Open source examples and prompts for calculating the effective token price of AI agent subscriptions from local usage logs.

The goal is simple: compare what a user pays for a subscription with the API-equivalent value of the usage they actually consumed.

This repository currently focuses on:

- Codex usage from `.codex` logs.
- Claude Code usage from `.claude` logs.
- Effective price per 1M tokens.
- Weekly quota extrapolation from the usage percentage shown in the product UI.

API-equivalent value is not the provider's real cost. It is the price a user would roughly pay if the same token mix were reproduced through official public API pricing.

## Repository Structure

```text
result/
  <github-username>/
    codex/
      data.json
      analysis.md
    claude/
      data.json
      analysis.md
CONTRIBUTE.md
README.md
```

Each contributor should add results under their own GitHub username:

```text
result/alice/codex/data.json
result/alice/codex/analysis.md
result/alice/claude/data.json
result/alice/claude/analysis.md
```

## Example Included

The first example is under:

- `result/melvynx/codex/`
- `result/melvynx/claude/`

It includes:

- subscription actually used
- weekly reset window
- measured usage percentage
- token totals
- API-equivalent spend
- effective per-1M token prices
- approximate error metrics

## Contribution Flow

1. Read `CONTRIBUTE.md`.
2. Choose the tool you want to analyze: `codex`, `claude`, or both.
3. Give the agent your weekly limit end date. This matters because the start date is usually `end date - 7 days`.
4. Let the agent verify current API prices from official docs.
5. Let the agent parse your local `.codex` and/or `.claude` logs.
6. Add your results under `result/<github-username>/<tool>/`.
7. Open a pull request.

Do not commit private conversation content. The result files should contain aggregate usage data only.

## Privacy Notes

Local agent logs can contain prompts, file paths, project names, tool outputs, and secrets accidentally pasted into conversations.

Before opening a pull request:

- Only publish aggregate numbers.
- Do not publish raw `.jsonl` logs.
- Redact private machine paths if needed.
- Redact repository names if they are private.
- Do not include prompts or assistant messages unless you intentionally want them public.

## License

MIT

# Agents Analysis

Open source examples and prompts for calculating the effective token price of AI agent subscriptions from local usage logs.

The goal is simple: compare what a user pays for a subscription with the API-equivalent value of the usage they actually consumed.

This repository currently focuses on:

- Codex usage from `.codex` logs.
- Claude Code usage from `.claude` logs.
- Effective price per 1M tokens.
- Weekly quota extrapolation from the usage percentage shown in the product UI.
- Small helper scripts to recompute results faster.
- Markdown pricing references for the model baselines used in examples.

API-equivalent value is not the provider's real cost. It is the price a user would roughly pay if the same token mix were reproduced through official public API pricing.

## Repository Structure

```text
result/
  <github-username>/
    codex/
      <analysis-timestamp>/
        data.json
        analysis.md
    claude/
      <analysis-timestamp>/
        data.json
        analysis.md
CONTRIBUTE.md
README.md
```

Each contributor should add results under their own GitHub username:

```text
result/alice/codex/2026-05-30T21-14-45Z/data.json
result/alice/codex/2026-05-30T21-14-45Z/analysis.md
result/alice/claude/2026-05-30T21-14-45Z/data.json
result/alice/claude/2026-05-30T21-14-45Z/analysis.md
```

Each analysis run is stored in its own timestamped folder under the selected tool. This allows multiple analyses during the same weekly quota window without overwriting earlier results. Use the measurement end time in UTC for the folder name, formatted like `YYYY-MM-DDTHH-MM-SSZ`.

## Example Included

The first example is under timestamped folders inside:

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
- monthly API-equivalent extrapolation

## Contribution Flow

1. Read `CONTRIBUTE.md`.
2. Choose the tool you want to analyze: `codex`, `claude`, or both.
3. Provide all required preflight data: GitHub username, subscription name, monthly price, weekly usage percentage, weekly reset date, and reset timezone.
4. Do not start cloning, parsing, or calculating until every required value is known.
5. Let the agent verify current API prices from official docs.
6. Let the agent parse your local `.codex` and/or `.claude` logs.
7. Add your results under `result/<github-username>/<tool>/<analysis-timestamp>/`.
8. Open a pull request.

Do not commit private conversation content. The result files should contain aggregate usage data only.

## Helper Scripts

The scripts are intentionally plain Python with no external dependencies.

Codex:

```bash
scripts/analyze_codex.py \
  --username <github-username> \
  --subscription "OpenAI Pro $200/month" \
  --monthly-price 200 \
  --used-percent 43 \
  --start "2026-05-23T21:14:45Z" \
  --limit-end "2026-05-30T23:14:45+02:00" \
  --output-dir result/<github-username>/codex
```

Claude:

```bash
scripts/analyze_claude.py \
  --username <github-username> \
  --subscription "Claude Max $100/month" \
  --monthly-price 100 \
  --used-percent 8 \
  --start "2026-05-24T09:00:00Z" \
  --limit-end "2026-05-31T11:00:00+02:00" \
  --output-dir result/<github-username>/claude
```

When `--output-dir` points to `result/<github-username>/<tool>`, the scripts create a timestamped child folder automatically. Pass `--analysis-id YYYY-MM-DDTHH-MM-SSZ` only when you need to reproduce a specific folder name.

The weekly usage percentage and weekly limit end date are not optional in the contribution workflow. They are what make the report calculable and reproducible.

## Pricing References

Pricing snapshots used by the examples live in:

- `docs/pricing/openai.md`
- `docs/pricing/anthropic.md`

Always re-check official pricing before publishing a new result.

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

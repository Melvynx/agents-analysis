# Contributing Results

This repository collects effective token price reports for AI agent subscriptions.

The useful comparison is not "how much did the provider spend?" The useful comparison is:

> If I had reproduced the same usage through the official API, how much would it have cost?

## Result Path

Create one folder per GitHub username and tool:

```text
result/<github-username>/codex/
result/<github-username>/claude/
```

Each tool folder should contain:

```text
data.json
analysis.md
```

Example:

```text
result/melvynx/codex/data.json
result/melvynx/codex/analysis.md
result/melvynx/claude/data.json
result/melvynx/claude/analysis.md
```

## Required Inputs

Before running the analysis, collect these values from the product UI:

- Which subscription you actually use, for example `OpenAI Pro $200/month` or `Claude Max $100/month`.
- Weekly usage percentage, for example `43% used`.
- Weekly limit end date, for example `Resets May 30, 2026 11:14 PM`.
- Timezone of that reset date.
- Whether you want to calculate `codex`, `claude`, or both.

The weekly limit end date is critical. Without it, the agent cannot know the exact 7-day window. In most cases:

```text
weekly_window_start = weekly_limit_end_date - 7 days
weekly_window_end = now, or the explicit measurement end date
```

## Pull Request Rules

- Do not commit raw `.codex` or `.claude` logs.
- Do not commit private prompts or assistant messages.
- Commit aggregate data only.
- Add your result under `result/<github-username>/<tool>/`.
- If you include local paths, make sure they are safe to publish.
- If API prices were not verified live, mark them as assumptions.

## Prompt To Run

Use this prompt with an agent that can read your local filesystem and browse current official API pricing.

```text
You are a usage and cost analyst. Calculate the effective token price per 1M tokens of my Codex and/or Claude subscription from my local `.codex` and `.claude` folders, then create contribution files for an open source repository.

I want to calculate: <codex | claude | both>
My GitHub username is: <github-username>
My Codex subscription is: <for example OpenAI Pro $200/month>
My Codex weekly limit ends at: <exact reset/end date with timezone>
My Codex weekly usage percentage is: <for example 43%>
My Claude subscription is: <for example Claude Max $100/month>
My Claude weekly limit ends at: <exact reset/end date with timezone>
My Claude weekly All models usage percentage is: <for example 8%>
My Claude Sonnet-only usage percentage is: <optional>

Important:
- Verify the latest official API prices before calculating.
- For OpenAI, verify GPT-5.5 input, cached input, and output prices.
- For Anthropic, verify Claude Opus input, cache write 5m, cache write 1h, cache read, and output prices.
- If prices cannot be verified, clearly mark the pricing as an assumption.
- The weekly limit end date is required. Use it to calculate the start of the 7-day window.
- Do not publish raw conversation logs.
- Do not publish private prompts, assistant messages, secrets, or raw tool outputs.

Create:
- `result/<github-username>/codex/data.json` if Codex is selected.
- `result/<github-username>/codex/analysis.md` if Codex is selected.
- `result/<github-username>/claude/data.json` if Claude is selected.
- `result/<github-username>/claude/analysis.md` if Claude is selected.

The `data.json` file must include:
- contributor GitHub username
- tool name
- subscription actually used
- monthly subscription price
- weekly subscription price
- weekly limit end date
- measurement start date
- measurement end date
- usage percentage used for extrapolation
- official API pricing used
- token totals
- conversations or sessions counted
- raw request counts if available
- deduped request counts if available
- skipped duplicates if available
- measured API-equivalent spend
- extrapolated weekly API-equivalent value at 100% quota
- effective API ratio
- effective token prices per 1M
- approximate error metrics
- parsing notes and assumptions

The `analysis.md` file must include:
- short human-readable summary
- calculation window
- subscription used
- measured API-equivalent spend
- extrapolated 100% weekly value
- effective price per 1M tokens
- important caveats
- privacy note

Parsing Codex:
- Include `~/.codex/sessions/**/*.jsonl`.
- Include `~/.codex/archived_sessions/*.jsonl`.
- Include any other Codex archive folders found locally.
- Keep only events inside the weekly measurement window.
- Count one conversation by `session_meta.payload.id`, otherwise by filename.
- For tokens, use `event_msg` events where `payload.type == "token_count"`.
- Sum `payload.info.last_token_usage`, not `total_token_usage`.
- Sum input, cached input, output, reasoning output, and total tokens.
- Calculate uncached input as `max(0, input_tokens - cached_input_tokens)`.
- Estimate tool error rate from `function_call_output` events with non-zero exit code.
- Estimate model/API error rate from explicit assistant messages containing API errors, rate limits, or overloads.

Parsing Claude:
- Include `~/.claude/projects/**/*.jsonl`.
- Include project subdirectories and subagent files.
- Keep only `type == "assistant"` lines with `message.usage`.
- Deduplicate by `requestId` when present.
- If `requestId` is missing, deduplicate by `(sessionId, message.id, timestamp, usage)`.
- Count skipped duplicates.
- Count one conversation by `sessionId`.
- Sum input tokens, cache creation tokens, cache read tokens, output tokens, 5m cache write tokens, and 1h cache write tokens.
- Map models containing `opus` to Opus pricing, `sonnet` to Sonnet pricing, and `haiku` to Haiku pricing.
- Treat `<synthetic>` as cost 0 and count it in error/system metrics when relevant.

Effective price formula:

weekly_subscription_cost = monthly_subscription_cost / (52 / 12)
weekly_api_value_at_100pct = measured_api_cost / (used_percent / 100)
effective_api_ratio = weekly_subscription_cost / weekly_api_value_at_100pct
effective_price_per_1m = official_api_price_per_1m * effective_api_ratio

Open a pull request with only the new result files.
```

## Review Checklist

Before opening a PR, check:

- The result path uses your GitHub username.
- The weekly limit end date is present.
- The measurement start and end dates are present.
- The subscription actually used is present.
- The API price source or assumption is present.
- No raw logs are included.
- No private prompts are included.

## Optional Helper Scripts

You can use the scripts in this repository instead of writing your own parser.

Codex:

```bash
scripts/analyze_codex.py \
  --username <github-username> \
  --subscription "OpenAI Pro $200/month" \
  --monthly-price 200 \
  --used-percent <weekly-used-percent> \
  --start "<weekly-window-start-iso>" \
  --limit-end "<weekly-limit-end-iso>" \
  --output-dir result/<github-username>/codex
```

Claude:

```bash
scripts/analyze_claude.py \
  --username <github-username> \
  --subscription "Claude Max $100/month" \
  --monthly-price 100 \
  --used-percent <weekly-used-percent> \
  --start "<weekly-window-start-iso>" \
  --limit-end "<weekly-limit-end-iso>" \
  --output-dir result/<github-username>/claude
```

The scripts output JSON to stdout and write `data.json` plus `analysis.md` when `--output-dir` is provided.

For Codex, `--extra-cost label=value` can be used to include additional API-equivalent costs from a remote machine or another agent log store.

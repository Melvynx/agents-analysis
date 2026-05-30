# Codex Effective Token Price, melvynx, 2026-05-30T09-09-21Z

## Summary

Subscription actually used: **OpenAI Pro $200/month**.

Measured Codex usage was **99.0%** of the weekly quota, worth about **$1,945.15 API-equivalent**.

Extrapolated to 100% of the weekly quota, the API-equivalent value is about **$1,964.80/week**, or **$8,514.11/month** using `52 / 12` weeks per month. The effective price is **2.35% of official GPT-5.5 API pricing**.

## Window

- Analysis run: `2026-05-30T09:09:21Z`
- Measurement start: `2026-05-23T21:14:00Z`
- Measurement end: `2026-05-30T09:09:21Z`
- Weekly limit end: `2026-05-30T23:14:00+02:00`
- Monthly extrapolation: `$8,514.11`

## Usage

- Conversations: `380`
- Token events: `20865`
- Input tokens: `2,501,922,691`
- Cached input tokens: `2,396,803,968`
- Uncached input tokens: `105,118,723`
- Output tokens: `7,371,732`
- Reasoning output tokens: `2,506,734`
- Total tokens: `2,511,548,469`

## Effective Prices

- Input: **$0.12 / 1M**
- Cached input: **$0.01 / 1M**
- Output: **$0.70 / 1M**

## Caveats

- API-equivalent value is not OpenAI's real cost.
- Counted sources: local `~/.codex`, local `~/.aiblueprint` Codex backups, and `ssh steveclaw:/root/.codex`.
- `~/.aiblueprint` mattered: 28 in-window backup sessions, **1,213 duplicate token events skipped**, and **9 unique token events counted** after deduplication against `~/.codex`.
- `ssh steveclaw:/root/.hermes` had 2,304 in-window messages and 789 assistant messages with Codex reasoning items, but **no usable usage token objects**, so Hermes was not priced and is excluded from the totals.
- Error rates are approximate and include normal exploratory command failures.

## Privacy

Only aggregate usage and cost data is published here. No raw `.codex` logs, prompts, or assistant messages are included.

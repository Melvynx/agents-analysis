# Claude Effective Token Price, melvynx

## Summary

Subscription actually used: **Claude Max $100/month**.

Measured Claude usage was **28.0%** of the weekly All models quota, worth about **$238.99 API-equivalent**.

Extrapolated to 100% of the weekly quota, the API-equivalent value is about **$853.53/week**, or **$3,698.64/month** using `52 / 12` weeks per month. The effective price is **2.70% of official Opus API pricing**.

## Window

- Measurement start: `2026-05-24T09:00:00Z`
- Measurement end: `2026-05-28T09:35:22Z`
- Weekly limit end: `2026-05-31T11:00:00+02:00`
- Monthly extrapolation: `$3,698.64`

## Usage

- Conversations: `59`
- Raw assistant usage events: `4098`
- Deduped assistant requests: `2081`
- Duplicates skipped: `2017`
- Input tokens: `53,228`
- Cache creation tokens: `10,603,811`
- Cache read tokens: `228,234,725`
- Output tokens: `1,215,449`

## Effective Opus Prices

- Input: **$0.14 / 1M**
- Cache write 5m: **$0.17 / 1M**
- Cache write 1h: **$0.27 / 1M**
- Cache read: **$0.01 / 1M**
- Output: **$0.68 / 1M**

## Sources

- `/Users/melvynx/.config/backups/claude-code/2026-05-27_06-51-38/projects`: primary restored source, 9,655 files scanned, 56 conversations, 2,068 deduped requests.
- `/Users/melvynx/.claude/projects`: current post-backup source, 3 files scanned, 3 conversations, 13 deduped requests.
- `ssh steveclaw:/root/.claude/projects`: checked, 85 files scanned, no assistant usage rows in the selected Claude window.

## Caveats

- API-equivalent value is not Anthropic's real cost.
- Claude weekly usage percentage must usually come from the UI.
- Current `~/.claude/projects` alone is incomplete for this window; the restored backup is the source of the main Claude session data.
- Error rates are approximate and synthetic messages are counted separately.

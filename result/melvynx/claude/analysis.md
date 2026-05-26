# Claude Effective Token Price, melvynx

## Summary

Subscription actually used: **Claude Max $100/month**.

The measured Claude usage was **8% of the weekly All models quota**, worth about **$103.15 API-equivalent** using Claude Opus pricing as the main baseline.

Extrapolated to 100% of the weekly quota, the API-equivalent value is about **$1,289.33/week**. Since the subscription costs about **$23.08/week**, the effective price is **1.79% of official Opus API pricing**.

## Window

- Weekly limit start: `2026-05-24T11:00:00+02:00`
- Weekly limit end: `2026-05-31T11:00:00+02:00`
- Measurement start: `2026-05-24T09:00:00Z`
- Measurement end: `2026-05-26T11:03:28Z`
- Timezone: `Europe/Zurich`

## Request Data

Local `.claude/projects` usage:

- Conversations: `25`
- Raw assistant usage events: `1,780`
- Deduped assistant requests: `875`
- Duplicates skipped: `905`
- Opus requests: `800`
- Sonnet requests: `68`
- Synthetic requests: `7`

Token totals:

- Input tokens: `4,648`
- Cache creation tokens: `4,909,889`
- Cache write 1h tokens: `4,490,641`
- Cache write 5m tokens: `419,248`
- Cache read tokens: `90,792,690`
- Output tokens: `467,597`

## Cost Breakdown

Claude Opus 4.7 official API baseline:

- Input: `$5.00 / 1M`
- Cache write 5m: `$6.25 / 1M`
- Cache write 1h: `$10.00 / 1M`
- Cache read: `$0.50 / 1M`
- Output: `$25.00 / 1M`

Measured API-equivalent value:

- Opus: `$100.91`
- Sonnet: `$2.23`
- Synthetic: `$0.00`
- Total: `$103.15`

## Effective Price

```text
weekly_subscription_cost = $100 / (52 / 12) = $23.08
weekly_api_value_at_100pct = $103.15 / 0.08 = $1,289.33
effective_api_ratio = $23.08 / $1,289.33 = 1.79%
```

Effective Opus non-Fast price:

- Input: **$0.09 / 1M**
- Cache write 5m: **$0.11 / 1M**
- Cache write 1h: **$0.18 / 1M**
- Cache read: **$0.009 / 1M**
- Output: **$0.45 / 1M**

Effective Opus Fast price, assuming 6x:

- Input: **$0.54 / 1M**
- Cache write 5m: **$0.67 / 1M**
- Cache write 1h: **$1.07 / 1M**
- Cache read: **$0.054 / 1M**
- Output: **$2.68 / 1M**

## Error Metrics

- Synthetic request rate: `~0.8%`
- Approximate API error rate: `~0.7%`

Most detected synthetic API errors were temporary overload messages.

## Caveats

- API-equivalent value is not Anthropic's real cost.
- The result depends on the user's actual model mix and cache behavior.
- Assistant usage rows were deduplicated by `requestId`.
- Logs from other machines are not included.
- Raw logs were not published.

# Codex Effective Token Price, melvynx

## Summary

Subscription actually used: **OpenAI Pro $200/month**.

The measured Codex usage was **43% of the weekly quota**, worth about **$1,133.23 API-equivalent** using GPT-5.5 pricing as the baseline.

Extrapolated to 100% of the weekly quota, the API-equivalent value is about **$2,635.42/week**. Since the subscription costs about **$46.15/week**, the effective price is **1.75% of official API pricing**.

## Window

- Weekly limit start: `2026-05-23T23:14:45+02:00`
- Weekly limit end: `2026-05-30T23:14:45+02:00`
- Measurement start: `2026-05-23T21:14:45Z`
- Measurement end: `2026-05-26T10:54:51Z`
- Timezone: `Europe/Zurich`

## Token Data

Local `.codex` usage:

- Conversations: `116`
- Events/token events: `11,315`
- Input tokens: `1,426,702,842`
- Cached input tokens: `1,374,140,672`
- Uncached input tokens: `52,562,170`
- Output tokens: `4,084,868`
- Reasoning output tokens: `1,377,122`
- Total tokens: `1,432,052,143`

Additional included usage:

- steveclaw Hermes adjusted cost: `$60.27`
- steveclaw `.codex` cost: `$0.53`

## Cost Breakdown

GPT-5.5 official API baseline:

- Input: `$5.00 / 1M`
- Cached input: `$0.50 / 1M`
- Output: `$30.00 / 1M`

Measured API-equivalent value:

- Local uncached input: `$262.81`
- Local cached input: `$687.07`
- Local output: `$122.55`
- Local `.codex` total: `$1,072.43`
- Total with Hermes and remote `.codex`: `$1,133.23`

## Effective Price

```text
weekly_subscription_cost = $200 / (52 / 12) = $46.15
weekly_api_value_at_100pct = $1,133.23 / 0.43 = $2,635.42
effective_api_ratio = $46.15 / $2,635.42 = 1.75%
```

Effective non-Fast price:

- Input: **$0.09 / 1M**
- Cached input: **$0.009 / 1M**
- Output: **$0.53 / 1M**

Effective Fast price, assuming 2.5x quota consumption:

- Input: **$0.22 / 1M**
- Cached input: **$0.022 / 1M**
- Output: **$1.31 / 1M**

## Error Metrics

- Approximate tool/command error rate: `~5.3%`
- Approximate model/API error rate: `~0.0%`

The tool error rate is based on command outputs with non-zero exit codes. This can include normal exploratory failures, not only provider errors.

## Caveats

- API-equivalent value is not OpenAI's real cost.
- The result depends on the user's actual token mix and cache behavior.
- Logs from machines not scanned are not included.
- Remote Hermes usage was included because the user indicated it also consumed the same limits.
- Raw logs were not published.

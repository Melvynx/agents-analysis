# Claude Max 20x ($200) Report

This report estimates the **monthly API-equivalent value** and **monthly token volume** you can expect on the Claude Max 20x ($200/month) plan, extrapolated from the real usage logs in this repo.

## Scope

Source data: all `result/*/claude/*/data.json` files.

- Direct Max 20x sample: **taka-foo** (`result/taka-foo/claude`)
- Supporting samples (for triangulation): 3× Max 5x ($100), 1× Pro ($20)
- API baseline: Anthropic **Claude Opus 4.7** public pricing
- All "value" figures are API-equivalent, not Anthropic's real cost.

## Headline (Claude Max 20x · $200/mo)

| Metric | Value |
| --- | --- |
| Monthly API-equivalent value (direct) | **~$18,883** |
| Monthly API-equivalent value (triangulated range) | **~$19,000 - $22,000** |
| Monthly tokens at 100% weekly quota | **~23.3B** |
| Value multiplier vs $200 | **~94x** (up to ~109x triangulated) |
| Effective token price | **~1.06%** of official Opus 4.7 API pricing |

## Direct sample (taka-foo)

The only Max 20x sample in the repo. Measured over ~1 day at **10%** of the weekly quota, then extrapolated.

| Field | Value |
| --- | --- |
| Subscription | Claude Max 20x $200/month |
| Weekly quota used | 10.0% |
| Measured window | 2026-05-29 to 2026-05-30 (~1 day) |
| Measured value | $435.76 |
| Weekly value at 100% quota | $4,357.59 |
| Monthly value at 100% quota | $18,882.87 |
| Effective rate | 1.06% of API |

Extrapolation factor (measured -> monthly at 100%): `(1 / 0.10) x (52 / 12) = 43.33`.

## Monthly token volume (extrapolated to 100% quota)

| Token type | Monthly tokens | Share |
| --- | --- | --- |
| Cache read | ~22.6B | 97.0% |
| Cache write (creation) | ~666M | 2.9% |
| Output | ~36.4M | 0.16% |
| Input (uncached) | ~104K | 0.0% |
| **Total** | **~23.3B** | 100% |

Cache write splits into ~665M at the 1-hour TTL and ~1.0M at the 5-minute TTL.

## Where the value comes from

Priced at Opus 4.7 rates, the monthly value is dominated by cache traffic:

| Token type | Monthly value | Share |
| --- | --- | --- |
| Cache read | ~$11,319 | 59.9% |
| Cache write (1h) | ~$6,654 | 35.2% |
| Output | ~$911 | 4.8% |
| Input + 5m cache writes | ~$7 | 0.1% |

Cache reads are 97% of the tokens but only ~60% of the value; the 1-hour cache writes are a small share of tokens yet 35% of value because they list at $10/1M.

## Effective token prices (with sub vs without)

Opus 4.7 rates, per 1M tokens. The subscription bills everything against the flat $200, so the effective rate is ~1.06% of list across the board.

| Token type | Without sub (API) | With sub (effective) | Save |
| --- | --- | --- | --- |
| Input | $5.00 | $0.053 | 98.9% |
| Cache write 5m | $6.25 | $0.066 | 98.9% |
| Cache write 1h | $10.00 | $0.106 | 98.9% |
| Cache read | $0.50 | $0.0053 | 98.9% |
| Output | $25.00 | $0.265 | 98.9% |

## Triangulation (three independent estimates)

Claude Max 20x grants 20x the Pro quota and 4x the Max 5x quota, so the same per-token behavior scales linearly.

| Method | Basis | Monthly value for Max 20x |
| --- | --- | --- |
| Direct | taka-foo Max 20x at 100% | **$18,883** |
| Via Max 5x | avg of 3 Max 5x samples ($5,273) x 4 | **$21,094** |
| Via Pro | Pro $20 sample ($1,088) x 20 | **$21,768** |

All three land in a **~$19k - $22k/month** band, supporting the direct estimate.

### Plan ladder (monthly value at 100% quota)

| Plan | Price | Monthly API value | Multiplier |
| --- | --- | --- | --- |
| Pro | $20 | ~$1,088 | ~54x |
| Max 5x | $100 | ~$5,273 (avg) | ~53x |
| Max 20x | $200 | ~$18,883 - $22,000 | ~94-109x |

## Caveats

- The direct Max 20x figure extrapolates from a single ~1-day window at 10% quota, so the multiplier (x10 to weekly) carries real uncertainty. The triangulation is what gives confidence in the ~$19-22k band.
- Usage is heavily Opus-weighted; a Sonnet/Haiku-heavy month would value lower at API rates but is also lighter on the quota.
- Weekly percentages come from the Claude UI; local logs do not store them.
- API-equivalent value is a value estimate at Anthropic list pricing, not what Anthropic actually pays or charges.

Source: `result/taka-foo/claude/data.json` (direct), plus Max 5x and Pro samples for triangulation.

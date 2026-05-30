# Claude Effective Token Price, jlalbany, 2026-05-27T15-18-27Z

## Summary

Subscription actually used: **Claude Max 5x USD 100/month**.

Measured Claude usage was **15.0%** of the weekly All models quota, worth about **$241.53 API-equivalent**.

Extrapolated to 100% of the weekly quota, the API-equivalent value is about **$1,610.22/week**, or **$6,977.64/month** using `52 / 12` weeks per month. The effective price is **1.43% of official Opus API pricing**.

## Window

- Analysis run: `2026-05-27T15:18:27Z`
- Measurement start: `2026-05-26T17:00:00Z`
- Measurement end: `2026-05-27T15:18:27Z`
- Weekly limit end: `2026-06-02T19:00:00+02:00`
- Monthly extrapolation: `$6,977.64`

## Usage

- Conversations: `4`
- Raw assistant usage events: `1782`
- Deduped assistant requests: `939`
- Duplicates skipped: `843`
- Input tokens: `47,980`
- Cache creation tokens: `6,369,787`
- Cache read tokens: `328,643,668`
- Output tokens: `915,456`

## Effective Opus Prices

- Input: **$0.07 / 1M**
- Cache write 5m: **$0.09 / 1M**
- Cache write 1h: **$0.14 / 1M**
- Cache read: **$0.01 / 1M**
- Output: **$0.36 / 1M**

## Caveats

- API-equivalent value is not Anthropic's real cost.
- Anthropic API pricing was checked on 2026-05-27 from `https://platform.claude.com/docs/en/about-claude/pricing`.
- Claude Max 5x subscription pricing was checked from the Anthropic help center; the UI screenshot identifies the active plan as `Max (5x)`.
- The Claude UI screenshot showed `15%` weekly All models usage and `3%` Sonnet-only usage; only All models usage is used for quota extrapolation.
- Claude weekly usage percentage must usually come from the UI.
- Error rates are approximate and synthetic messages are counted separately.

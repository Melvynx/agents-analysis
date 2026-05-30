# Claude Effective Token Price, taka-foo

## Summary

Subscription actually used: **Claude Max 20x $200/month**.

Measured Claude usage was **10.0%** of the weekly All models quota, worth about **$435.76 API-equivalent**.

Extrapolated to 100% of the weekly quota, the API-equivalent value is about **$4,357.59/week**, or **$18,882.87/month** using `52 / 12` weeks per month. The effective price is **1.06% of official Opus API pricing**.

## Window

- Measurement start: `2026-05-29T09:00:00Z`
- Measurement end: `2026-05-30T09:48:37.043066Z`
- Weekly limit end: `2026-06-05T11:00:00+02:00`
- Monthly extrapolation: `$18,882.87`

## Usage

- Conversations: `2`
- Raw assistant usage events: `2121`
- Deduped assistant requests: `1086`
- Duplicates skipped: `1035`
- Input tokens: `2,408`
- Cache creation tokens: `15,379,200`
- Cache read tokens: `522,404,329`
- Output tokens: `840,770`

## Effective Opus Prices

- Input: **$0.05 / 1M**
- Cache write 5m: **$0.07 / 1M**
- Cache write 1h: **$0.11 / 1M**
- Cache read: **$0.01 / 1M**
- Output: **$0.26 / 1M**

## Caveats

- API-equivalent value is not Anthropic's real cost.
- Claude weekly usage percentage must usually come from the UI.
- Error rates are approximate and synthetic messages are counted separately.

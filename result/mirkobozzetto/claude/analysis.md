# Claude Effective Token Price, mirkobozzetto

## Summary

Subscription actually used: **Claude Max 20x $200/month**.

The weekly UI usage percentage was **not captured** for this contribution, so no extrapolation is applied. The numbers below are the **directly measured 7-day API-equivalent spend**, used as a conservative floor (`used_percent = 100` = "measured window = full week").

Directly measured Claude API-equivalent value over the 7-day window: **$769.02/week**, or **$3,332.41/month** using `52 / 12` weeks per month, against a **$46.15/week** subscription cost. The effective price is **6.00% of official Opus API pricing** (about **16.7x value** for what is paid).

If actual weekly quota usage was below 100%, the true value at full quota is higher and the effective price lower — so 6.00% is an **upper bound on cost**, not a best case.

## Window

- Measurement start: `2026-05-22T12:27:08Z`
- Measurement end: `2026-05-29T12:27:08Z`
- Weekly limit end: `2026-05-29T12:27:08Z`
- Monthly extrapolation: `$3,332.41`

## Usage

- Conversations: `282`
- Raw assistant usage events: `29737`
- Deduped assistant requests: `5013`
- Duplicates skipped: `24724`
- Input tokens: `886,214`
- Cache creation tokens: `52,467,875`
- Cache read tokens: `690,373,045`
- Output tokens: `2,994,020`

## Effective Opus Prices

- Input: **$0.30 / 1M**
- Cache write 5m: **$0.38 / 1M**
- Cache write 1h: **$0.60 / 1M**
- Cache read: **$0.03 / 1M**
- Output: **$1.50 / 1M**

## Caveats

- API-equivalent value is not Anthropic's real cost.
- Claude weekly usage percentage must usually come from the UI; it was not captured here, so `used_percent = 100` is a conservative floor (no extrapolation), making the 6.00% effective ratio an upper bound on cost.
- The measurement window is the 7 days preceding the run, not a real weekly reset boundary.
- Models in the window: Opus 4.8 / 4.7 / 4.6 and Haiku 4.5. Opus pricing is used as the effective-price baseline.
- Error rates are approximate and synthetic messages are counted separately.

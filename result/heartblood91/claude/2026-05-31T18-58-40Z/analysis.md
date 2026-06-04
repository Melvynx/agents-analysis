# Claude effective value, heartblood91, 2026-05-31T18-58-40Z

## Summary (reset-proof headline)

Subscription actually used: **Claude Max 20x ($200/month)**.

Over the **last 30 days**, this account did **$6,129.41** of API-equivalent usage for **$200** of subscription — a **30.6x** value multiple, i.e. you pay **3.26% of official API pricing**.

This is the figure that matters and it does **not** depend on any quota percentage or extrapolation: it is simply the cost the official API would have charged for the exact same logged usage over a fixed calendar window, compared to what the subscription cost over that same window.

## Why no 100%-quota extrapolation

Anthropic granted **2 mid-week grace resets this week**. The UI currently shows **38% (all models)**, but that percentage only reflects usage since the **last** reset, while the measured token window spans the **whole week** since Monday. So the usual `measured / used%` extrapolation is broken here: it would produce an **upper bound** of ~$22,547.71/month, which is almost certainly overstated. It is reported below for transparency only — **the 30-day measured ratio above is the honest number.**

## Window

- Analysis run: `2026-05-31T18:58:40.515687Z`
- Headline window: last 30 days (`2026-05-01` -> `2026-05-31`)
- Local data available from: `2026-02-25`
- Current weekly limit nominal reset: `2026-06-01 20:59 CEST`

## Weekly history (measured, reset-proof)

Weekly API-equivalent spend vs the weekly slice of the subscription (**$46.15/week**). The weekly quota % for past weeks is **not stored locally** so it cannot be used; the contributor recalls ~50-80% on prior weeks but that is memory only and not relied upon.

| Week (Mon 20:59 CEST) | API-equivalent | Requests | Tokens (B) | vs sub |
|---|---|---|---|---|
| 2026-02-23 | $282.48 | 5,024 | 0.43 | 6.1x |
| 2026-03-02 | $136.29 | 1,866 | 0.19 | 3.0x |
| 2026-03-09 | $292.89 | 2,551 | 0.46 | 6.3x |
| 2026-03-16 | $1,200.45 | 5,435 | 1.49 | 26.0x |
| 2026-03-23 | $534.70 | 1,398 | 0.60 | 11.6x |
| 2026-03-30 | $547.05 | 2,245 | 0.90 | 11.9x |
| 2026-04-06 | $825.88 | 2,997 | 1.21 | 17.9x |
| 2026-04-13 | $1,131.40 | 4,431 | 1.70 | 24.5x |
| 2026-04-20 | $869.67 | 3,279 | 1.32 | 18.8x |
| 2026-04-27 | $2,008.51 | 6,999 | 2.97 | 43.5x |
| 2026-05-04 | $1,101.90 | 3,651 | 1.40 | 23.9x |
| 2026-05-11 | $725.32 | 2,463 | 0.91 | 15.7x |
| 2026-05-18 | $1,591.90 | 5,517 | 2.23 | 34.5x |
| 2026-05-25 *(partial)* | $1,977.26 | 6,159 | 2.43 | 42.8x |

## Current week snapshot (informational, see warning)

- All-models quota used (UI): **38%**
- Mid-week grace resets: **2**
- Measured API-equivalent since Monday: **$1,977.26**
- Upper-bound weekly @100%: **$5,203.32** — monthly **$22,547.71** *(overstated, do not cite)*
- Dominant model: Opus 4.7 (long >150k-context sessions drive huge cache-read volume)

## Codex (deferred)

- Plan: **OpenAI Plus ($20/month)**
- Current week (started): **0%** used
- Weekly resets: **Sat 2026-06-06 22:24 CEST** (from local rate-limit logs)
- Most Codex usage runs on a remote machine (hermes) not present locally, so a local-only measurement (~$27 last week) is unrepresentative. A combined Codex report will follow after the Jun 6 reset.

## Follow-up

- A second Claude PR with a **full clean week** snapshot is planned for **Mon 2026-06-08**.
- A Codex PR is planned after the **2026-06-06** weekly reset.

## Caveats

- API-equivalent value is not Anthropic's real cost.
- 2 mid-week grace resets make the current-week percentage/measurement misaligned; only the upper-bound extrapolation is shown.
- Prior-week quota percentages are unavailable; those extrapolations are intentionally omitted.
- Deduplicated by requestId; synthetic messages excluded from cost.
- All usage is local to a single machine.

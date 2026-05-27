# Codex Effective Token Price, jlalbany

## Summary

Subscription actually used: **OpenAI Pro EUR 114/month (~USD 133.94 at ECB 2026-05-27 EUR/USD 1.1749)**.

Measured Codex usage was **83.0%** of the weekly quota, worth about **$2,556.86 API-equivalent**.

Extrapolated to 100% of the weekly quota, the API-equivalent value is about **$3,080.56/week**, or **$13,349.07/month** using `52 / 12` weeks per month. The effective price is **1.00% of official GPT-5.5 API pricing**.

## Window

- Measurement start: `2026-05-23T20:00:00Z`
- Measurement end: `2026-05-27T15:18:27Z`
- Weekly limit end: `2026-05-30T22:00:00+02:00`
- Monthly extrapolation: `$13,349.07`

## Usage

- Conversations: `219`
- Token events: `25928`
- Input tokens: `3,325,790,039`
- Cached input tokens: `3,195,828,096`
- Uncached input tokens: `129,961,943`
- Output tokens: `10,304,564`
- Reasoning output tokens: `3,625,690`

## Effective Prices

- Input: **$0.05 / 1M**
- Cached input: **$0.01 / 1M**
- Output: **$0.30 / 1M**

## Caveats

- API-equivalent value is not OpenAI's real cost.
- OpenAI API pricing was checked on 2026-05-27 from `https://platform.openai.com/docs/pricing`.
- Subscription price comes from the ChatGPT UI screenshot: `114 EUR/month`, converted to USD using ECB EUR/USD `1.1749` for 2026-05-27.
- The ChatGPT UI screenshot exposed the weekly reset date as `30 mai` but did not expose the exact reset time, so the limit end is recorded as `2026-05-30T22:00:00+02:00` and should be treated as an approximation.
- Logs from other machines are not included unless added through extra cost inputs.
- Error rates are approximate and include normal exploratory command failures.

# Real Analysis: Is the Codex vs Claude "$200 value" comparison honest?

This document interrogates the headline claim from the two reports - that the Codex $200 plan is worth ~$8,600/month while the Claude Max 20x $200 plan is worth ~$18,900/month - and shows, with the underlying data and reproducible math, that **comparing those two numbers as "Claude is worth ~2x more" is misleading**.

Every number below is traced to its source. Confidence levels are stated explicitly at the end.

---

## TL;DR (the verdict)

1. **The output you actually get is nearly identical on both $200 plans:** ~$977/mo (Codex) vs ~$911/mo (Claude), priced at each provider's own API rates. Same real work.
2. **100% of the "2x" gap is in input/cache accounting, not in work delivered.**
3. That cache gap is inflated by three calculation asymmetries: a 10x-amplified extrapolation on the Claude side, Anthropic charging 2x for "cache writes" that Codex has no equivalent for, and Claude re-reading ~2x more context per output token.
4. So the honest statement is: **both $200 plans deliver roughly the same real output; Claude's number only looks bigger because of pricing-model differences and a shaky one-day extrapolation.**

The math in each report is internally consistent. The error is in **placing the two numbers side by side** as if they measured the same thing.

---

## Proof 1: Your real Claude usage is ~93% cache reads

Measured directly from `~/.claude/projects/**/*.jsonl`, deduplicated by `requestId`, filtered to 2026-05-30.

| Token type | Tokens | % of count | API-$ (Opus list) | % of $ |
| --- | --- | --- | --- | --- |
| Cache read | 83,277,832 | 92.7% | $41.64 | 36.8% |
| Cache write | 5,692,904 | 6.3% | $56.93 | 50.3% |
| Fresh input | 295,568 | 0.3% | $1.48 | 1.3% |
| **Output (real work)** | **529,070** | **0.6%** | **$13.23** | **11.7%** |
| Total | 89,795,374 | 100% | $113.27 | 100% |

- 758 deduped requests, **100% Opus 4.8**.
- **~87% of the day's API-equivalent dollars is caching overhead; only ~12% is output.**

This confirms the lived observation: most of what burns is cache, not output.

---

## Why the model "re-reads" (the mechanic)

LLMs are **stateless** - the model keeps no memory between API calls. To continue a conversation, the client must resend the **entire context** on **every** call: system prompt, CLAUDE.md, all prior messages, and every tool result (files read, command output).

In an agentic loop, one task is many API calls (read file -> call, run command -> call, edit -> call). Each call re-sends everything accumulated so far. Your own numbers show the scale:

```
83,277,832 cache-read tokens / 758 requests = ~109,800 tokens re-read per request
```

That ~110K is your living context being re-sent ~758 times today. **Prompt caching does not stop the re-reading; it makes it cheap** (the repeated prefix is billed at the cache-read rate, ~10% of input). So caching is a 90% discount, but the token *count* stays huge because it equals `context size x number of calls`.

---

## Why cache is counted as "value $" (and the honest caveat)

The reports price every token at the provider's public API list price. On the real API you genuinely would be billed for cache reads and cache writes, so the figure is a legitimate **API-equivalent value**.

**Caveat:** that value measures **the cost of keeping the model aware of a long context**, not the value of work delivered. When ~87% of the dollars are cache, the headline "value" is mostly *context overhead*, dressed up as value. The only line that reflects what you received is **output** (plus a little fresh input).

---

## Proof 2: Decomposition of both $200 numbers (the core proof)

Both numbers normalized to **monthly at 100% of quota**, each priced at its own provider's API list.

**Codex** - source: `result/melvynx/codex/2026-05-30T09-13-16Z` (measured at **99%** quota, ~1 week, factor x4.38):

| Bucket | Monthly $ |
| --- | --- |
| Uncached input ("first read", $5/1M) | $2,309 |
| Cached input ("re-read", $0.50/1M) | $5,303 |
| Output ($30/1M) | $977 |
| **Total** | **$8,589** |

**Claude** - source: `result/taka-foo/claude` (measured at **10%** quota, ~1 day, factor x43.33):

| Bucket | Monthly $ |
| --- | --- |
| Cache write 1h ("first read", $10/1M) | $6,654 |
| Cache write 5m ($6.25/1M) | $6 |
| Cache read ("re-read", $0.50/1M) | $11,319 |
| Fresh input ($5/1M) | $1 |
| Output ($25/1M) | $911 |
| **Total** | **$18,891** |

### Test 1 - Output only (the real, least-gameable "work")

> **Codex $977/mo vs Claude $911/mo -> roughly EQUAL.**

The actual generated work is the same for your $200. (In raw output tokens: Codex ~32.6M/mo vs Claude ~36.4M/mo, a 1.12x edge to Claude - nowhere near 2x.)

### Test 2 - Where the gap actually lives

> Input/cache side: **Codex $7,612 vs Claude $17,980 (2.4x).**
> 100% of the headline gap is here. None of it is in output.

### Test 3 - Pricing-model asymmetry (cache writes)

Anthropic charges a **premium** for creating a cache entry (cache write 1h = $10/1M, *double* the $5 input rate). OpenAI/Codex has **no separate cache-write charge** - the first read is just normal input at $5/1M.

> Re-price Claude's cache writes at Codex's $5 "first read" rate:
> **Claude value falls $18,891 -> $15,562.** Same tokens, same work, different price list.

### Test 4 - Extrapolation reliability (the biggest problem)

| Plan | Measured quota | Scale factor to monthly@100% | Error sensitivity |
| --- | --- | --- | --- |
| Codex | 99% | x4.38 | 1% error -> ~1% swing (basically measured) |
| Claude | 10% | x43.33 | 1% error in the 10% reading -> ~10% swing |

The Claude figure is **one day multiplied by ~10**. If taka-foo's sampled day ran just **1.5x heavier** than their true weekly average, the real monthly value is **~$12,600, not $18,900**. The Codex figure has no comparable wobble.

> You are comparing a **measurement** (Codex) against a **guess with a 10x error multiplier** (Claude).

---

## The honest comparison

| Question | Answer |
| --- | --- |
| Which $200 plan does more real work? | Roughly a **tie** (output ~$977 vs ~$911/mo). |
| Which provider's API would bill more for this usage at full quota? | Claude - but because it **charges more for the same caching** and the number is a **10x extrapolation**, not because you get more done. |
| Is "$9k vs $20k = Claude worth 2x" fair? | **No.** It compares a measured number to a one-day x10 guess, across two pricing models that treat caching differently, on a metric dominated by context overhead. |

**The deeper trap is the word "value."** "API-equivalent value" measures *what the provider's meter would charge*, so it rewards verbose context, heavy cache re-reads, and a pricier cache-write rate. A plan can score "2x more valuable" while delivering identical output. That is exactly what happened.

---

## Why your limit also drains fast (related, supported externally)

- Subscription limits are **compute/cost-weighted, not message-counted** ("depends on the length and complexity of your conversations" - Anthropic). Big cached contexts and especially **cache writes** consume quota.
- **Opus is the multiplier.** Anthropic states "Opus costs several times more per turn than Sonnet," and Max 20x has a small Opus allowance (community estimate ~24-40 Opus-hours/week) versus a much larger separate Sonnet pool. You are 100% Opus.
- **A real 2026 bug made it worse:** Anthropic cut Claude Code's default cache TTL from 1 hour to 5 minutes, so caches expire faster -> more expensive cache **re-writes** (the $56.93 line in your day) -> quota drains faster. Anthropic publicly acknowledged the quota-drain issue.

Practical levers: use **Sonnet** for routine work (separate, larger pool, far cheaper per turn), `/clear` and `/compact` often (your drain is `context size x calls`), and work in continuous bursts so the cache stays warm.

---

## Confidence levels (assurance)

**Proven directly from data in this repo / your machine (high confidence):**
- Your usage today is 92.7% cache read, 0.6% output (re-run the command below).
- Output value is ~equal across plans ($977 vs $911/mo).
- 100% of the headline gap is input/cache, not output.
- Codex first-read is $5/1M; Claude cache write 1h is $10/1M (the 2x pricing asymmetry).
- Scale factors are x4.38 (Codex, 99%) and x43.33 (Claude, 10%).

**Inferred from the calculation, robust (high confidence):**
- Normalizing cache-write price drops Claude to ~$15.6k; the residual gap is context re-read volume (621 vs 326 cache-reads per output token).
- The x10 extrapolation makes the Claude headline unreliable; a 1.5x-heavy sample day implies ~$12.6k.

**Supported by external reporting, not by repo data (medium confidence):**
- Exact subscription-limit formula (Anthropic does not publish the per-token weights).
- Opus-vs-Sonnet multiplier magnitude and the Max 20x hour estimates.
- The cache-TTL change and quota-drain bug (documented by press, acknowledged by Anthropic).

---

## How to reproduce (so you do not have to trust me)

Your usage today, deduped by request, by token type:

```bash
python3 - << 'EOF'
import json, glob, os
from collections import defaultdict
TODAY="2026-05-30"
seen=set(); tot=defaultdict(int); reqs=0
for fp in glob.glob(os.path.expanduser("~/.claude/projects/**/*.jsonl"), recursive=True):
    for line in open(fp, errors="ignore"):
        try: o=json.loads(line)
        except: continue
        if o.get("type")!="assistant": continue
        m=o.get("message");
        if not isinstance(m,dict) or not m.get("usage"): continue
        if not o.get("timestamp","").startswith(TODAY): continue
        rid=o.get("requestId") or m.get("id")
        if rid and rid in seen: continue
        if rid: seen.add(rid)
        reqs+=1
        for k in ("input_tokens","cache_creation_input_tokens","cache_read_input_tokens","output_tokens"):
            tot[k]+=m["usage"].get(k,0) or 0
g=sum(tot.values())
print("requests:",reqs,"total tokens:",g)
for k,v in tot.items(): print(f"  {k:30} {v:>14,} ({v/g*100:.1f}%)")
EOF
```

Source data: `result/melvynx/codex/2026-05-30T09-13-16Z/data.json` (Codex), `result/taka-foo/claude/data.json` (Claude Max 20x), and the supporting Max 5x / Pro samples in `result/*/claude/`.

External sources: [Anthropic - Models, usage & limits in Claude Code](https://support.claude.com/en/articles/14552983-models-usage-and-limits-in-claude-code), [The Register - quotas running out too fast](https://www.theregister.com/2026/03/31/anthropic_claude_code_limits/), [XDA - the 1-hour cache nerf](https://www.xda-developers.com/anthropic-quietly-nerfed-claude-code-hour-cache-token-budget/), [piunikaweb - cache bugs blamed for drain](https://piunikaweb.com/2026/03/31/claude-cache-bugs-tokens-20x-more-anthropic-investigating/).

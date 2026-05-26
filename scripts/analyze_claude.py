#!/usr/bin/env python3
"""Calculate effective Claude token prices from local .claude logs."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PRICES = {
    "opus": {"input": 5.0, "cache_write_5m": 6.25, "cache_write_1h": 10.0, "cache_read": 0.5, "output": 25.0},
    "sonnet": {"input": 3.0, "cache_write_5m": 3.75, "cache_write_1h": 6.0, "cache_read": 0.3, "output": 15.0},
    "haiku": {"input": 1.0, "cache_write_5m": 1.25, "cache_write_1h": 2.0, "cache_read": 0.1, "output": 5.0},
}


def parse_dt(value: str) -> datetime:
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"
    parsed = datetime.fromisoformat(value)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def family(model: str) -> str:
    lower = (model or "").lower()
    if "opus" in lower:
        return "opus"
    if "sonnet" in lower:
        return "sonnet"
    if "haiku" in lower:
        return "haiku"
    if "synthetic" in lower:
        return "synthetic"
    return "unknown"


def cost_for(model: str, usage: dict[str, Any]) -> tuple[float, str]:
    fam = family(model)
    if fam not in PRICES:
        return 0.0, fam
    price = PRICES[fam]
    cache = usage.get("cache_creation") or {}
    write_5m = int(cache.get("ephemeral_5m_input_tokens") or 0)
    write_1h = int(cache.get("ephemeral_1h_input_tokens") or 0)
    cache_creation_total = int(usage.get("cache_creation_input_tokens") or 0)
    unclassified_write = max(0, cache_creation_total - write_5m - write_1h)
    return (
        int(usage.get("input_tokens") or 0) / 1_000_000 * price["input"]
        + int(usage.get("output_tokens") or 0) / 1_000_000 * price["output"]
        + int(usage.get("cache_read_input_tokens") or 0) / 1_000_000 * price["cache_read"]
        + write_5m / 1_000_000 * price["cache_write_5m"]
        + write_1h / 1_000_000 * price["cache_write_1h"]
        + unclassified_write / 1_000_000 * price["cache_write_5m"],
        fam,
    )


def money(value: float) -> str:
    return f"${value:,.2f}"


def analyze(args: argparse.Namespace) -> dict[str, Any]:
    claude_home = Path(args.claude_home).expanduser()
    projects = claude_home / "projects"
    start = parse_dt(args.start)
    end = parse_dt(args.end) if args.end else datetime.now(timezone.utc)
    monthly_price = float(args.monthly_price)
    weekly_price = monthly_price / (52 / 12)
    used_percent = float(args.used_percent)

    files_scanned = 0
    sessions: set[str] = set()
    seen: set[str] = set()
    raw_assistant_usage_events = 0
    deduped_assistant_requests = 0
    duplicates_skipped = 0
    synthetic_requests = 0
    synthetic_api_errors = 0
    requests_by_model: Counter[str] = Counter()
    requests_by_family: Counter[str] = Counter()
    tokens: Counter[str] = Counter()
    cost_by_model: defaultdict[str, float] = defaultdict(float)
    cost_by_family: defaultdict[str, float] = defaultdict(float)

    for path in sorted(projects.rglob("*.jsonl")):
        files_scanned += 1
        try:
            handle = path.open("r", encoding="utf-8", errors="replace")
        except OSError:
            continue
        with handle:
            for line_no, line in enumerate(handle, 1):
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError:
                    continue
                timestamp = obj.get("timestamp")
                if not timestamp:
                    continue
                try:
                    ts = parse_dt(timestamp)
                except ValueError:
                    continue
                if ts < start or ts > end:
                    continue
                session_id = obj.get("sessionId") or path.stem
                sessions.add(session_id)
                if obj.get("type") != "assistant":
                    continue
                message = obj.get("message") or {}
                usage = message.get("usage") or {}
                if not usage:
                    continue
                raw_assistant_usage_events += 1
                dedupe_key = obj.get("requestId") or message.get("id") or f"{session_id}:{timestamp}:{line_no}:{json.dumps(usage, sort_keys=True)}"
                if dedupe_key in seen:
                    duplicates_skipped += 1
                    continue
                seen.add(dedupe_key)
                deduped_assistant_requests += 1

                model = message.get("model") or "unknown"
                fam = family(model)
                requests_by_model[model] += 1
                requests_by_family[fam] += 1
                if fam == "synthetic":
                    synthetic_requests += 1
                    text = json.dumps(message.get("content"), ensure_ascii=False).lower()
                    if "api error" in text or "overloaded" in text or "rate limit" in text:
                        synthetic_api_errors += 1

                cache = usage.get("cache_creation") or {}
                write_5m = int(cache.get("ephemeral_5m_input_tokens") or 0)
                write_1h = int(cache.get("ephemeral_1h_input_tokens") or 0)
                values = {
                    "input_tokens": int(usage.get("input_tokens") or 0),
                    "cache_creation_input_tokens": int(usage.get("cache_creation_input_tokens") or 0),
                    "cache_write_5m_tokens": write_5m,
                    "cache_write_1h_tokens": write_1h,
                    "cache_read_input_tokens": int(usage.get("cache_read_input_tokens") or 0),
                    "output_tokens": int(usage.get("output_tokens") or 0),
                }
                tokens.update(values)
                cost, cost_family = cost_for(model, usage)
                cost_by_model[model] += cost
                cost_by_family[cost_family] += cost

    measured_total = sum(cost_by_model.values())
    weekly_api_value = measured_total / (used_percent / 100) if used_percent else 0
    monthly_api_value = weekly_api_value * (52 / 12)
    effective_ratio = weekly_price / weekly_api_value if weekly_api_value else 0

    return {
        "schema_version": "1.0",
        "contributor": {"github_username": args.username},
        "tool": "claude",
        "subscription": {
            "actual_subscription_used": args.subscription,
            "monthly_price_usd": monthly_price,
            "weekly_price_usd": weekly_price,
        },
        "weekly_limit": {
            "all_models_used_percent": used_percent,
            "used_percent_source": args.used_percent_source,
            "limit_start_at": start.isoformat().replace("+00:00", "Z"),
            "limit_end_at": args.limit_end,
        },
        "measurement_window": {
            "start_at": start.isoformat().replace("+00:00", "Z"),
            "end_at": end.isoformat().replace("+00:00", "Z"),
        },
        "api_pricing": {
            "provider": "anthropic",
            "model_baseline": "claude-opus-4.7",
            "pricing_checked_at": args.pricing_checked_at,
            "currency": "USD",
            "per_1m_tokens": {
                "opus": PRICES["opus"],
                "sonnet": PRICES["sonnet"],
                "haiku": PRICES["haiku"],
            },
        },
        "usage": {
            "files_scanned": files_scanned,
            "sessions": len(sessions),
            "raw_assistant_usage_events": raw_assistant_usage_events,
            "deduped_assistant_requests": deduped_assistant_requests,
            "duplicates_skipped": duplicates_skipped,
            "requests_by_model": dict(requests_by_model),
            "requests_by_family": dict(requests_by_family),
            "tokens": dict(tokens),
        },
        "cost_breakdown_usd": {
            "by_model": dict(cost_by_model),
            "by_family": dict(cost_by_family),
            "measured_total_api_equivalent": measured_total,
            "weekly_api_value_at_100_percent": weekly_api_value,
            "monthly_api_value_at_100_percent": monthly_api_value,
        },
        "effective_prices": {
            "effective_api_ratio": effective_ratio,
            "effective_api_percent": effective_ratio * 100,
            "opus_non_fast_per_1m_tokens_usd": {
                key: value * effective_ratio for key, value in PRICES["opus"].items()
            },
        },
        "errors": {
            "synthetic_requests": synthetic_requests,
            "synthetic_request_rate_percent": (synthetic_requests / deduped_assistant_requests * 100) if deduped_assistant_requests else 0,
            "synthetic_api_error_requests": synthetic_api_errors,
            "api_error_rate_approx_percent": (synthetic_api_errors / deduped_assistant_requests * 100) if deduped_assistant_requests else 0,
        },
        "assumptions": [
            "API-equivalent value is not Anthropic's real cost.",
            "Assistant usage rows are deduplicated by requestId when available.",
            "Claude usage percentage is not stored in local logs and usually must come from the UI.",
        ],
    }


def write_outputs(data: dict[str, Any], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "data.json").write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    usage = data["usage"]
    tokens = usage["tokens"]
    costs = data["cost_breakdown_usd"]
    eff = data["effective_prices"]
    analysis = f"""# Claude Effective Token Price, {data['contributor']['github_username']}

## Summary

Subscription actually used: **{data['subscription']['actual_subscription_used']}**.

Measured Claude usage was **{data['weekly_limit']['all_models_used_percent']}%** of the weekly All models quota, worth about **{money(costs['measured_total_api_equivalent'])} API-equivalent**.

Extrapolated to 100% of the weekly quota, the API-equivalent value is about **{money(costs['weekly_api_value_at_100_percent'])}/week**, or **{money(costs['monthly_api_value_at_100_percent'])}/month** using `52 / 12` weeks per month. The effective price is **{eff['effective_api_percent']:.2f}% of official Opus API pricing**.

## Window

- Measurement start: `{data['measurement_window']['start_at']}`
- Measurement end: `{data['measurement_window']['end_at']}`
- Weekly limit end: `{data['weekly_limit']['limit_end_at']}`
- Monthly extrapolation: `{money(costs['monthly_api_value_at_100_percent'])}`

## Usage

- Conversations: `{usage['sessions']}`
- Raw assistant usage events: `{usage['raw_assistant_usage_events']}`
- Deduped assistant requests: `{usage['deduped_assistant_requests']}`
- Duplicates skipped: `{usage['duplicates_skipped']}`
- Input tokens: `{tokens.get('input_tokens', 0):,}`
- Cache creation tokens: `{tokens.get('cache_creation_input_tokens', 0):,}`
- Cache read tokens: `{tokens.get('cache_read_input_tokens', 0):,}`
- Output tokens: `{tokens.get('output_tokens', 0):,}`

## Effective Opus Prices

- Input: **{money(eff['opus_non_fast_per_1m_tokens_usd']['input'])} / 1M**
- Cache write 5m: **{money(eff['opus_non_fast_per_1m_tokens_usd']['cache_write_5m'])} / 1M**
- Cache write 1h: **{money(eff['opus_non_fast_per_1m_tokens_usd']['cache_write_1h'])} / 1M**
- Cache read: **{money(eff['opus_non_fast_per_1m_tokens_usd']['cache_read'])} / 1M**
- Output: **{money(eff['opus_non_fast_per_1m_tokens_usd']['output'])} / 1M**

## Caveats

- API-equivalent value is not Anthropic's real cost.
- Claude weekly usage percentage must usually come from the UI.
- Error rates are approximate and synthetic messages are counted separately.
"""
    (output_dir / "analysis.md").write_text(analysis, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--claude-home", default="~/.claude")
    parser.add_argument("--start", required=True)
    parser.add_argument("--end", help="Measurement end ISO timestamp. Defaults to now.")
    parser.add_argument("--limit-end", required=True)
    parser.add_argument("--used-percent", required=True)
    parser.add_argument("--used-percent-source", default="user_ui")
    parser.add_argument("--monthly-price", required=True)
    parser.add_argument("--subscription", default="Claude Max")
    parser.add_argument("--username", required=True)
    parser.add_argument("--pricing-checked-at", default=datetime.now(timezone.utc).date().isoformat())
    parser.add_argument("--output-dir")
    args = parser.parse_args()

    data = analyze(args)
    if args.output_dir:
        write_outputs(data, Path(args.output_dir))
    print(json.dumps(data, indent=2))


if __name__ == "__main__":
    main()

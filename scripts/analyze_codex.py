#!/usr/bin/env python3
"""Calculate effective Codex token prices from local .codex logs."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


DEFAULT_PRICING = {
    "provider": "openai",
    "model_baseline": "gpt-5.5",
    "currency": "USD",
    "per_1m_tokens": {
        "input": 5.0,
        "cached_input": 0.5,
        "output": 30.0,
    },
}


def parse_dt(value: str) -> datetime:
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"
    parsed = datetime.fromisoformat(value)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def money(value: float) -> str:
    return f"${value:,.2f}"


def iter_codex_files(codex_home: Path) -> list[Path]:
    files: list[Path] = []
    for pattern in ("sessions/**/*.jsonl", "archived_sessions/*.jsonl"):
        files.extend(codex_home.glob(pattern))
    for extra_dir in ("archives", "archive", "archived"):
        path = codex_home / extra_dir
        if path.exists():
            files.extend(path.rglob("*.jsonl"))
    return sorted(set(files))


def session_id_from_filename(path: Path) -> str:
    match = re.search(r"([0-9a-f]{8}-[0-9a-f-]{27})", path.name)
    return match.group(1) if match else path.stem


def analyze(args: argparse.Namespace) -> dict[str, Any]:
    codex_home = Path(args.codex_home).expanduser()
    start = parse_dt(args.start)
    end = parse_dt(args.end) if args.end else datetime.now(timezone.utc)
    monthly_price = float(args.monthly_price)
    weekly_price = monthly_price / (52 / 12)
    used_percent = float(args.used_percent)
    pricing = DEFAULT_PRICING
    prices = pricing["per_1m_tokens"]

    sessions: set[str] = set()
    files_scanned = 0
    events = 0
    token_events = 0
    tokens: Counter[str] = Counter()
    tool_outputs = 0
    failed_tool_outputs = 0
    assistant_messages = 0
    assistant_api_errors = 0
    max_secondary_used_percent = 0.0
    last_secondary_used_percent: float | None = None

    for path in iter_codex_files(codex_home):
        files_scanned += 1
        current_session_id = session_id_from_filename(path)
        touched = False
        try:
            handle = path.open("r", encoding="utf-8", errors="replace")
        except OSError:
            continue
        with handle:
            for line in handle:
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
                touched = True
                events += 1
                payload = obj.get("payload") or {}
                if obj.get("type") == "session_meta":
                    current_session_id = (payload.get("id") or current_session_id)
                if payload.get("type") == "token_count":
                    token_events += 1
                    info = payload.get("info") or {}
                    usage = info.get("last_token_usage") or {}
                    for key in (
                        "input_tokens",
                        "cached_input_tokens",
                        "output_tokens",
                        "reasoning_output_tokens",
                        "total_tokens",
                    ):
                        tokens[key] += int(usage.get(key) or 0)
                    secondary = ((payload.get("rate_limits") or {}).get("secondary") or {}).get("used_percent")
                    if isinstance(secondary, (int, float)):
                        last_secondary_used_percent = float(secondary)
                        max_secondary_used_percent = max(max_secondary_used_percent, float(secondary))
                if obj.get("type") == "response_item" and payload.get("type") == "function_call_output":
                    tool_outputs += 1
                    raw_output = payload.get("output") or ""
                    output = raw_output if isinstance(raw_output, str) else json.dumps(raw_output, ensure_ascii=False)
                    match = re.search(r"Process exited with code ([-0-9]+)", output)
                    if match and match.group(1) != "0":
                        failed_tool_outputs += 1
                if obj.get("type") == "response_item" and payload.get("type") == "message" and payload.get("role") == "assistant":
                    assistant_messages += 1
                    text = json.dumps(payload, ensure_ascii=False).lower()
                    if "api error" in text or "rate limit" in text or "overloaded" in text:
                        assistant_api_errors += 1
        if touched:
            sessions.add(current_session_id)

    uncached_input = max(0, tokens["input_tokens"] - tokens["cached_input_tokens"])
    measured_cost = (
        uncached_input / 1_000_000 * prices["input"]
        + tokens["cached_input_tokens"] / 1_000_000 * prices["cached_input"]
        + tokens["output_tokens"] / 1_000_000 * prices["output"]
    )
    extra_costs: dict[str, float] = {}
    for item in args.extra_cost or []:
        label, raw_value = item.split("=", 1)
        extra_costs[label] = float(raw_value)
    measured_total = measured_cost + sum(extra_costs.values())
    weekly_api_value = measured_total / (used_percent / 100) if used_percent else 0
    monthly_api_value = weekly_api_value * (52 / 12)
    effective_ratio = weekly_price / weekly_api_value if weekly_api_value else 0

    return {
        "schema_version": "1.0",
        "contributor": {"github_username": args.username},
        "tool": "codex",
        "subscription": {
            "actual_subscription_used": args.subscription,
            "monthly_price_usd": monthly_price,
            "weekly_price_usd": weekly_price,
        },
        "weekly_limit": {
            "used_percent": used_percent,
            "used_percent_source": args.used_percent_source,
            "observed_max_secondary_used_percent": max_secondary_used_percent,
            "observed_last_secondary_used_percent": last_secondary_used_percent,
            "limit_start_at": start.isoformat().replace("+00:00", "Z"),
            "limit_end_at": args.limit_end,
        },
        "measurement_window": {
            "start_at": start.isoformat().replace("+00:00", "Z"),
            "end_at": end.isoformat().replace("+00:00", "Z"),
        },
        "api_pricing": pricing | {"pricing_checked_at": args.pricing_checked_at},
        "usage": {
            "files_scanned": files_scanned,
            "sessions": len(sessions),
            "events": events,
            "token_events": token_events,
            "input_tokens": tokens["input_tokens"],
            "cached_input_tokens": tokens["cached_input_tokens"],
            "uncached_input_tokens": uncached_input,
            "output_tokens": tokens["output_tokens"],
            "reasoning_output_tokens": tokens["reasoning_output_tokens"],
            "total_tokens": tokens["total_tokens"],
        },
        "cost_breakdown_usd": {
            "uncached_input": uncached_input / 1_000_000 * prices["input"],
            "cached_input": tokens["cached_input_tokens"] / 1_000_000 * prices["cached_input"],
            "output": tokens["output_tokens"] / 1_000_000 * prices["output"],
            "local_total": measured_cost,
            "extra_costs": extra_costs,
            "measured_total_api_equivalent": measured_total,
            "weekly_api_value_at_100_percent": weekly_api_value,
            "monthly_api_value_at_100_percent": monthly_api_value,
        },
        "effective_prices": {
            "effective_api_ratio": effective_ratio,
            "effective_api_percent": effective_ratio * 100,
            "non_fast_per_1m_tokens_usd": {
                "input": prices["input"] * effective_ratio,
                "cached_input": prices["cached_input"] * effective_ratio,
                "output": prices["output"] * effective_ratio,
            },
        },
        "errors": {
            "tool_outputs": tool_outputs,
            "failed_tool_outputs": failed_tool_outputs,
            "tool_command_error_rate_approx_percent": (failed_tool_outputs / tool_outputs * 100) if tool_outputs else 0,
            "assistant_messages": assistant_messages,
            "assistant_api_error_messages": assistant_api_errors,
            "model_api_error_rate_approx_percent": (assistant_api_errors / assistant_messages * 100) if assistant_messages else 0,
        },
        "assumptions": [
            "API-equivalent value is not OpenAI's real cost.",
            "GPT-5.5 official API pricing is used as the baseline.",
            "Codex token totals are summed from last_token_usage to avoid cumulative double counting.",
        ],
    }


def write_outputs(data: dict[str, Any], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "data.json").write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    usage = data["usage"]
    costs = data["cost_breakdown_usd"]
    eff = data["effective_prices"]
    analysis = f"""# Codex Effective Token Price, {data['contributor']['github_username']}

## Summary

Subscription actually used: **{data['subscription']['actual_subscription_used']}**.

Measured Codex usage was **{data['weekly_limit']['used_percent']}%** of the weekly quota, worth about **{money(costs['measured_total_api_equivalent'])} API-equivalent**.

Extrapolated to 100% of the weekly quota, the API-equivalent value is about **{money(costs['weekly_api_value_at_100_percent'])}/week**, or **{money(costs['monthly_api_value_at_100_percent'])}/month** using `52 / 12` weeks per month. The effective price is **{eff['effective_api_percent']:.2f}% of official GPT-5.5 API pricing**.

## Window

- Measurement start: `{data['measurement_window']['start_at']}`
- Measurement end: `{data['measurement_window']['end_at']}`
- Weekly limit end: `{data['weekly_limit']['limit_end_at']}`
- Monthly extrapolation: `{money(costs['monthly_api_value_at_100_percent'])}`

## Usage

- Conversations: `{usage['sessions']}`
- Token events: `{usage['token_events']}`
- Input tokens: `{usage['input_tokens']:,}`
- Cached input tokens: `{usage['cached_input_tokens']:,}`
- Uncached input tokens: `{usage['uncached_input_tokens']:,}`
- Output tokens: `{usage['output_tokens']:,}`
- Reasoning output tokens: `{usage['reasoning_output_tokens']:,}`

## Effective Prices

- Input: **{money(eff['non_fast_per_1m_tokens_usd']['input'])} / 1M**
- Cached input: **{money(eff['non_fast_per_1m_tokens_usd']['cached_input'])} / 1M**
- Output: **{money(eff['non_fast_per_1m_tokens_usd']['output'])} / 1M**

## Caveats

- API-equivalent value is not OpenAI's real cost.
- Logs from other machines are not included unless added through extra cost inputs.
- Error rates are approximate and include normal exploratory command failures.
"""
    (output_dir / "analysis.md").write_text(analysis, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--codex-home", default="~/.codex")
    parser.add_argument("--start", required=True, help="Measurement start ISO timestamp.")
    parser.add_argument("--end", help="Measurement end ISO timestamp. Defaults to now.")
    parser.add_argument("--limit-end", required=True, help="Weekly limit end/reset timestamp for reporting.")
    parser.add_argument("--used-percent", required=True)
    parser.add_argument("--used-percent-source", default="user_ui")
    parser.add_argument("--monthly-price", required=True)
    parser.add_argument("--subscription", default="OpenAI Pro")
    parser.add_argument("--username", required=True)
    parser.add_argument("--pricing-checked-at", default=datetime.now(timezone.utc).date().isoformat())
    parser.add_argument("--extra-cost", action="append", help="Extra API-equivalent cost as label=value.")
    parser.add_argument("--output-dir")
    args = parser.parse_args()

    data = analyze(args)
    if args.output_dir:
        write_outputs(data, Path(args.output_dir))
    print(json.dumps(data, indent=2))


if __name__ == "__main__":
    main()

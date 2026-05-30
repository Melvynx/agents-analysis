# Codex Max20 Report

This report summarizes the available community analysis files and explicitly ignores any "fast" vs "no fast" split because the data model does not expose that signal.

## Scope

Source data comes from all `result/*/*/*/data.json` files in this repo.

- Files reviewed: 10
- Plan slices: Codex and Claude runs
- Codex-only runs: 6
- Timestamp range: 2026-04-20 to 2026-05-30

## Fast/No-Fast Question

The current Codex analyzer reads only token counters (`input`, `cached_input`, `output`, `reasoning_output`, `total_tokens`) and does not classify fast mode.

- There is no field used in scoring for model speed tier.
- Reported values are therefore mixed/aggregated at the non-fast pricing baseline used by the script.
- The script is [scripts/analyze_codex.py](/Users/melvynx/Developer/agents-analysis/scripts/analyze_codex.py).

## Codex $200 Findings

Only Codex runs with subscription string `$200`:

- [result/melvynx/codex/2026-05-26T20-34-35Z](/Users/melvynx/Developer/agents-analysis/result/melvynx/codex/2026-05-26T20-34-35Z)
- [result/melvynx/codex/2026-05-28T09-35-22Z](/Users/melvynx/Developer/agents-analysis/result/melvynx/codex/2026-05-28T09-35-22Z)
- [result/melvynx/codex/2026-05-30T09-09-21Z](/Users/melvynx/Developer/agents-analysis/result/melvynx/codex/2026-05-30T09-09-21Z)
- [result/melvynx/codex/2026-05-30T09-13-16Z](/Users/melvynx/Developer/agents-analysis/result/melvynx/codex/2026-05-30T09-13-16Z)

Key aggregates for these 4 runs:

- Average measured window value: `$1,649.90`
- Average 100% weekly equivalent: `$9,816.83` per month
- Effective API-equivalent rate: about `2.07%` of official GPT-5.5 pricing
- Window usage range: `44.0%` to `99.0%`
- Monthly equivalent range (100% weekly): `11,575.09` to `8,514.11`

## Last Window (reference point)

Latest run: `2026-05-30T09-13-16Z`.

- Used percent of quota: `99.0%`
- Measured window value: `$1,967.16`
- Window normalized to 100%: `$1,987.03` for that week
- File: [result/melvynx/codex/2026-05-30T09-13-16Z/data.json](/Users/melvynx/Developer/agents-analysis/result/melvynx/codex/2026-05-30T09-13-16Z/data.json)

## `$20` and `$100` baselines (for multiplier view)

- `$20` Codex sample: only one run in this repo, monthly-equivalent at 100% is `$985.27` ([tidic84 2026-04-20](/Users/melvynx/Developer/agents-analysis/result/tidic84/codex/2026-04-20T00-00-00Z/data.json))
- `$100` Codex sample is not present in this dataset
- `$200` average monthly-equivalent is substantially above `$20` sample at current pace, but this is expected with different usage windows and is not a direct linear comparison.

## Practical Conclusion

- Use the `$200` Codex runs as the best signal in this repo for your current plan behavior.
- Any "fast mode" uplift cannot be added safely from available data.
- If you need a fast split, we need raw session payloads containing a fast indicator; currently only aggregated token logs are available.

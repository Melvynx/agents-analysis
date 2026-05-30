# Results

Results are organized by GitHub username and tool:

```text
result/<github-username>/<tool>/<analysis-timestamp>/data.json
result/<github-username>/<tool>/<analysis-timestamp>/analysis.md
```

Use the measurement end time in UTC for `<analysis-timestamp>`, formatted like `YYYY-MM-DDTHH-MM-SSZ`. This lets the same contributor add multiple analyses during one weekly quota window.

Supported tool folder names:

- `codex`
- `claude`

Do not add raw `.codex` or `.claude` logs here. Only aggregate usage data should be committed.

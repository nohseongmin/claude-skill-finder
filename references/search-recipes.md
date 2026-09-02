# Search recipes

Two queries, maximum. Pick the row that matches what is missing.

## Looking for a skill

| Situation | Query |
|---|---|
| A vendor owns this stack | `<vendor> skills in:name` or `<vendor> agent-skills in:name` |
| Any skill for a domain | `path:**/SKILL.md <domain>` (code search) |
| Browse the ecosystem | `topic:claude-skills` / `topic:agent-skills` |
| Curated lists | `awesome claude skills in:name` |

## Looking for a reference implementation

| Situation | Query |
|---|---|
| Library or pattern | `<core function> <language> stars:>200 pushed:><last year>` |
| Protocol or format work | `<format> parser <language> stars:>200` |
| "How does anyone do this" | code search on the exact API symbol, not prose |

## Judging a hit without cloning it

```bash
gh api repos/<owner>/<name> --jq '"\(.stargazers_count) stars, pushed \(.pushed_at[0:10]), \(.license.spdx_id)"'
```

Three numbers decide it: stars, last push, license. Vendor-owned repos skip the
star threshold and nothing else.

## When to stop

- Vendor repo found - stop, that is the answer
- Two searches, no gate-passing hit - stop, build it directly
- Only unlicensed or stale hits - stop, they are not usable anyway

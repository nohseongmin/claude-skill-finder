# Vendor skill catalog

Skills published by the people who own the stack. These skip the star gate: if the
task touches one of these, that repo is the reference, and stage 2 is unnecessary.

Verified 2026-09-02. Re-check any row before relying on it:

```bash
gh api repos/<owner>/<name> --jq '"\(.stargazers_count) stars, pushed \(.pushed_at[0:10])"'
```

## Anthropic

| Repo | Ships |
|---|---|
| [anthropics/skills](https://github.com/anthropics/skills) | `docx` `pdf` `pptx` `xlsx` `canvas-design` `frontend-design` `webapp-testing` `mcp-builder` `skill-creator` `artifacts-builder` `algorithmic-art` `theme-factory` `brand-guidelines` |

Most harnesses already bundle the document skills. Check locally before cloning.

## By stack

| Stack | Repo | Reach for it when |
|---|---|---|
| Next.js, React, deploys | [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills) | the frontend or its caching gets non-trivial |
| React Native, Expo | [expo/skills](https://github.com/expo/skills) | anything aimed at an app store |
| Postgres, auth, storage | [supabase/agent-skills](https://github.com/supabase/agent-skills) | SQLite stops being enough |
| Auth | [better-auth/skills](https://github.com/better-auth/skills) | rolling your own login instead of OAuth |
| Payments | [stripe/ai](https://github.com/stripe/ai) | international checkout |
| Error monitoring | [getsentry/skills](https://github.com/getsentry/skills) | the thing now has users |
| Edge, agents, MCP | [cloudflare/skills](https://github.com/cloudflare/skills) | serverless or an agent backend |
| Serverless Postgres | [neondatabase/agent-skills](https://github.com/neondatabase/agent-skills) | branch-per-PR databases |
| Analytics at volume | [ClickHouse/agent-skills](https://github.com/ClickHouse/agent-skills) | log or event scale |
| Model hosting | [replicate/skills](https://github.com/replicate/skills), [fal-ai-community/skills](https://github.com/fal-ai-community/skills) | image, audio or video inference |
| Scraping | [firecrawl/cli](https://github.com/firecrawl/cli) | collection is the product |
| Programmatic video | [remotion-dev/skills](https://github.com/remotion-dev/skills) | shorts or motion rendered from code |
| Design to code | [google-labs-code/stitch-skills](https://github.com/google-labs-code/stitch-skills), [google-gemini/gemini-skills](https://github.com/google-gemini/gemini-skills) | a mock needs to become UI |
| Security review | [trailofbits/skills](https://github.com/trailofbits/skills) | crypto, memory safety, supply chain |

## Adding your own

Local-only entries belong in a sibling file the skill also reads, not in this one.
This table is the shared, verifiable part; your private catalog is yours.

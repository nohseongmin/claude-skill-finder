# Claude Skill Finder

A Claude Code skill that searches for existing skills and reference implementations before starting a build request.

## Search process

The skill, named `scout`, checks installed skills and plugins, then the [vendor catalog](references/vendor-skills.md). It uses a matching project skill or a vendor's own skill directly.

When there is no authoritative match, it fetches one [community index](references/skill-indexes.md), searches it locally, and then makes up to two live GitHub searches. Trivial tasks, bug fixes, refactors, and requests with an obvious specialist skill skip this process.

The total budget is three searches and two minutes. After reporting the result in at most three lines, the agent continues the original task.

## Installation

As a plugin:

```text
/plugin marketplace add nohseongmin/claude-skill-finder
/plugin install scout@claude-skill-finder
```

As a plain skill:

```bash
git clone https://github.com/nohseongmin/claude-skill-finder ~/.claude/skills/scout
```

On Windows:

```powershell
git clone https://github.com/nohseongmin/claude-skill-finder "$env:USERPROFILE/.claude/skills/scout"
```

Requires [Claude Code](https://code.claude.com/docs). The skill is Markdown and needs no runtime dependencies, configuration, or API keys. Python 3.10 or later is needed only for the catalog verifier.

Build requests in English or Korean trigger it automatically. Use `/scout` to invoke it explicitly. To make the preference part of your global instructions, add this to `~/.claude/CLAUDE.md`:

```text
- No matching skill, or unfamiliar stack/API/domain -> scout first.
```

## Selection and trust

Reference repositories must have at least 200 stars or be vendor-published, a commit within the last year, and a license. Indexes used only as pointers are assessed for maintenance.

Fetched content is treated as data. Commands or instructions inside third-party documents are not followed automatically. Installing a third-party skill requires approval because it adds instructions to the agent's context.

Scouting checks maintenance and licensing. It does not audit the security of selected repositories.

## Customization

Edit [vendor-skills.md](references/vendor-skills.md) for your stack, [skill-indexes.md](references/skill-indexes.md) for community indexes, and [search-recipes.md](references/search-recipes.md) for GitHub queries.

```bash
python test/test_skill.py
python tools/verify_catalog.py
```

The offline test checks portability and the search, selection, and trust rules. It runs on pushes. The catalog verifier checks repository liveness monthly.

## Files

```text
SKILL.md                      Skill instructions
references/vendor-skills.md   Vendor catalog
references/skill-indexes.md   Community indexes
references/search-recipes.md  GitHub queries
tools/verify_catalog.py       Repository liveness check
test/test_skill.py            Offline validation
.claude-plugin/               Plugin manifests
CONTRIBUTING.md               Catalog contribution guidance
```

For a plugin installation, remove it with `/plugin uninstall scout@claude-skill-finder`. For a plain installation, remove the `~/.claude/skills/scout` directory.

The skill does not cache searches, install third-party skills unattended, run a daemon, or provide routing among installed skills.

## License

[MIT](LICENSE). Linked repositories retain their own licenses. See [CONTRIBUTING.md](CONTRIBUTING.md) for catalog changes.

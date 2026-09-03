# Skill indexes

Other people already maintain lists of what exists. One fetch and a local grep beats
a GitHub code search on accuracy, speed and budget - an index search does not count
against the two stage 2 searches.

Verified 2026-09-03. Star counts move; the shapes below are what matters.

## Machine readable, query these first

**[alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills)** - 25k stars, MIT, a real Claude Code marketplace: 99 plugin bundles, several hundred skills, each entry carrying `description`, `keywords` and `category`.

```bash
curl -sL https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/.claude-plugin/marketplace.json \
  | python -c "import json,sys; q='stripe'; [print(p['name'],'-',p['description'][:90]) for p in json.load(sys.stdin)['plugins'] if q in json.dumps(p).lower()]"
```

**[davepoon/buildwithclaude](https://github.com/davepoon/buildwithclaude)** - 3.4k stars, MIT, same marketplace shape, 86 plugins, plus an `mcp-servers.json` when the gap is a server rather than a skill. Query it the same way.

**[hesreallyhim/awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code)** - 53k stars, a CSV with id, category, link, author, description and a staleness flag. Broader than skills: commands, hooks, whole workflows.

```bash
curl -sL https://raw.githubusercontent.com/hesreallyhim/awesome-claude-code/main/THE_RESOURCES_TABLE_NEW.csv | grep -i "<term>"
```

## Readable, but only by eye

**[ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills)** - 74k stars, the largest list, one directory per skill. No index file, so list the directories:

```bash
gh api repos/ComposioHQ/awesome-claude-skills/contents --jq '.[]|select(.type=="dir").name'
```

**No license file.** Read it as a pointer, never copy files out of it. An unlicensed
repo is not usable material no matter how many stars it has.

## Using a hit

A marketplace entry installs natively, which is better than cloning by hand:

```
/plugin marketplace add <owner>/<repo>
/plugin install <name>@<marketplace>
```

Same rule as everywhere else: propose it, let the user run it. An index tells you a
skill exists; it does not tell you the skill is safe.

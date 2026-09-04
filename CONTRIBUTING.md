# Contributing

The skill is one markdown file. Most useful contributions are one line long.

## Adding a row to the vendor catalog

`references/vendor-skills.md` lists skills published by the people who own the stack.
A row belongs there if the vendor themselves maintains it. Community skills do not go
in this table; the live search already finds those.

Before opening a PR:

```bash
python tools/verify_catalog.py
```

It refuses rows that are gone, archived, or a year without a commit.

## Adding a skill index

`references/skill-indexes.md` holds lists other people maintain. A machine-readable
index (marketplace manifest, CSV, JSON) is worth far more than another README table,
so include the exact query one-liner with the entry. Note the license: an unlicensed
list is usable as a pointer, never as a source of files.

## Changing the skill itself

`SKILL.md` is the whole product. Three things are load-bearing and the test suite
fails without them:

- the three-search budget
- the quality gate (stars or vendor-published, recent commit, license)
- the trust boundary, including the one confirmation before installing anything

If a change makes the skill do more, it probably belongs in a different skill.

```bash
python test/test_skill.py
```

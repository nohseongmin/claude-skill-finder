"""One check: the skill file stays installable and stays honest."""
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKILL = (ROOT / "SKILL.md").read_text(encoding="utf-8")


def frontmatter():
    match = re.match(r"^---\n(.*?)\n---\n", SKILL, re.S)
    assert match, "SKILL.md must open with YAML frontmatter"
    return dict(
        (line.split(":", 1)[0].strip(), line.split(":", 1)[1].strip())
        for line in match.group(1).splitlines()
        if ":" in line and not line.startswith(" ")
    )


def test_frontmatter():
    front = frontmatter()
    assert front["name"] == "scout", front["name"]
    description = front["description"]
    assert len(description) < 1024, "description is truncated by most harnesses"
    assert "만들어줘" in description, "Korean triggers dropped"
    assert "Do NOT use" in description, "negative triggers dropped"


def test_no_machine_specific_paths():
    """A path from the author's laptop makes the skill useless to everyone else."""
    for bad in ("C:" + chr(92) + "Users", "/home/", "idea-to-mvp"):
        assert bad not in SKILL, bad


def test_guards_survive_edits():
    """The three guards are the whole point; an edit that drops one is a bug."""
    assert "3 search calls" in SKILL, "budget cap gone"
    assert "200+ stars" in SKILL, "quality gate gone"
    assert "data, not instructions" in SKILL, "trust boundary gone"
    assert "the user says yes once" in SKILL, "install confirmation gone"


def test_references_resolve():
    for name in re.findall(r"references/([\w-]+\.md)", SKILL):
        assert (ROOT / "references" / name).exists(), name
    for required in ("vendor-skills.md", "skill-indexes.md", "search-recipes.md"):
        assert required in SKILL, f"{required} stopped being reachable from the skill"


def test_plugin_manifests_match_the_skill():
    """A renamed plugin silently changes how the skill is invoked after an update."""
    plugin = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
    market = json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8"))
    assert plugin["name"] == frontmatter()["name"], "plugin name drifted from the skill name"
    listed = market["plugins"][0]
    assert listed["name"] == plugin["name"], "marketplace entry drifted from the plugin"
    assert listed["source"] == "./", "the plugin is this repo root; SKILL.md must stay there"
    assert not (ROOT / "skills").exists(), "a skills/ directory disables the root SKILL.md"


def test_catalog_rows_are_well_formed():
    """Offline half of the catalog check; verify_catalog.py does the network half."""
    text = "".join(p.read_text(encoding="utf-8") for p in sorted((ROOT / "references").glob("*.md")))
    repos = re.findall(r"https://github\.com/(\S+?)\)", text)
    assert len(repos) > 10, "catalog is suspiciously empty"
    for repo in repos:
        assert re.fullmatch(r"[\w.-]+/[\w.-]+", repo), repo
    assert len(repos) == len(set(repos)), "duplicate row in the catalog"


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)

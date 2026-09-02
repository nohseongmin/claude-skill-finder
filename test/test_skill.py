"""One check: the skill file stays installable and stays honest."""
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


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)

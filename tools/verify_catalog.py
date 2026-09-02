"""Ping every repo in the vendor catalog. A catalog of dead links is worse than none.

    python tools/verify_catalog.py

Exits non-zero if a row is gone, archived, or has not been touched in a year.
Unauthenticated GitHub API: 60 calls/hour, and the catalog is far smaller than that.
"""
import datetime
import json
import pathlib
import re
import sys
import urllib.error
import urllib.request

CATALOG = pathlib.Path(__file__).resolve().parent.parent / "references" / "vendor-skills.md"
STALE_AFTER_DAYS = 365


def repos():
    text = CATALOG.read_text(encoding="utf-8")
    found = re.findall(r"https://github\.com/([\w.-]+/[\w.-]+)", text)
    return sorted(set(found))


def fetch(repo):
    request = urllib.request.Request(
        f"https://api.github.com/repos/{repo}",
        headers={"Accept": "application/vnd.github+json", "User-Agent": "claude-skill-finder"},
    )
    with urllib.request.urlopen(request, timeout=15) as response:
        return json.load(response)


def main():
    today = datetime.date.today()
    problems = []
    for repo in repos():
        try:
            data = fetch(repo)
        except urllib.error.HTTPError as error:
            problems.append(f"{repo}: HTTP {error.code}")
            print(f"DEAD  {repo} (HTTP {error.code})")
            continue
        pushed = datetime.date.fromisoformat(data["pushed_at"][:10])
        age = (today - pushed).days
        note = f"{data['stargazers_count']} stars, pushed {pushed}"
        if data.get("archived"):
            problems.append(f"{repo}: archived")
            print(f"STALE {repo} ({note}, archived)")
        elif age > STALE_AFTER_DAYS:
            problems.append(f"{repo}: {age} days since last push")
            print(f"STALE {repo} ({note})")
        else:
            print(f"ok    {repo} ({note})")
    if problems:
        print(f"\n{len(problems)} row(s) need attention", file=sys.stderr)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())

"""Ping every repo this skill points at. A catalog of dead links is worse than none.

    python tools/verify_catalog.py

Exits non-zero if a row is gone, archived, has not been touched in a year, or -
for the vendor catalog, whose gate requires one - has no license.
Unauthenticated GitHub API allows 60 calls/hour, which covers the catalog. Set
GITHUB_TOKEN to raise that when a shared IP has already spent the quota.
"""
import datetime
import json
import os
import pathlib
import re
import sys
import urllib.error
import urllib.request

REFERENCES = pathlib.Path(__file__).resolve().parent.parent / "references"
VENDOR_CATALOG = REFERENCES / "vendor-skills.md"
STALE_AFTER_DAYS = 365


def repos():
    """(repo, needs_license) pairs. Only the vendor catalog's gate requires a license -
    skill-indexes.md documents pointer-only entries that are read, never copied from."""
    found = {}
    for path in sorted(REFERENCES.glob("*.md")):
        for repo in re.findall(r"https://github\.com/([\w.-]+/[\w.-]+)", path.read_text(encoding="utf-8")):
            found[repo] = found.get(repo, False) or path == VENDOR_CATALOG
    return sorted(found.items())


def fetch(repo):
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "claude-skill-finder"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(f"https://api.github.com/repos/{repo}", headers=headers)
    with urllib.request.urlopen(request, timeout=15) as response:
        return json.load(response)


def main():
    today = datetime.date.today()
    problems = []
    for repo, needs_license in repos():
        try:
            data = fetch(repo)
        except urllib.error.HTTPError as error:
            if error.code in (403, 429):
                # Rate limited, not dead. Reporting these as dead rows would be a lie.
                print(
                    f"gave up at {repo}: GitHub rate limit. Set GITHUB_TOKEN and rerun.",
                    file=sys.stderr,
                )
                return 2
            problems.append(f"{repo}: HTTP {error.code}")
            print(f"DEAD  {repo} (HTTP {error.code})")
            continue
        except urllib.error.URLError as error:
            # DNS failure, timeout, connection refused - a network hiccup on one repo,
            # not proof it's dead. Report it and keep checking the rest of the catalog.
            problems.append(f"{repo}: {error.reason}")
            print(f"ERROR {repo} ({error.reason})")
            continue
        except TimeoutError:
            problems.append(f"{repo}: timed out")
            print(f"ERROR {repo} (timed out)")
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
        elif needs_license and not data.get("license"):
            problems.append(f"{repo}: no license file")
            print(f"UNLIC {repo} ({note}, no license)")
        else:
            print(f"ok    {repo} ({note})")
    if problems:
        print(f"\n{len(problems)} row(s) need attention", file=sys.stderr)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())

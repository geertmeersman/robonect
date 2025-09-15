"""Script to calculate the next beta version."""

import os
import sys

import requests

# Get repository owner and repository name from the environment variable
repository = os.environ["GITHUB_REPOSITORY"]
owner, repo = repository.split("/")

# print(f"Repository: {repo}")
# print(f"Owner: {owner}")

# Get the latest release information
response = requests.get(
    f"https://api.github.com/repos/{owner}/{repo}/releases/latest",
    timeout=10,
)
if response.status_code == 404:
    # No releases yet; start from v0.0.0
    latest_version = "v0.0.0"
else:
    response.raise_for_status()
    latest_release = response.json()
    latest_version = latest_release["tag_name"]

ref = os.environ["GITHUB_REF"]

# Get the commit count since the latest release
response = requests.get(
    f"https://api.github.com/repos/{owner}/{repo}/compare/{latest_version}...{ref}",
    timeout=10,
)
compare_info = response.json()
commit_count = compare_info["total_commits"]


def is_dependabot_commit(commit):
    """Check if a commit was authored by Dependabot."""
    author = commit.get("author") or {}
    commit_meta = commit.get("commit") or {}
    commit_author = commit_meta.get("author") or {}
    commit_committer = commit_meta.get("committer") or {}
    fields = [
        author.get("login", ""),
        commit_author.get("name", ""),
        commit_author.get("email", ""),
        commit_committer.get("name", ""),
        commit_committer.get("email", ""),
    ]
    text = " ".join(x for x in fields if x)
    return "dependabot" in text.lower()


def get_semver_level(commit_messages, commits):
    """Extract SemVer level, but treat Dependabot commits as patch."""
    major_keywords = ["breaking change", "major"]
    minor_keywords = ["feat", "minor"]

    # If all commits are from dependabot, just return patch
    if all(is_dependabot_commit(c) for c in commits):
        return "patch"

    for i, message in enumerate(commit_messages):
        if not is_dependabot_commit(commits[i]):
            ml = message.lower()
            if any(keyword in ml for keyword in major_keywords):
                return "major"

    for i, message in enumerate(commit_messages):
        if not is_dependabot_commit(commits[i]):
            ml = message.lower()
            if any(keyword in ml for keyword in minor_keywords):
                return "minor"

    return "patch"


# Determine version components based on commit messages
commit_messages = [c["commit"]["message"] for c in compare_info["commits"]]
bump = get_semver_level(commit_messages, compare_info["commits"])

base = latest_version.lstrip("v").split("-", 1)[0]
major, minor, patch = map(int, base.split("."))

if bump == "major":
    major += 1
    minor = 0
    patch = 0
elif bump == "minor":
    minor += 1
    patch = 0
else:
    patch += 1

# Create the next version
next_version = f"v{major}.{minor}.{patch}"

# Check if there are any commits since the latest release
if commit_count > 0:
    next_version += f"-beta.{commit_count}"

print(next_version)
sys.exit(0)

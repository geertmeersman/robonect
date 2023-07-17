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
    f"https://api.github.com/repos/{owner}/{repo}/releases/latest", timeout=10
)
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


def get_semver_level(commit_messages):
    """Extract SemVer level."""
    major_keywords = ["breaking change", "major"]
    minor_keywords = ["feat", "minor"]
    for message in commit_messages:
        if any(keyword in message for keyword in major_keywords):
            return "major"
    for message in commit_messages:
        if any(keyword in message for keyword in minor_keywords):
            return "minor"
    return "patch"


# Determine version components based on commit messages
commit_messages = []
for commit in compare_info["commits"]:
    commit_messages.append(commit["commit"]["message"])

bump = get_semver_level(commit_messages)

major, minor, patch = map(int, latest_version[1:].split("."))

if bump == "major":
    major += 1
elif bump == "minor":
    minor += 1
else:
    patch += 1

# Create the next version
next_version = f"v{major}.{minor}.{patch}"

# Check if there are any commits since the latest release
if commit_count > 0:
    next_version += f"-beta.{commit_count}"

print(next_version)
sys.exit(0)

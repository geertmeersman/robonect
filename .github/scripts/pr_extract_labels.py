"""Script to extract the labels for a PR."""
import os
import re
import sys


def extract_semver_types(commit_messages):
    """Extract SemVer types."""
    types = []
    for message in commit_messages:
        pattern = r"^(feat|fix|chore|docs|style|refactor|perf|test)(?:\(.+?\))?:\s(.+)$"
        match = re.match(pattern, message)
        if match and match.group(1) not in types:
            types.append(match.group(1))
    return types


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


file_path = "COMMIT_MESSAGES"
if os.path.exists(file_path):
    with open(file_path) as file:
        messages = []
        for line in file:
            messages.append(line.strip())
        semver_level = get_semver_level(messages)
        types = extract_semver_types(messages)
        types.append(semver_level)
        print(types)
        sys.exit(0)
else:
    sys.exit(f"ERROR: {file_path} does not exist")

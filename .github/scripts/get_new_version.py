"""Script to calculate the next version."""
import subprocess
import sys

from git import Repo
from git_conventional_version.api import Api
import semantic_version
import semver


def get_last_beta_tag():
    """Get the last beta tag from GIT."""
    command = ["git", "describe", "--tags", "--abbrev=0", "--match", "*beta*"]
    output = subprocess.check_output(command).decode().strip()
    return output


def get_version_without_prerelease(version):
    """Get SemVer version without prerelease suffix."""
    semver = semantic_version.Version(version)
    return str(semver.major) + "." + str(semver.minor) + "." + str(semver.patch)


api = Api(repo=Repo(search_parent_directories=True))
last_beta_tag = get_last_beta_tag()
new_tag = api.get_new_version(type="final")
last_beta_tag_without_prerelease = get_version_without_prerelease(last_beta_tag)
ver = semver.Version.parse(last_beta_tag)
if new_tag != last_beta_tag_without_prerelease:
    new_version = f"{new_tag}-beta.1"
else:
    new_version = ver.bump_prerelease()
print(new_version)
sys.exit(0)

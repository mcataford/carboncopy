from pathlib import Path
import subprocess
import re

import requests

from .constants import FETCH_URL_PATTERN, GIT_EXT_PATTERN, GIT_LINK_PATTERN


class NotInAGitRepositoryError(Exception):
    pass


class NoTemplateError(Exception):
    pass


def clone_template_head(url: str, destination: Path) -> None:
    _run(
        "git clone {url} {location}".format(url=url, location=destination.resolve()),
        stdout=subprocess.DEVNULL,
    )


def get_local_repository_meta():
    stdout = _run("git remote show origin")
    stdout_split = stdout.decode().split("\n")

    for line in stdout_split:
        if re.search(FETCH_URL_PATTERN, line):
            match = re.search(GIT_LINK_PATTERN, line)
            org, repo = match.group(0).split("/")

            return org, re.sub(GIT_EXT_PATTERN, "", repo)

    return None, None


def get_repo_metadata(owner, repo):
    headers = {"Accept": "application/vnd.github.baptiste-preview+json"}
    r = requests.get(
        "https://api.github.com/repos/{owner}/{repo}".format(owner=owner, repo=repo),
        headers=headers,
    )
    repo_data = r.json()

    template_repo = repo_data.get("template_repository")
    return template_repo


def _run(command, stdout=subprocess.PIPE):
    return subprocess.run(command.split(" "), stdout=stdout, stderr=stdout).stdout

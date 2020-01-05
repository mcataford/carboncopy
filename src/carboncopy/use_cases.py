import subprocess
import re
from pathlib import Path
import requests
import shutil
import os
import json
import uuid

from .config_defaults import CONFIG_DEFAULTS
from .constants import RCFILE_PATH
from .fs_utils import squash, clean_temp_files, get_template_file_paths
from .git_utils import get_local_repository_meta, get_repo_metadata, clone_template_head


def get_local_config(root_path=Path(".")):
    config_path = root_path.joinpath(RCFILE_PATH)
    try:
        with open(config_path, "r") as config_file:
            loaded_config = json.load(config_file)

        merged_config = CONFIG_DEFAULTS.copy()

        for key in loaded_config:
            merged_config[key] = loaded_config.get(key)

        return merged_config

    except FileNotFoundError:
        print("No config file found in current directory! Proceeding with defaults.")
        return CONFIG_DEFAULTS
    except Exception as e:
        print(e.__class__)
        print(e)


class UseCases:
    def __init__(self, config):
        self.config = config
        self.template_repo = None
        self.org = None
        self.repo = None

    def fetch_template_repository_details(self):
        org, repo = get_local_repository_meta()
        self.template_repo = get_repo_metadata(org, repo)
        self.org = org
        self.repo = repo

    def clone_template_repository(self):
        clone_template_head(
            self.template_repo.get("clone_url"), Path(self.config.get("temp_directory"))
        )

    def stage_changes(self):
        path = Path(self.config.get("temp_directory"))
        template_files = get_template_file_paths(path)

        staged = [path.get("destination") for path in template_files]

        print(
            "Overwriting the following from {org}/{repo}".format(
                org=self.org, repo=self.repo
            )
        )

        for staged_file in staged:
            print(str(staged_file))

        return template_files

    def apply_changes(self, paths):
        for path in paths:
            squash(path.get("template"), path.get("destination"))

    def clean_up(self):
        clean_temp_files(Path(self.config.get("temp_directory")))

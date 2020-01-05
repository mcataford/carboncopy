import subprocess
import re
from pathlib import Path
import requests
import shutil
import os
import json
import uuid
from typing import List, Dict, Any

from .config_defaults import CONFIG_DEFAULTS
from .constants import RCFILE_PATH, FORCED_IGNORE_PATTERNS
from .fs_utils import Transform, squash, clean_temp_files, get_template_transforms
from .git_utils import (
    NoTemplateError,
    NotInAGitRepositoryError,
    get_local_repository_meta,
    get_repo_metadata,
    clone_template_head,
)
from .cli_utils import prompt_staging_files_confirmation
from .print_utils import pretty_print


def get_local_config(root_path: Path = Path(".")) -> Dict[str, Any]:
    config_path = root_path.joinpath(RCFILE_PATH)
    try:
        with open(config_path, "r") as config_file:
            loaded_config = json.load(config_file)

        merged_config = CONFIG_DEFAULTS.copy()

        for key in loaded_config:
            merged_config[key] = loaded_config.get(key)

        return merged_config

    except FileNotFoundError:
        pretty_print(
            "No config file found in current directory! Proceeding with defaults."
        )
    except ValueError:
        pretty_print("Invalid RC file!")

    return CONFIG_DEFAULTS


class UseCases:
    def __init__(self, config: Dict[str, Any]) -> None:
        self.config = config
        self.template_repo: Dict[str, str] = {}
        self.org = None
        self.repo = None

    def fetch_template_repository_details(self) -> None:
        org, repo = get_local_repository_meta()
        template_repo_data = get_repo_metadata(org, repo)

        if not (org and repo):
            raise NotInAGitRepositoryError()

        if not template_repo_data:
            raise NoTemplateError()

        self.org = org
        self.repo = repo
        self.template_repo = template_repo_data

    def clone_template_repository(self) -> None:
        clone_template_head(
            self.template_repo["clone_url"], Path(self.config["temp_directory"])
        )

    def stage_changes(self) -> List[Transform]:
        path = Path(self.config["temp_directory"])
        available_transforms = get_template_transforms(path)

        def can_stage(path_str: str) -> bool:
            return not re.match(FORCED_IGNORE_PATTERNS, path_str) and all(
                [re.match(patt, path_str) for patt in self.config["ignore"]]
            )

        allowed_transforms = [
            transform
            for transform in available_transforms
            if can_stage(transform.get_destination(as_str=True))
        ]

        destinations = [
            transform.get_destination(as_str=True) for transform in allowed_transforms
        ]
        chosen_files = prompt_staging_files_confirmation(
            destinations, "{}/{}".format(self.org, self.repo)
        )
        chosen_transforms = [
            transform
            for transform in allowed_transforms
            if transform.get_destination(as_str=True)
            in chosen_files["suggested_changes"]
        ]

        return chosen_transforms

    def apply_changes(self, paths: List[Transform]) -> None:
        for path in paths:
            squash(path)

    def clean_up(self) -> None:
        clean_temp_files(Path(self.config["temp_directory"]))

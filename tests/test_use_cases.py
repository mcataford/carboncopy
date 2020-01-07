import json

import pytest

from src.carboncopy.use_cases import get_local_config, UseCases
from src.carboncopy.constants import RCFILE_PATH
from src.carboncopy.config_defaults import CONFIG_DEFAULTS
from src.carboncopy.git_utils import NotInAGitRepositoryError, NoTemplateError

from .test_utils import assert_captured_output_matches_snapshot

def test_get_local_config_returns_default_config_if_no_config_file_present(tmp_path, snapshot, capsys):
    assert len(list(tmp_path.iterdir())) == 0

    fetched_config = get_local_config(tmp_path)

    assert fetched_config == CONFIG_DEFAULTS

    assert_captured_output_matches_snapshot(capsys, snapshot)

def test_get_local_config_returns_default_config_if_invalid_config_file_present(tmp_path, snapshot, capsys):
    invalid_config_file = tmp_path / RCFILE_PATH

    invalid_config_file.write_text('')

    assert len(list(tmp_path.iterdir())) == 1

    fetched_config = get_local_config(tmp_path)

    assert fetched_config == CONFIG_DEFAULTS

    assert_captured_output_matches_snapshot(capsys, snapshot)

def test_get_local_config_merges_rcfile_with_default_config(tmp_path, snapshot, capsys):
    valid_config = { "ignore": ["some-file.md"] }

    config_file = tmp_path / RCFILE_PATH
    config_file.write_text(json.dumps(valid_config))

    assert len(list(tmp_path.iterdir())) == 1

    fetched_config = get_local_config(tmp_path)

    expected_config = {**CONFIG_DEFAULTS, **valid_config}

    assert fetched_config == expected_config

    assert_captured_output_matches_snapshot(capsys, snapshot)

def test_fetch_template_repository_details_throws_NotInGitRepositoryError_if_not_in_repo():
    pass

def test_fetch_template_repository_details_throws_NoTemplateError_if_no_template_repo():
    pass

def test_stage_changes_ignores_all_forced_ignore_patterns():
    pass

def test_stage_changes_ignores_all_configured_ignore_patterns():
    pass

def test_apply_changes_squashes_all_files():
    pass

def test_clean_up_cleans_up_temporary_directory_files():
    pass

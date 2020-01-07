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

def test_fetch_template_repository_details_throws_NotInGitRepositoryError_if_not_in_repo(capsys, snapshot, monkeypatch):
    # This simulates the repository meta not finding a repository.
    def _mock():
        return (None, None)

    monkeypatch.setattr("src.carboncopy.use_cases.get_local_repository_meta", _mock)
    
    use_cases = UseCases(config=CONFIG_DEFAULTS)
    
    with pytest.raises(NotInAGitRepositoryError):
        use_cases.fetch_template_repository_details()
    
    assert_captured_output_matches_snapshot(capsys, snapshot)

def test_fetch_template_repository_details_throws_NoTemplateError_if_no_template_repo(capsys, monkeypatch, snapshot):
    # This simulates the repository data not containing a template repo reference
    def _mock(a, b):
        return None

    def _mock_local_meta():
        return 'org', 'repo'

    monkeypatch.setattr('src.carboncopy.use_cases.get_local_repository_meta', _mock_local_meta)
    monkeypatch.setattr("src.carboncopy.use_cases.get_repo_metadata", _mock)

    use_cases = UseCases(config=CONFIG_DEFAULTS, non_interactive=True)

    with pytest.raises(NoTemplateError):
        use_cases.fetch_template_repository_details()

    assert_captured_output_matches_snapshot(capsys, snapshot)

def test_stage_changes_ignores_all_forced_ignore_patterns(capsys, tmp_path, snapshot):
    # Set up a mock template_directory
    temp_dir = tmp_path / CONFIG_DEFAULTS["temp_directory"]
    temp_dir.mkdir()
    # .git is a notoriously ignored directory
    forced_ignored_dir = temp_dir / ".git"
    forced_ignored_dir.mkdir()
    some_file = forced_ignored_dir / "some_file.txt"
    some_file.write_text("smol file")

    use_cases = UseCases(config=CONFIG_DEFAULTS, non_interactive=True, root_path=tmp_path)

    staged = use_cases.stage_changes()
    assert len(staged) == 0

    assert_captured_output_matches_snapshot(capsys, snapshot)


def test_stage_changes_ignores_all_configured_ignore_patterns(capsys, tmp_path, snapshot):
    # Set up a mock template_directory
    temp_dir = tmp_path / CONFIG_DEFAULTS["temp_directory"]
    temp_dir.mkdir()
    forced_ignored_dir = temp_dir / "ignore_folder"
    forced_ignored_dir.mkdir()
    some_file = forced_ignored_dir / "some_file.txt"
    some_file.write_text("smol file")

    config = { "ignore": ["ignore_folder"] }
    merged_config = {**CONFIG_DEFAULTS, **config}
    use_cases = UseCases(config=merged_config , non_interactive=True, root_path=tmp_path)

    staged = use_cases.stage_changes()
    assert len(staged) == 0   

    assert_captured_output_matches_snapshot(capsys, snapshot)

def test_stage_changes_creates_transforms_for_all_valid_changes(capsys, snapshot, tmp_path):
    # Set up a mock template_directory
    temp_dir = tmp_path / CONFIG_DEFAULTS["temp_directory"]
    temp_dir.mkdir()
    forced_ignored_dir = temp_dir / "coolio"
    forced_ignored_dir.mkdir()
    some_file = forced_ignored_dir / "some_file.txt"
    some_file.write_text("smol file")

    use_cases = UseCases(config=CONFIG_DEFAULTS , non_interactive=True, root_path=tmp_path)

    staged = use_cases.stage_changes()
    assert len(staged) == 1   

    assert_captured_output_matches_snapshot(capsys, snapshot)



def test_apply_changes_squashes_all_files(tmp_path, capsys, snapshot):
    temp_dir = tmp_path / CONFIG_DEFAULTS["temp_directory"]
    temp_dir.mkdir()
    cloned_repo = temp_dir / "attack_of_the_clone_repos"
    cloned_repo.mkdir()
    some_file = cloned_repo / "some_file.txt"
    some_file.write_text("smol file")

    use_cases = UseCases(config=CONFIG_DEFAULTS, non_interactive=True, root_path=tmp_path)

    staged = use_cases.stage_changes()
    use_cases.apply_changes(staged)

    resulting_files = list(tmp_path.iterdir())
    
    resulting_copy = tmp_path / "attack_of_the_clone_repos"
    assert len(list(resulting_copy.iterdir())) == 1
    
    copied_file = resulting_copy / "some_file.txt"

    assert copied_file.read_text() == "smol file"

def test_clean_up_cleans_up_temporary_directory_files(tmp_path):
    temp_dir = tmp_path / CONFIG_DEFAULTS["temp_directory"]
    temp_dir.mkdir()
    cloned_repo = temp_dir / "attack_of_the_clone_repos"
    cloned_repo.mkdir()
    some_file = cloned_repo / "some_file.txt"
    some_file.write_text("smol file")

    use_cases = UseCases(config=CONFIG_DEFAULTS, non_interactive=True, root_path=tmp_path)

    use_cases.clean_up()

    assert len(list(tmp_path.iterdir())) == 0

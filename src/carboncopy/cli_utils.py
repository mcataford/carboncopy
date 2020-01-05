import inquirer

from typing import List
from pathlib import Path


def prompt_staging_files_confirmation(
    staged: List[Path], template_repository_name: str
):
    questions = [
        inquirer.Checkbox(
            "suggested_changes",
            message="The following files can be pulled from {}. Select the ones to be merged in:".format(
                template_repository_name
            ),
            choices=[str(staged_file) for staged_file in staged],
        )
    ]

    return inquirer.prompt(questions)

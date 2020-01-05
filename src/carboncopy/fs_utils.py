import shutil
from pathlib import Path
from typing import Union, List, Dict, Any
import os


def clean_temp_files(path: Path) -> None:
    if path:
        shutil.rmtree(path, True)


def get_template_file_paths(path: Path) -> List[Dict[str, Path]]:
    file_paths = []

    stack = [path]

    while stack:
        current_path = stack.pop()

        if not current_path.is_dir():
            file_paths.append(current_path)
            continue

        for child in current_path.iterdir():
            child_path = Path(child)
            stack.append(child_path)

    return [
        {"template": filename, "destination": filename.relative_to(path)}
        for filename in file_paths
    ]


def squash(source: Path, destination: Path) -> None:
    if not destination.parent.exists():
        os.makedirs(destination.parent)

    try:
        shutil.copy(source, destination)
        print(
            "Copied {source} -> {destination}".format(
                source=source, destination=destination
            )
        )
    except IsADirectoryError:
        print(
            "Failed to copy {source} -> {destination}".format(
                source=source, destination=destination
            )
        )
    except Exception as e:
        print(e.__class__)
        print(e)

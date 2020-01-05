import shutil
from pathlib import Path
from typing import Union, List, Dict, Any


def clean_temp_files(path: Path) -> None:
    if path:
        shutil.rmtree(path, True)


def get_template_file_paths(path: Path) -> List[Dict[str, Path]]:
    # TODO: expand to proper nested file structure.
    return [
        {"template": Path(filename), "destination": Path(filename).relative_to(path)}
        for filename in path.iterdir()
    ]


def squash(source: Path, destination: Path) -> None:
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

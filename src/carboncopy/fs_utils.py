import shutil
from pathlib import Path
from typing import Union, List, Dict, Any
import os

from .print_utils import pretty_print


class Transform:
    def __init__(self, source: Path, destination: Path):
        self.source = source
        self.destination = destination

    def get_source(self, as_str: bool = False):
        return str(self.source) if as_str else self.source

    def get_destination(self, as_str: bool = False):
        return str(self.destination) if as_str else self.destination

    def __repr__(self):
        return "<{classname} {source} -> {destination}>".format(
            classname=self.__class__,
            source=str(self.source),
            destination=str(self.destination),
        )


def clean_temp_files(path: Path) -> None:
    if path:
        shutil.rmtree(path, True)


def get_template_transforms(path: Path) -> List[Transform]:
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
        Transform(source=filename, destination=filename.relative_to(path))
        for filename in file_paths
    ]


def squash(transform: Transform) -> None:
    destination = transform.get_destination()
    source = transform.get_source()

    if not destination.parent.exists():
        os.makedirs(destination.parent)

    try:
        shutil.copy(source, destination)
        pretty_print(
            "Copied {source} -> {destination}".format(
                source=source, destination=destination
            )
        )
    except IsADirectoryError:
        pretty_print(
            "Failed to copy {source} -> {destination}".format(
                source=source, destination=destination
            )
        )
    except Exception as e:
        pretty_print(e.__class__)
        pretty_print(e)

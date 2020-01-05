import shutil
from pathlib import Path


def clean_temp_files(path: Path):
    shutil.rmtree(path, True)


def get_template_file_paths(path):
    # TODO: expand to proper nested file structure.
    return [
        {"template": Path(filename), "destination": Path(filename).relative_to(path)}
        for filename in path.iterdir()
    ]


def squash(source, destination):
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

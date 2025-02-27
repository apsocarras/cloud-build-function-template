#!/usr/bin/env python
from __future__ import annotations

import logging
import os
import shutil

PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)


logger = logging.getLogger(__name__)


def remove_file(filepath: str) -> None:
    os.remove(os.path.join(PROJECT_DIRECTORY, filepath))


def remove_dir(filepath: str) -> None:
    shutil.rmtree(os.path.join(PROJECT_DIRECTORY, filepath))


def move_file(filepath: str, target: str) -> None:
    os.rename(
        os.path.join(PROJECT_DIRECTORY, filepath),
        os.path.join(PROJECT_DIRECTORY, target),
    )


def move_dir(src: str, target: str) -> None:
    shutil.move(
        os.path.join(PROJECT_DIRECTORY, src), os.path.join(PROJECT_DIRECTORY, target)
    )


def clean_files_and_dirs() -> None:
    """Remove unused directories and files"""
    if "{{cookiecutter.include_github_actions}}" != "y":
        remove_dir(".github")
    else:
        if "{{cookiecutter.publish_to_pypi}}" == "n":
            remove_file(os.path.join(".github", "workflows", "release_pypi.yaml"))

    if "{{cookiecutter.include_devcontainer}}" != "y":
        remove_dir(".devcontainer")

    licenses = {
        "MIT License": "LICENSE_MIT",
        "BSD License": "LICENSE_BSD",
        "ISC License": "LICENSE_ISC",
        "Apache Software License 2.0": "LICENSE_APACHE",
        "GNU General Public License v3": "LICENSE_GPL",
    }
    chosen_license = "{{cookiecutter.open_source_license}}"

    for license_type, license_file_name in licenses.items():
        if license_type != chosen_license:
            remove_file(license_file_name)
        else:
            move_file(license_file_name, "LICENSE")


if __name__ == "__main__":
    clean_files_and_dirs()

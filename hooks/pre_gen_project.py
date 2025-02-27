from __future__ import annotations

import json
import logging
import os
import re
import sys
from pathlib import Path

logger = logging.getLogger(__name__)

PROJECT_DIRECTORY = Path(os.path.realpath(os.path.curdir))
COOKIECUTTER_JSON_INPUTS = PROJECT_DIRECTORY / "cookiecutter.json"
BAKED_DIR = PROJECT_DIRECTORY / "{{cookiecutter.project_name}}"
ENV_OUT_DIR = BAKED_DIR / "_local"
ENV_PATH = ENV_OUT_DIR / ".env"


def validate_project_names() -> None:
    PROJECT_NAME_REGEX = r"^[-a-zA-Z][-a-zA-Z0-9]+$"
    project_name = "{{cookiecutter.project_name}}"
    if not re.match(PROJECT_NAME_REGEX, project_name):
        logger.error(
            f"ERROR: The project name {project_name} is not a valid Python module name. Please do not use a _ and use - instead"
        )
        # Exit to cancel project
        sys.exit(1)

    PROJECT_SLUG_REGEX = r"^[_a-zA-Z][_a-zA-Z0-9]+$"
    project_slug = "{{cookiecutter.project_slug}}"
    if not re.match(PROJECT_SLUG_REGEX, project_slug):
        logger.error(
            f"ERROR: The project slug {project_slug} is not a valid Python module name. Please do not use a - and use _ instead"
        )
        # Exit to cancel project
        sys.exit(1)


def validate_file_paths() -> None:
    if not COOKIECUTTER_JSON_INPUTS.is_file():
        logger.error(
            f"ERROR: cookiecutter.json not found in project directory {os.listdir(PROJECT_DIRECTORY)}"
        )
        sys.exit(1)

    if not BAKED_DIR.is_dir():
        logger.error(
            "ERROR: {{cookiecutter.project_name}}"
            + f" not found in project directory {os.listdir(PROJECT_DIRECTORY)}"
        )
        sys.exit(1)


def make_env_file() -> None:
    """Generate .env file in baked package files based on cookiecutter.json"""

    with open(COOKIECUTTER_JSON_INPUTS, mode="r") as file:
        input_data: dict[str, str] = json.load(file)

    with open(ENV_PATH, "w") as file:
        for k in input_data.keys():
            line_str = k.upper().strip() + " = " + "{{cookiecutter." + k + "}}"
            _ = file.write(line_str)
            _ = file.write("\n")


if __name__ == "__main__":
    validate_project_names()
    validate_file_paths()
    make_env_file()

from __future__ import annotations

import json
import logging
import re
import sys

logger = logging.getLogger(__name__)


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


if __name__ == "__main__":
    validate_project_names()


def make_env_file() -> None:
    """Generate .env file in baked package files based on cookiecutter.json"""

    with open(COOKIECUTTER_JSON_INPUTS, mode="r") as file:
        input_data: dict[str, str] = json.load(file)

    with open(ENV_PATH, "w") as file:
        for k in input_data.keys():
            line_str = (
                k.upper().strip()
                + " = "
                + "{%raw%}{{{%endraw%}"
                + "cookiecutter."
                + k.strip()
                + "{%raw%}}}{%endraw%}"
            )
            logger.debug(line_str)
            _ = file.write(line_str)
            _ = file.write("\n")

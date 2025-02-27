import json
import logging
from pathlib import Path

import click

PROJECT_ROOT = Path(__file__).parents[1]
COOKIE_CUTTER_PROJECT_FOLDER = PROJECT_ROOT / "{{cookiecutter.project_name}}"
# ^^ This is the literal "{%raw%}{{cookiecutter.project_name}}{%endraw$}" directory in the base template repo

logger = logging.getLogger(__name__)


@click.command()
@click.argument("cookiecutter_path", default=PROJECT_ROOT / "cookiecutter.json")
@click.argument("env_path", default=COOKIE_CUTTER_PROJECT_FOLDER / "_local" / ".env")
def main(cookiecutter_path: str | Path, env_path: str | Path) -> None:
    """Generate .env file in baked package files based on cookiecutter.json"""

    with open(cookiecutter_path, mode="r") as file:
        input_data: dict[str, str] = json.load(file)

    with open(env_path, "w") as file:
        for k in input_data.keys():
            line_str = k.upper().strip() + " = " + "{{cookiecutter." + k.strip() + "}}"
            logger.debug(line_str)
            _ = file.write(line_str)
            _ = file.write("\n")


if __name__ == "__main__":
    main()

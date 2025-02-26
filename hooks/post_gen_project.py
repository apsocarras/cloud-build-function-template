#!/usr/bin/env python
from __future__ import annotations

import json
import logging
import os
import shutil
from types import MappingProxyType

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


def get_user_input_map() -> MappingProxyType[str, str]:
    user_inputs: MappingProxyType[str, str] = MappingProxyType(
        {
            "author": "{{cookiecutter.author}}",
            "email": "{{cookiecutter.email}}",
            "author_github_handle": "{{cookiecutter.author_github_handle}}",
            "github_pat": "{{cookiecutter.github_pat}}",
            "github_cloud_build_app_installation_id": "{{cookiecutter.github_cloud_build_app_installation_id}}",
            "project_name": "{{cookiecutter.project_name}}",
            "project_slug": "{{cookiecutter.project_slug}}",
            "project_description": "{{cookiecutter.project_description}}",
            "min_python_version": "{{cookiecutter.min_python_version}}",
            "open_source_license": "{{cookiecutter.open_source_license}}",
            "publish_to_pypi": "{{cookiecutter.publish_to_pypi}}",
            "include_devcontainer": "{{cookiecutter.include_devcontainer}}",
            "include_github_actions": "{{cookiecutter.include_github_actions}}",
            "google_application_credentials": "{{cookiecutter.google_application_credentials}}",
            "gcp_project_id": "{{cookiecutter.gcp_project_id}}",
            "gcp_region_id": "{{cookiecutter.gcp_region_id}}",
            "gcp_artifact_registry_repo_name": "{{cookiecutter.gcp_artifact_registry_repo_name}}",
            "docker_image_name": "{{cookiecutter.docker_image_name}}",
            "gcp_log_bucket_name": "{{cookiecutter.gcp_log_bucket_name}}",
            "gcp_trigger_name": "{{cookiecutter.gcp_trigger_name}}",
            "trigger_branch_pattern": "{{cookiecutter.trigger_branch_pattern}}",
            "print_user_inputs_on_build": "{{cookiecutter.print_user_inputs_on_build}}",
        }
    )
    return user_inputs


if __name__ == "__main__":
    clean_files_and_dirs()
    user_inputs = get_user_input_map()
    if user_inputs["print_user_inputs_on_build"] == "y":
        print(json.dumps(dict(user_inputs), indent=4))

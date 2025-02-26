from __future__ import annotations

import logging
import os
import shlex
import subprocess
from typing import LiteralString

import logging_config
import pytest

logger = logging.getLogger(__name__)

from dotenv import load_dotenv

from tests.utils import is_valid_yaml, run_within_dir

load_dotenv()
assert os.environ.get("GITHUB_PAT", None)
assert os.environ.get("GITHUB_CLOUD_BUILD_INSTALLATION_ID", None)


@pytest.fixture
def gh_pat() -> str:
    return os.environ.get("GITHUB_PAT")


@pytest.fixture
def github_cloud_build_app_installation_id() -> str:
    return os.environ.get("GITHUB_CLOUD_BUILD_INSTALLATION_ID")


def test_bake_project(cookies):
    result = cookies.bake(extra_context={"project_name": "my-project"})

    assert result.exit_code == 0
    assert result.exception is None
    assert result.project_path.name == "my-project"
    assert result.project_path.is_dir()


def test_using_pytest(
    cookies, tmp_path, gh_pat, github_cloud_build_app_installation_id
) -> None:
    TEST_PROJECT_NAME = "example-cloud-build-function"
    TEST_PROJECT_SLUG = TEST_PROJECT_NAME.replace("-", "_")
    TEST_PROJECT_TEST_FOLDER: LiteralString = f"test_{TEST_PROJECT_SLUG}"

    def make_test_folder_path(*args: str) -> str:
        return os.path.join(TEST_PROJECT_TEST_FOLDER, *args)

    gcp_functions_test_file = make_test_folder_path("cloud_infra", "gcp_test.py")
    main_test_file = make_test_folder_path("main_test.py")
    smoke_test_file = make_test_folder_path("smoke_test.py")

    def make_test_command(
        test_file_name: str, other_args: str | None = None
    ) -> list[str]:
        return shlex.split(f"uv run pytest tests/{test_file_name}" + (other_args or ""))

    with run_within_dir(tmp_path):
        result = cookies.bake(
            extra_context={
                "publish_to_pypi": "n",
                "github_pat": gh_pat,
                "project_name": TEST_PROJECT_NAME,
                "github_cloud_build_app_installation_id": os.environ.get(
                    "GITHUB_CLOUD_BUILD_INSTALLATION_ID"
                ),
            }
        )

        # Assert that project was created.
        assert result.exit_code == 0
        assert result.exception is None
        assert result.project_path.name == TEST_PROJECT_NAME
        assert result.project_path.is_dir()
        assert is_valid_yaml(
            result.project_path / ".github" / "workflows" / "ci_test.yaml"
        )

        # Setup mock version number for package w/ SCM
        # Install the uv environment and run the tests.
        os.environ[
            f"SETUPTOOLS_SCM_PRETEND_VERSION_FOR_{TEST_PROJECT_SLUG.upper()}"
        ] = "1.0.0"
        with run_within_dir(str(result.project_path)):
            ## Setup git
            # assert subprocess.check_call(shlex.split("git init")) == 0
            # assert subprocess.check_call(shlex.split("git add .")) == 0
            # assert (
            #     subprocess.check_call(shlex.split('git commit -m "Initial commit"'))
            #     == 0
            # )
            # Setup package env
            assert subprocess.check_call(shlex.split("uv sync")) == 0
            # Run tests individually
            assert (
                subprocess.check_call(make_test_command(gcp_functions_test_file)) == 0
            )
            assert subprocess.check_call(make_test_command(main_test_file)) == 0
            assert (
                subprocess.check_call(
                    make_test_command(
                        smoke_test_file,
                    )
                )
                == 0
            )


def test_devcontainer(cookies, tmp_path):
    """Test that the devcontainer files are created when devcontainer=y"""
    with run_within_dir(tmp_path):
        result = cookies.bake(extra_context={"include_devcontainer": "y"})
        assert result.exit_code == 0
        assert os.path.isfile(f"{result.project_path}/.devcontainer/devcontainer.json")
        assert os.path.isfile(
            f"{result.project_path}/.devcontainer/postCreateCommand.sh"
        )


def test_not_devcontainer(cookies, tmp_path):
    """Test that the devcontainer files are not created when devcontainer=n"""
    with run_within_dir(tmp_path):
        result = cookies.bake(extra_context={"include_devcontainer": "n"})
        assert result.exit_code == 0
        assert not os.path.isfile(
            f"{result.project_path}/.devcontainer/devcontainer.json"
        )
        assert not os.path.isfile(
            f"{result.project_path}/.devcontainer/postCreateCommand.sh"
        )


def test_scripts_folder(cookies, tmp_path):
    """Test that the scripts/ folder was created successfully"""
    with run_within_dir(tmp_path):
        result = cookies.bake()
        assert result.exit_code == 0
        assert os.path.isdir(script_dir := os.path.join(result.project_path, "scripts"))
        logger.debug(os.listdir(script_dir))


def test_license_mit(cookies, tmp_path):
    with run_within_dir(tmp_path):
        result = cookies.bake(extra_context={"open_source_license": "MIT License"})
        assert result.exit_code == 0
        assert os.path.isfile(f"{result.project_path}/LICENSE")
        assert not os.path.isfile(f"{result.project_path}/LICENSE_BSD")
        assert not os.path.isfile(f"{result.project_path}/LICENSE_ISC")
        assert not os.path.isfile(f"{result.project_path}/LICENSE_APACHE")
        assert not os.path.isfile(f"{result.project_path}/LICENSE_GPL")
        with open(f"{result.project_path}/LICENSE", encoding="utf8") as licfile:
            content = licfile.readlines()
            assert len(content) == 21


def test_license_bsd(cookies, tmp_path):
    with run_within_dir(tmp_path):
        result = cookies.bake(extra_context={"open_source_license": "BSD License"})
        assert result.exit_code == 0
        assert os.path.isfile(f"{result.project_path}/LICENSE")
        assert not os.path.isfile(f"{result.project_path}/LICENSE_MIT")
        assert not os.path.isfile(f"{result.project_path}/LICENSE_ISC")
        assert not os.path.isfile(f"{result.project_path}/LICENSE_APACHE")
        assert not os.path.isfile(f"{result.project_path}/LICENSE_GPL")
        with open(f"{result.project_path}/LICENSE", encoding="utf8") as licfile:
            content = licfile.readlines()
            assert len(content) == 28


def test_license_isc(cookies, tmp_path):
    with run_within_dir(tmp_path):
        result = cookies.bake(extra_context={"open_source_license": "ISC License"})
        assert result.exit_code == 0
        assert os.path.isfile(f"{result.project_path}/LICENSE")
        assert not os.path.isfile(f"{result.project_path}/LICENSE_MIT")
        assert not os.path.isfile(f"{result.project_path}/LICENSE_BSD")
        assert not os.path.isfile(f"{result.project_path}/LICENSE_APACHE")
        assert not os.path.isfile(f"{result.project_path}/LICENSE_GPL")
        with open(f"{result.project_path}/LICENSE", encoding="utf8") as licfile:
            content = licfile.readlines()
            assert len(content) == 7


def test_license_apache(cookies, tmp_path):
    with run_within_dir(tmp_path):
        result = cookies.bake(
            extra_context={"open_source_license": "Apache Software License 2.0"}
        )
        assert result.exit_code == 0
        assert os.path.isfile(f"{result.project_path}/LICENSE")
        assert not os.path.isfile(f"{result.project_path}/LICENSE_MIT")
        assert not os.path.isfile(f"{result.project_path}/LICENSE_BSD")
        assert not os.path.isfile(f"{result.project_path}/LICENSE_ISC")
        assert not os.path.isfile(f"{result.project_path}/LICENSE_GPL")
        with open(f"{result.project_path}/LICENSE", encoding="utf8") as licfile:
            content = licfile.readlines()
            assert len(content) == 202


def test_license_gplv3(cookies, tmp_path):
    with run_within_dir(tmp_path):
        result = cookies.bake(
            extra_context={"open_source_license": "GNU General Public License v3"}
        )
        assert result.exit_code == 0
        assert os.path.isfile(f"{result.project_path}/LICENSE")
        assert not os.path.isfile(f"{result.project_path}/LICENSE_MIT")
        assert not os.path.isfile(f"{result.project_path}/LICENSE_BSD")
        assert not os.path.isfile(f"{result.project_path}/LICENSE_ISC")
        assert not os.path.isfile(f"{result.project_path}/LICENSE_APACHE")
        with open(f"{result.project_path}/LICENSE", encoding="utf8") as licfile:
            content = licfile.readlines()
            assert len(content) == 674


def test_license_no_license(cookies, tmp_path):
    with run_within_dir(tmp_path):
        result = cookies.bake(extra_context={"open_source_license": "Not open source"})
        assert result.exit_code == 0
        assert not os.path.isfile(f"{result.project_path}/LICENSE")
        assert not os.path.isfile(f"{result.project_path}/LICENSE_MIT")
        assert not os.path.isfile(f"{result.project_path}/LICENSE_BSD")
        assert not os.path.isfile(f"{result.project_path}/LICENSE_ISC")
        assert not os.path.isfile(f"{result.project_path}/LICENSE_APACHE")
        assert not os.path.isfile(f"{result.project_path}/LICENSE_GPL")


logging_config

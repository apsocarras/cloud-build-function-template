from __future__ import annotations

import os
import shlex
import subprocess

from tests.utils import is_valid_yaml, run_within_dir


def test_bake_project(cookies):
    result = cookies.bake(extra_context={"project_name": "my-project"})

    assert result.exit_code == 0
    assert result.exception is None
    assert result.project_path.name == "my-project"
    assert result.project_path.is_dir()


def test_using_pytest(cookies, tmp_path) -> None:
    with run_within_dir(tmp_path):
        result = cookies.bake(
            extra_context={"project_name": "my-project", "publish_to_pypi": "y"}
        )

        # Assert that project was created.
        assert result.exit_code == 0
        assert result.exception is None
        assert result.project_path.name == "my-project"
        assert result.project_path.is_dir()
        assert is_valid_yaml(
            result.project_path / ".github" / "workflows" / "release_pypi.yaml"
        )
        assert is_valid_yaml(
            result.project_path / ".github" / "workflows" / "ci_test.yaml"
        )

        # Setup mock version number for package w/ SCM
        os.environ["SETUPTOOLS_SCM_PRETEND_VERSION_FOR_MY_PROJECT"] = "1.0.0"
        # Install the uv environment and run the tests.
        with run_within_dir(str(result.project_path)):
            assert subprocess.check_call(shlex.split("uv sync")) == 0
            assert subprocess.check_call(shlex.split("uv run pytest tests/")) == 0


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

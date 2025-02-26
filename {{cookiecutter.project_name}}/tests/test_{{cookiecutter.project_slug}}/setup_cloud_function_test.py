from __future__ import annotations

from {{cookiecutter.project_slug}}.setup_cloud_function import Config
from {{cookiecutter.project_slug}}.gcp_functions import (
    assign_permissions_to_default_cloud_builder_service_account,
    assign_secret_to_service_account,
    connect_github_via_connection,
    create_artifact_registry_repository,
    create_build_trigger,
    create_github_cloud_build_connection,
    create_secret,
    make_secret_path,
)

import logging 
from math import log
import os 
from tests import logging_config
import subprocess
from tests.utils import run_within_dir
import pytest 

logger = logging.getLogger(__name__)

@pytest.fixture
def default_config() -> Config:
    config= Config()
    return config

def test_assign_permissions_to_default_cloud_builder_service_account(default_config) -> None:
    assign_permissions_to_default_cloud_builder_service_account(
        gcp_project_id=default_config.GCP_PROJECT_ID,
        gcp_project_number=default_config.gcp_project_number,
    )



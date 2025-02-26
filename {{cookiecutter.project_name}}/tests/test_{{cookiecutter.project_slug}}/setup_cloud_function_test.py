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

def test_create_secret(default_config) -> None: 
    kwargs={
        'secret_name':default_config.gcp_pat_secret_name,
        'project_id':default_config.GCP_PROJECT_ID,
        'secret_value':default_config.GITHUB_PAT,
        'service_account_email':default_config.cloud_build_service_agent_email,
    }
    create_secret(**kwargs)

def test_assign_secret_to_service_account(default_config) -> None: 
    assign_secret_to_service_account(
        service_account_email=default_config.cloud_build_service_agent_email,
        secret_path=default_config.gcp_pat_secret_path,
    )


def test_create_github_cloud_build_connection(default_config) -> None: 
    kwargs = {
        "connection_name":default_config.gcp_github_connection_name,
        "secret_path":default_config.gcp_pat_secret_path,
        "cloud_build_install_id":default_config.GITHUB_CLOUD_BUILD_INSTALLATION_ID,
        "region_id":default_config.GCP_REGION_ID,
    }
    create_github_cloud_build_connection(**kwargs)


def test_connect_github_via_connection(default_config) -> None: 
    kwargs = {
        "project_name":default_config.PROJECT_NAME,
        "github_uri":default_config.github_uri,
        "connection_name":default_config.gcp_github_connection_name,
        "region_id":default_config.GCP_REGION_ID,
     }
    connect_github_via_connection(**kwargs)
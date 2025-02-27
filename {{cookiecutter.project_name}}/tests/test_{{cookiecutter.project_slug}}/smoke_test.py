"""
Put basic tests here to ensure that your package builds correctly and maintains its basic functionality.
"""

from {{cookiecutter.project_slug}} import hello_author
from {{cookiecutter.project_slug}}.cloud_infra.config import Config
import pytest 

def test_hello_author() ->  None: 
    hello_author()

def test_config() -> None:
    dummy_inputs = {
        'PROJECT_NAME':'dummy-project', 
        'GITHUB_AUTHOR': 'dummy-author',
        'GITHUB_PAT': 'dummy-pat',
        'GITHUB_CLOUD_BUILD_APP_INSTALLATION_ID': 'dummy-id',
        'GCP_PROJECT_ID': 'wck-source',
        'GOOGLE_APPLICATION_CREDENTIALS': 'dummy-app-creds',
        'GCP_REGION_ID': 'dummy-region-id',
        'GCP_ARTIFACT_REGISTRY_REPO': 'dummy-art-registry',
        'GCP_TRIGGER_NAME': 'dummy-trigger',
        'TRIGGER_BRANCH_PATTERN': 'dummy-trigger-pattern',
    }

    config = Config(**dummy_inputs, run_validation=False) 
    config.gcp_project_number
    config.cloud_build_service_agent_email
    config.gcp_github_connection_name
    config.gcp_pat_secret_name
    config.gcp_pat_secret_path
    config.github_uri
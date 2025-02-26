"""
Put basic tests here to ensure that your package builds correctly and maintains its basic functionality.
"""

from {{cookiecutter.project_slug}} import hello_author
from {{cookiecutter.project_slug}}.cloud_infra.config import Config
import pytest 

def test_hello_author() ->  None: 
    hello_author()

def test_config() -> None:
    config = Config(run_validation=False) 
    config.gcp_project_number
    config.cloud_build_service_agent_email
    config.gcp_github_connection_name
    config.gcp_pat_secret_name
    config.gcp_pat_secret_path
    config.github_uri
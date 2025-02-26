from {{cookiecutter.project_slug}}.gcp_functions import assign_permissions_to_default_cloud_builder_service_account, create_secret
from {{cookiecutter.project_slug}}.setup_cloud_function import Config
import pytest 


@pytest.fixture 
def default_config() -> Config: 
    config = Config(run_validation=False)
    return config 

def test_assign_permissions_to_default_cloud_builder_service_account(
default_config, 
):
    assign_permissions_to_default_cloud_builder_service_account(
        gcp_project_id=default_config.GCP_PROJECT_ID, 
        gcp_project_number=default_config.gcp_project_number,
    )

def test_create_secret(default_config): 
    
    kwargs = {
        "secret_name":default_config.gcp_pat_secret_name,
        "project_id":default_config.GCP_PROJECT_ID,
        "secret_value":default_config.GITHUB_PAT,
        "service_account_email": default_config.cloud_build_service_agent_email,
    }

    create_secret(**kwargs)
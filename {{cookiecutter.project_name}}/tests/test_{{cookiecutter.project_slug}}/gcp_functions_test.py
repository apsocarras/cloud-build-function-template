from {{cookiecutter.project_slug}}.gcp_functions import assign_permissions_to_default_cloud_builder_service_account
from {{cookiecutter.project_slug}}.setup_cloud_function import Config
import pytest 


@pytest.fixture 
def default_config() -> Config: 
    config = Config()
    return config 

def test_assign_permissions_to_default_cloud_builder_service_account(
default_config, 
):
    assign_permissions_to_default_cloud_builder_service_account(
        gcp_project_id=default_config.GCP_PROJECT_ID, 
        gcp_project_number=default_config.gcp_project_number,
    )

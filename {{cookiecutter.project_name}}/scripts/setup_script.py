from pathlib import Path
from {{cookiecutter.project_slug}}.cloud_infra.config import Config 
from {{cookiecutter.project_slug}}.cloud_infra import gcp 
from {{cookiecutter.project_slug}}.cloud_infra import github

from google.cloud import resourcemanager_v3
from google.cloud.resourcemanager_v3.services.projects.client import ProjectsClient


import logging 

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

CUR_FILE = Path(__file__)
PROJECT_DIRECTORY = CUR_FILE.parents[1]
ENV_FILE_PATH = PROJECT_DIRECTORY / "_local" / ".env"

def main() -> None:

    config = Config.from_env(ENV_FILE_PATH, run_validation=False)

    logger.debug("Assigning permissions to default cloud build service account")
    _ = gcp.assign_permissions_to_default_cloud_builder_service_account(
        config.GCP_PROJECT_ID, config.gcp_project_number
    )

    logger.debug("Creating secret in google cloud for gh pat")
    gh_pat_secret_path = gcp.create_secret(
        secret_name=config.gcp_pat_secret_name,
        project_id=config.GCP_PROJECT_ID,
        secret_value=config.GITHUB_PAT,
    )

    logger.debug("Assigning the secret to the cloud builder service account")
    _ = gcp.assign_secret_to_service_account(
        service_account_email=config.cloud_build_service_agent_email,
        secret_path=gh_pat_secret_path,
    )

    logger.debug("Creating the cloud build to github connection")
    _ = gcp.create_github_cloud_build_connection(
        connection_name=config.gcp_github_connection_name,
        secret_path=config.gcp_pat_secret_path,
        cloud_build_install_id=config.GITHUB_CLOUD_BUILD_APP_INSTALLATION_ID,
        region_id=config.GCP_REGION_ID,
    )

    logger.debug("Connecting Cloud Build to GitHub via the connection")
    _ = gcp.connect_github_via_connection(
        project_name=config.PROJECT_NAME,
        github_uri=config.github_uri,
        connection_name=config.gcp_github_connection_name,
        region_id=config.GCP_REGION_ID,
    )

    logger.debug("Creating Artifact Registry Repository")
    _ = gcp.create_artifact_registry_repository(
        project_name=config.PROJECT_NAME,
        artifact_registry_repo_name=config.GCP_ARTIFACT_REGISTRY_REPO,
        region_id=config.GCP_REGION_ID,
        description=None,
    )

    logger.debug("Creating Cloud Build Trigger")
    _ = gcp.create_build_trigger(
        region_id=config.GCP_REGION_ID,
        project_name=config.PROJECT_NAME,
        author=config.GITHUB_AUTHOR,
        trigger_name=config.GCP_TRIGGER_NAME,
        trigger_pattern=config.TRIGGER_BRANCH_PATTERN,
        service_account_email=config.cloud_build_service_agent_email,
    )


if __name__ == "__main__": 
    main()
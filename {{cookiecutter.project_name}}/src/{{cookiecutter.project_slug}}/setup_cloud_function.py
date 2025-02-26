from dataclasses import dataclass

from google.cloud import resourcemanager_v3
from google.cloud.resourcemanager_v3.services.projects.client import ProjectsClient

from .gcp_functions import (
    assign_permissions_to_default_cloud_builder_service_account,
    assign_secret_to_service_account,
    connect_github_via_connection,
    create_artifact_registry_repository,
    create_build_trigger,
    create_github_cloud_build_connection,
    create_secret,
    make_secret_path,
)
from .github_functions import (
    check_github_pat,
    check_github_repo,
)


@dataclass
class Config:
    PROJECT_NAME: str = "{{cookiecutter.project_name}}"  # gh repo name
    GITHUB_PAT: str = "{{cookiecutter.github_pat}}"
    GITHUB_AUTHOR: str = "{{cookiecutter.author_github_handle}}"
    GITHUB_CLOUD_BUILD_INSTALLATION_ID: str = (
        "{{cookiecutter.github_cloud_build_app_installation_id}}"
    )
    GCP_PROJECT_ID: str = (
        "{{cookiecutter.gcp_project_id}}"  # name of organizing project in GCP
    )
    GOOGLE_APPLICATION_CREDENTIALS: str = (
        "{{cookiecutter.google_application_credentials}}"
    )
    GCP_REGION_ID: str = "{{cookiecutter.gcp_region_id}}"
    GCP_ARTIFACT_REGISTRY_REPO: str = "{{cookiecutter.gcp_artifact_registry_repo_name}}"
    GCP_TRIGGER_NAME: str = "{{cookiecutter.gcp_trigger_name}}"
    GCP_TRIGGER_PATTERN: str = "{{cookiecutter.trigger_branch_pattern}}"

    run_validation: bool = True

    @property
    def gcp_project_number(self) -> str:
        projects_client: ProjectsClient = resourcemanager_v3.ProjectsClient()
        project_name = f"projects/{self.GCP_PROJECT_ID}"
        project: resourcemanager_v3.Project = projects_client.get_project(
            name=project_name
        )
        project_number = project.name.split("/")[-1]
        return project_number

    @property
    def cloud_build_service_agent_email(self) -> str:
        return f"service-${self.gcp_project_number}@gcp-sa-cloudbuild.iam.gserviceaccount.com"

    @property
    def gcp_github_connection_name(self) -> str:
        return f"{self.PROJECT_NAME}-gh-connection"

    @property
    def gcp_pat_secret_name(self) -> str:
        return f"{self.PROJECT_NAME}-github-pat"

    @property
    def gcp_pat_secret_path(self) -> str:
        return make_secret_path(
            secret_name=self.gcp_pat_secret_name, project_id=self.GCP_PROJECT_ID
        )

    @property
    def github_uri(self) -> str:
        return f"https://github.com/{self.GITHUB_AUTHOR}/{self.PROJECT_NAME}.git"

    ## Validation steps
    def __post_init__(self) -> None:
        if self.run_validation:
            check_github_pat(self.GITHUB_AUTHOR, self.GITHUB_PAT)
            _ = check_github_repo(
                self.GITHUB_AUTHOR, self.PROJECT_NAME, self.GITHUB_PAT
            )


if __name__ == "__main__":
    config = Config()

    assign_permissions_to_default_cloud_builder_service_account(
        config.GCP_PROJECT_ID, config.gcp_project_number
    )
    gh_pat_secret_path = create_secret(
        secret_name=config.gcp_pat_secret_name,
        project_id=config.GCP_PROJECT_ID,
        secret_value=config.GITHUB_PAT,
        service_account_email=config.cloud_build_service_agent_email,
    )

    assign_secret_to_service_account(
        service_account_email=config.cloud_build_service_agent_email,
        secret_path=gh_pat_secret_path,
    )

    create_github_cloud_build_connection(
        connection_name=config.gcp_github_connection_name,
        secret_path=config.gcp_pat_secret_path,
        cloud_build_install_id=config.GITHUB_CLOUD_BUILD_INSTALLATION_ID,
        region_id=config.GCP_REGION_ID,
    )

    connect_github_via_connection(
        project_name=config.PROJECT_NAME,
        github_uri=config.github_uri,
        connection_name=config.gcp_github_connection_name,
        region_id=config.GCP_REGION_ID,
    )

    create_artifact_registry_repository(
        project_name=config.PROJECT_NAME,
        artifact_registry_repo_name=config.GCP_ARTIFACT_REGISTRY_REPO,
        region_id=config.GCP_REGION_ID,
        description=None,
    )

    create_build_trigger(
        region_id=config.GCP_REGION_ID,
        project_name=config.PROJECT_NAME,
        author=config.GITHUB_AUTHOR,
        trigger_name=config.GCP_TRIGGER_NAME,
        trigger_pattern=config.GCP_TRIGGER_PATTERN,
        service_account_email=config.cloud_build_service_agent_email,
    )

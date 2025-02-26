import logging
from dataclasses import dataclass

from google.cloud import resourcemanager_v3
from google.cloud.resourcemanager_v3.services.projects.client import ProjectsClient

from .gcp import (
    make_secret_path,
)
from .github import (
    check_github_pat,
    check_github_repo,
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@dataclass
class Config:
    PROJECT_NAME: str  # gh repo name
    GITHUB_PAT: str
    GITHUB_AUTHOR: str
    GITHUB_CLOUD_BUILD_INSTALLATION_ID: str
    GCP_PROJECT_ID: str
    GOOGLE_APPLICATION_CREDENTIALS: str
    GCP_REGION_ID: str
    GCP_ARTIFACT_REGISTRY_REPO: str
    GCP_TRIGGER_NAME: str
    GCP_TRIGGER_PATTERN: str

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
        return f"service-{self.gcp_project_number}@gcp-sa-cloudbuild.iam.gserviceaccount.com"

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

import logging
from dataclasses import dataclass, fields
from pathlib import Path

from dotenv import dotenv_values
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
    GITHUB_PAT: str
    GITHUB_CLOUD_BUILD_APP_INSTALLATION_ID: str
    GCP_PROJECT_ID: str
    GOOGLE_APPLICATION_CREDENTIALS: str
    GCP_REGION_ID: str
    GCP_ARTIFACT_REGISTRY_REPO: str
    GCP_TRIGGER_NAME: str
    TRIGGER_BRANCH_PATTERN: str
    PROJECT_NAME: str
    GITHUB_AUTHOR: str
    run_validation: bool = True

    @classmethod
    def from_env(
        cls,
        env_path: str | Path,
        run_validation: bool = True,
        **kwargs: dict[str, str | bool],
    ) -> "Config":
        field_names = set(f.name for f in fields(cls))
        env_values = {
            k: v for k, v in dotenv_values(env_path).items() if k in field_names
        }
        inputs: dict[str, str | bool] = {
            **env_values,
            **{"run_validation": run_validation},
            **kwargs,
        }  # pyright: ignore[reportAssignmentType]
        return cls(**inputs)  # pyright: ignore[reportArgumentType]

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


from dataclasses import dataclass


@dataclass
class Toy:
    foo: str = "bar"


set(f.name for f in fields(Toy))

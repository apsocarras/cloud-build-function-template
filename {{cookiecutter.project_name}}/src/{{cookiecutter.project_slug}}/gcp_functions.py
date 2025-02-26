import logging
import subprocess
from ast import TypeAlias
from typing import TypeAlias

from google.cloud import secretmanager
from google.cloud.secretmanager_v1.services.secret_manager_service.client import (
    SecretManagerServiceClient,
)

logger = logging.getLogger(__name__)

SecretPath: TypeAlias = str


def assign_permissions_to_default_cloud_builder_service_account(
    gcp_project_id: str,
    gcp_project_number: str,
) -> None:
    default_cloud_build_service_account = (
        f"service-{gcp_project_number}@gcp-sa-cloudbuild.iam.gserviceaccount.com"
    )
    cmds = [
        "gcloud",
        "projects",
        "add-iam-policy-binding",
        gcp_project_id,
        f"--member=serviceAccount:{default_cloud_build_service_account}",
        "--role=roles/cloudbuild.builds.builder",
    ]
    result = subprocess.run(cmds, check=True, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(
            f"Command failed with return code {result.returncode}: {result.stderr}"
        )


def make_secret_path(secret_name: str, project_id: str) -> SecretPath:
    parent = f"projects/{project_id}"
    secret_path = f"{parent}/secrets/{secret_name}"
    return secret_path


def create_secret(
    secret_name: str,
    project_id: str,
    secret_value: str,
    service_account_email: str,
    overwrite: bool = True,
) -> SecretPath:
    client: SecretManagerServiceClient = secretmanager.SecretManagerServiceClient()

    secret_path = make_secret_path(secret_name=secret_name, project_id=project_id)

    try:
        _ = client.get_secret(name=secret_path)
        logger.info(f"Secret {secret_name} already exists in project {project_id}")
        if overwrite:
            logger.info("Overwriting secret with new value.")
            client.delete_secret(name=secret_path)

    except Exception as e:
        if "NotFound" in str(e):
            logger.info(
                f"Secrete {secret_name} not found in prolect {project_id}. Creating."
            )
            pass
        else:
            raise

    secret = client.create_secret(
        parent=parent,
        secret_id=secret_name,
    )

    _ = client.add_secret_version(
        parent=secret.name,
        payload={"data": secret_value.encode()},  # pyright: ignore[reportArgumentType]
    )

    return secret_path


def assign_secret_to_service_account(
    service_account_email: str, secret_path: SecretPath
) -> None:
    """TODO: not sure how to do this with the google cloud sdk"""
    cmds = [
        "gcloud",
        "secrets",
        "add-iam-policy-binding",
        secret_path,
        f"--member='serviceAccount:${service_account_email}'",
        "--role='roles/secretmanager.secretAccessor'",
    ]
    subprocess.call(cmds)
    return None


def create_github_cloud_build_connection(
    connection_name: str,
    secret_path: SecretPath,
    cloud_build_install_id: str,  # github.com/settings/installations/
    region_id: str,
) -> None:
    cmds = [
        "gcloud",
        "builds",
        "connections",
        "create",
        "github",
        connection_name,
        f"--authorizer-token-secret-version='{connection_name}'",
        f"--app-installation-id='{cloud_build_install_id}'",
        f"--region={region_id}",
    ]
    subprocess.call(cmds)
    return


def connect_github_via_connection(
    project_name: str,
    github_uri: str,
    connection_name: str,
    region_id: str,
) -> None:
    cmds = [
        "gcloud",
        "builds",
        "repositories",
        "create",
        project_name,
        f"--remote-uri='{github_uri}'",
        f"--connection='{connection_name}'",
        f"--region='{region_id}'",
    ]
    subprocess.call(cmds)
    return


def create_artifact_registry_repository(
    project_name: str,
    artifact_registry_repo_name: str,
    region_id: str,
    description: str | None = None,
) -> None:
    description = (
        description
        or f"Repository for images related to the {project_name} cloud build project"
    )
    cmds = [
        "gcloud",
        "artifacts",
        "repositories",
        "create",
        artifact_registry_repo_name,
        "--repository-format=docker",
        f"--location='{region_id}'",
        f"--description='{description}'",
    ]

    subprocess.call(cmds)


def create_build_trigger(
    region_id: str,
    project_name: str,
    author: str,
    trigger_pattern: str,
    trigger_name: str,
    service_account_email: str,
) -> None:
    cmds = [
        "gcloud",
        "builds",
        "triggers",
        "create",
        "github",
        f"--region='{region_id}'",
        f"--repo-name='{project_name}'",
        f"--repo-owner='{author}'",
        f"--branch-pattern='{trigger_pattern}'",
        "--build-config=cloudbuild.yaml",
        f"--name='{trigger_name}'",
        f"--service-account='{service_account_email}'",
        # --require-approval,
        # --include-logs-with-status,
    ]
    subprocess.call(cmds)

import logging
import subprocess
from ast import TypeAlias
from subprocess import CompletedProcess
from typing import TypeAlias

from google.cloud import secretmanager, secretmanager_v1
from google.cloud.secretmanager_v1.services.secret_manager_service.client import (
    SecretManagerServiceClient,
)
from google.cloud.secretmanager_v1.types.service import (
    DeleteSecretRequest,
    GetSecretRequest,
)

logger = logging.getLogger(__name__)

SecretPath: TypeAlias = str


def run_subprocess_w_check(
    cmds: list[str], quiet: bool = True
) -> CompletedProcess[str]:
    extra_cmd = ["--quiet"] if quiet else []
    try:
        result: CompletedProcess[str] = subprocess.run(
            cmds + extra_cmd,
            check=True,
            capture_output=True,
            text=True,
        )
        return result
    except subprocess.CalledProcessError as e:
        error_data = {
            "return_code": e.returncode,
            "command": e.cmd,
            "output": e.output.strip(),
            "error": e.stderr.strip(),
        }
        raise RuntimeError(error_data) from e


def assign_permissions_to_default_cloud_builder_service_account(
    gcp_project_id: str, gcp_project_number: str, quiet: bool = True
) -> CompletedProcess[str]:
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

    result = run_subprocess_w_check(cmds, quiet)
    return result


def make_secret_path(secret_name: str, project_id: str) -> SecretPath:
    parent = f"projects/{project_id}"
    secret_path = f"{parent}/secrets/{secret_name}"
    return secret_path


def create_secret(
    secret_name: str,
    project_id: str,
    secret_value: str,
    overwrite: bool = True,
) -> SecretPath:
    """https://codelabs.developers.google.com/codelabs/secret-manager-python?authuser=2#5"""
    client: SecretManagerServiceClient = secretmanager.SecretManagerServiceClient()

    parent = f"projects/{project_id}"
    secret_path = make_secret_path(secret_name=secret_name, project_id=project_id)
    secret = {"replication": {"automatic": {}}}

    try:
        get_request: GetSecretRequest = secretmanager_v1.GetSecretRequest(
            name=secret_path,
        )
        _ = client.get_secret(request=get_request)
        logger.info(f"Secret {secret_name} already exists in project {project_id}")
        if overwrite:
            logger.info("Overwriting secret with new value.")

            del_request: DeleteSecretRequest = secretmanager_v1.DeleteSecretRequest(
                name=secret_path
            )

            client.delete_secret(request=del_request)

    except Exception as e:
        if "NotFound" in str(e) or "not found" in str(e):
            logger.info(
                f"Secret {secret_name} not found in project {project_id}. Creating."
            )
            pass
        else:
            raise

    _ = client.create_secret(secret_id=secret_name, parent=parent, secret=secret)  # pyright: ignore[reportArgumentType]

    # add secret version w/ new value
    payload = secret_value.encode("UTF-8")
    request = secretmanager.AddSecretVersionRequest(
        parent=secret_path, payload={"data": payload}
    )
    _ = client.add_secret_version(request=request)

    return secret_path


def assign_secret_to_service_account(
    service_account_email: str, secret_path: SecretPath, quiet: bool = True
) -> CompletedProcess[str]:
    """TODO: not sure how to do this with the google cloud sdk"""
    cmds = [
        "gcloud",
        "secrets",
        "add-iam-policy-binding",
        secret_path,
        f"--member=serviceAccount:{service_account_email}",
        "--role=roles/secretmanager.secretAccessor",
    ]
    return run_subprocess_w_check(cmds, quiet)


def create_github_cloud_build_connection(
    connection_name: str,
    secret_path: SecretPath,
    cloud_build_install_id: str,  # github.com/settings/installations/
    region_id: str,
    secret_version: int = 1,
    quiet: bool = True,
) -> None:
    cmds = [
        "gcloud",
        "builds",
        "connections",
        "create",
        "github",
        connection_name,
        f"--authorizer-token-secret-version={secret_path}/versions/{secret_version}",
        f"--app-installation-id={cloud_build_install_id}",
        f"--region={region_id}",
    ]
    try:
        _ = run_subprocess_w_check(cmds, quiet)
    except RuntimeError as e:
        if "already exists" in str(e):
            logger.info(
                f"GitHub Cloud Build Connection {connection_name} already exists."
            )
            return
        else:
            raise e


def connect_github_via_connection(
    project_name: str,
    github_uri: str,
    connection_name: str,
    region_id: str,
    quiet: bool = True,
) -> None:
    cmds = [
        "gcloud",
        "builds",
        "repositories",
        "create",
        project_name,
        f"--remote-uri={github_uri}",
        f"--connection={connection_name}",
        f"--region={region_id}",
    ]
    try:
        _ = run_subprocess_w_check(cmds, quiet)
    except RuntimeError as e:
        if "already exists" in str(e):
            logger.info(f"GitHub repository {github_uri} already connected.")
            return
        else:
            raise e


def create_artifact_registry_repository(
    project_name: str,
    artifact_registry_repo_name: str,
    region_id: str,
    description: str | None = None,
    quiet: bool = True,
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
        f"--location={region_id}",
        f"--description='{description}'",
    ]
    try:
        _ = run_subprocess_w_check(cmds, quiet)
    except RuntimeError as e:
        if "already exists" in str(e):
            logger.info(
                f"Artifact repository {artifact_registry_repo_name} already exists."
            )
            return
        else:
            raise e


def create_build_trigger(
    region_id: str,
    project_name: str,
    author: str,
    trigger_pattern: str,
    trigger_name: str,
    service_account_email: str,
    quiet: bool = True,
) -> None:
    cmds = [
        "gcloud",
        "builds",
        "triggers",
        "create",
        "github",
        f"--region={region_id}",
        f"--repo-name={project_name}",
        f"--repo-owner={author}",
        f"--branch-pattern={trigger_pattern}",
        "--build-config=cloudbuild.yaml",
        f"--name={trigger_name}",
        f"--service-account={service_account_email}",
        # --require-approval,
        # --include-logs-with-status,
    ]
    try:
        _ = run_subprocess_w_check(cmds, quiet)
    except RuntimeError as e:
        if "already exists" in str(e):
            logger.info(f"Artifact repository {trigger_name} already exists.")
            return
        else:
            raise e

from types import MappingProxyType

## Default user inputs provided during cookiecutter setup.
USER_INPUTS = MappingProxyType(
    {
        "PROJECT_NAME": "{{cookiecutter.project_name}}",  # gh repo name
        "GITHUB_PAT": "{{cookiecutter.github_pat}}",
        "GITHUB_AUTHOR": "{{cookiecutter.author_github_handle}}",
        "GITHUB_CLOUD_BUILD_INSTALLATION_ID": "{{cookiecutter.github_cloud_build_app_installation_id}}",
        "GCP_PROJECT_ID": "{{cookiecutter.gcp_project_id}}",  # name of organizing project in GCP
        "GOOGLE_APPLICATION_CREDENTIALS": "{{cookiecutter.google_application_credentials}}",
        "GCP_REGION_ID": "{{cookiecutter.gcp_region_id}}",
        "GCP_ARTIFACT_REGISTRY_REPO": "{{cookiecutter.gcp_artifact_registry_repo_name}}",
        "GCP_TRIGGER_NAME": "{{cookiecutter.gcp_trigger_name}}",
        "GCP_TRIGGER_PATTERN": "{{cookiecutter.trigger_branch_pattern}}",
    }
)

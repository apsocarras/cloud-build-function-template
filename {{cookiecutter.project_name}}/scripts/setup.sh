#!/bin/bash 

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

## Set environmental variables 
# Added by cookiecutter initialization
PROJECT_NAME="{{cookiecutter.project_name}}" # gh repo name
GITHUB_PAT="{{cookiecutter.github_pat}}"
GITHUB_AUTHOR="{{cookiecutter.github_author}}"
GITHUB_CLOUD_BUILD_INSTALLATION_ID="{{cookiecutter.github_cloud_build_app_installation_id}}"
GCP_PROJECT_ID="{{cookiecutter.gcp_project_id}}" # name of organizing project in GCP
GCP_REGION_ID="{{cookiecutter.gcp_region_id}}"
GCP_ARTIFACT_REGISTRY_REPO="{{cookiecutter.gcp_artifact_registry_repo_name}}"
# DOCKER_IMAGE_NAME="{{cookiecutter.docker_image_name}}"
GCP_TRIGGER_NAME="{{cookiecutter.gcp_trigger_name}}"
GCP_TRIGGER_PATTERN="{{cookiecutter.trigger_branch_pattern}}"
# GCP_LOG_BUCKET_NAME="{{cookiecutter.gcp_log_bucket_name}}"

# Derived variables 
GCP_PROJECT_NUMBER=$(gcloud projects describe ${GCP_PROJECT_ID} --format="value(projectNumber)")
DEFAULT_CLOUD_BUILD_SERVICE_AGENT="service-${GCP_PROJECT_NUMBER}@gcp-sa-cloudbuild.iam.gserviceaccount.com"
GCP_GH_CONNECTION_NAME="${PROJECT_NAME}-gh-connection"
GCP_PAT_SECRET_NAME="${PROJECT_NAME}-github-pat"
GITHUB_URI="https://github.com/{$GITHUB_AUTHOR}/{$PROJECT_NAME}.git"

#### --- Prerequisites --- ####

### Install the Cloud Build GitHub App on your GitHub account or in an organization you own.

### Verify gh auth login matches author account 
GH_ACTIVE_ACCOUNT=$(gh auth status --active | sed -n 's/.*github.com account \([^ ]*\).*/\1/p')
bash "$SCRIPT_DIR/check_accounts/check_github_account_CLI.sh" "$GITHUB_AUTHOR" "$GH_ACTIVE_ACCOUNT"

### Verify core.project in gcloud CLI matches project id setting 
ACTIVE_PROJECT_ID=$(gcloud config list --format="value(core.project)")
bash "$SCRIPT_DIR/check_accounts/check_gcloud_CLI.sh" "$GCP_PROJECT_ID" "$ACTIVE_PROJECT_ID"

### Verify github repository exists: {{cookiecutter.github_author}}/{{cookiecutter.project_name}}
bash "$SCRIPT_DIR/check_accounts/check_github_repo_CLI.sh" $GITHUB_AUTHOR $PROJECT_NAME $GITHUB_PAT

#### -------------------- ####

## PROVIDE PERMISSIONS TO CLOUD BUILDER SERVICE ACCOUNT 
gcloud projects add-iam-policy-binding $GCP_PROJECT_ID \
    --member="serviceAccount:${DEFAULT_CLOUD_BUILD_SERVICE_AGENT}" \
    --role="roles/cloudbuild.builds.builder"

## CONNECT GITHUB REPO TO CLOUD BUILD: https://cloud.google.com/build/docs/automating-builds/github/connect-repo-github?authuser=2#gcloud_1

bash "$SCRIPT_DIR"/gcloud_setup/setup_secret.sh \
    $GCP_PAT_SECRET_NAME \
    $GCP_PROJECT_ID \
    $GITHUB_PAT \
    "$DEFAULT_CLOUD_BUILD_SERVICE_AGENT"

SECRET_PATH="projects/$GCP_PROJECT_ID/secrets/$GCP_PAT_SECRET_NAME/versions/1"
echo "INFO: Created secret at $SECRET_PATH"
bash "$SCRIPT_DIR/gcloud_setup/create_github_connection.sh" \
    "$GCP_GH_CONNECTION_NAME" \
    "$SECRET_PATH" \
    "$GITHUB_CLOUD_BUILD_INSTALLATION_ID" \
    "$GCP_REGION_ID"\

bash "$SCRIPT_DIR/gcloud_setup/connect_github_via_connection.sh" \
    "$PROJECT_NAME" \
    "$GITHUB_URI" \
    "$GCP_GH_CONNECTION_NAME" \
    "$GCP_REGION_ID"

## CREATE ARTIFACT REPOSITORY
bash "$SCRIPT_DIR/gcloud_setup/create_artifact_registry_repo.sh" $GCP_ARTIFACT_REGISTRY_REPO $GCP_REGION_ID $PROJECT_NAME 

## CREATE BUILD TRIGGER 
bash "$SCRIPT_DIR/gcloud_setup/create_build_trigger.sh" "$GCP_REGION_ID" "$PROJECT_NAME" "$GITHUB_AUTHOR" "$GCP_TRIGGER_PATTERN" "$GCP_TRIGGER_NAME" "$DEFAULT_CLOUD_BUILD_SERVICE_AGENT"

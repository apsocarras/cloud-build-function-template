#!/bin/bash 

## Set environmental variables 
# Added by cookiecutter initialization
PROJECT_NAME="{{cookiecutter.project_name}}" # gh repo name
GITHUB_PAT="{{cookiecutter.github_pat}}"
GITHUB_AUTHOR="{{cookiecutter.author_github_handle}}"
GCP_PROJECT_ID="{{cookiecutter.gcp_project_id}}" # name of organizing project in GCP
GCP_REGION_ID="{{cookiecutter.gcp_region_id}}"
GCP_ARTIFACT_REGISTRY_REPO="{{cookiecutter.gcp_artifact_registry_repo_name}}"
DOCKER_IMAGE_NAME="{{cookiecutter.docker_image_name}}"
GCP_TRIGGER_NAME="{{cookiecutter.gcp_trigger_name}}"
GCP_TRIGGER_PATTERN="{{cookiecutter.trigger_branch_pattern}}"
GCP_LOG_BUCKET_NAME="{{cookiecutter.gcp_log_bucket_name}}"

# Derived variables 
GCP_PROJECT_NUMBER=$(gcloud projects describe ${GCP_PROJECT_ID} --format="value(projectNumber)")
DEFAULT_CLOUD_BUILD_SERVICE_AGENT="service-${GCP_PROJECT_NUMBER}@gcp-sa-cloudbuild.iam.gserviceaccount.com"

#### --- Prerequisites --- ####

### Install the Cloud Build GitHub App on your GitHub account or in an organization you own.

### Authenticate shell session with: gcloud auth login and gh cli
## gh auth login 
if gh auth status --json user --quiet > /dev/null; then
    echo "Authenticated with GitHub CLI"
else
    echo "Not authenticated with GitHub CLI"
    exit 1
fi
## gcloud auth login
if gcloud auth list --filter=status:ACTIVE --format="value(account)" > /dev/null; then
    echo "Authenticated with gcloud CLI"
else
    echo "Not authenticated with gcloud CLI"
    exit 1
fi

## Verify that the core.project in gcloud CLI is the same as the cookiecutter setting 
CUR_PROJECT_ID=$(gcloud config list --format="value(core.project)")
if [[ "$CUR_PROJECT_ID" != "$GCP_PROJECT_ID" ]]; then 
    echo "Current value(core.project) ($CUR_PROJECT_ID) is different from cookiecutter input ($GCP_PROJECT_ID)."
    echo "Run 'gcloud config set project $GCP_PROJECT_ID' and rerun the script".
    exit 1
fi 

### Create github repository: {{cookiecutter.author_github_handle}}/{{cookiecutter.project_name}}
export REPO_ENDPOINT="${GITHUB_AUTHOR}/${PROJECT_NAME}"
response_message=$(curl -s -w "%{message}" -o response.txt https://api.github.com/repos/${REPO_ENDPOINT})

if [[ "$response_message" == "Not Found"]]; then 
    echo "Found github repo at: $REPO_ENDPOINT"
else 
    echo "GitHub repo not found: $REPO_ENDPOINT"
    exit 1
fi 

#### -------------------- ####

## PROVIDE PERMISSIONS TO CLOUD BUILDER SERVICE ACCOUNT 
gcloud projects add-iam-policy-binding $GCP_PROJECT_ID \
    --member="serviceAccount:${DEFAULT_CLOUD_BUILD_SERVICE_AGENT}" \
    --role="roles/cloudbuild.builds.builder"

## CONNECT GITHUB REPO TO CLOUD BUILD: https://cloud.google.com/build/docs/automating-builds/github/connect-repo-github?authuser=2#gcloud_1
# Add to google cloud secrets 
GCP_PAT_SECRET_NAME="${PROJECT_NAME}-github-pat"
echo -n $GITHUB_PAT | gcloud secrets create $GCP_PAT_SECRET_NAME --data-file=-

# Grant access to the Cloud Build Service Agent on the secret, where SECRET_NAME is the name of your secret as stored in Secret Manager:
gcloud secrets add-iam-policy-binding $GCP_PAT_SECRET_NAME \
    --member="serviceAccount:${DEFAULT_CLOUD_BUILD_SERVICE_AGENT}" \
    --role="roles/secretmanager.secretAccessor"

# Create the GitHub Connection 
GCP_GH_CONNECTION_NAME="${PROJECT_NAME}-gh-connection"
gcloud builds connections create github $GCP_GH_CONNECTION_NAME \
    --authorizer-token-secret-version=projects/$GCP_PROJECT_ID/secrets/$GCP_PAT_SECRET_NAME/versions/1 \
    --app-installation-id=

# Connect the repo via the Connection
GITHUB_URI="https://github.com/{$GITHUB_AUTHOR}/{$PROJECT_NAME}.git"
gcloud builds repositories create $PROJECT_NAME \
    --remote-uri=$GITHUB_URI \
    --connection=$GCP_GH_CONNECTION_NAME --region=$GCP_REGION_ID

## CREATE ARTIFACT REPOSITORY
gcloud artifacts repository create ${GCP_ARTIFACT_REGISTRY_REPO} \
    --repository-format=docker \
    --location=$GCP_REGION_ID \
    --description="Repository for images related to the ${PROJECT_NAME} cloud build project"

## CREATE BUILD TRIGGER 
gcloud builds triggers create github \
    --region=$GCP_REGION_ID \
    --repo-name=$PROJECT_NAME \
    --repo-owner=$GITHUB_AUTHOR \
    --branch-pattern=$GCP_TRIGGER_PATTERN \
    --build-config=cloudbuild.yaml \
    --name=$GCP_TRIGGER_NAME
    --service-account=$DEFAULT_CLOUD_BUILD_SERVICE_AGENT
    # --require-approval \
    # --include-logs-with-status \

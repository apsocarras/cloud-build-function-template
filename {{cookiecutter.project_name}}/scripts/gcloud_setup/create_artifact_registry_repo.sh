#!/bin/bash 

GCP_ARTIFACT_REGISTRY_REPO=$1 
GCP_REGION_ID=$2
PROJECT_NAME=$3

gcloud artifacts repositories create "$GCP_ARTIFACT_REGISTRY_REPO" \
    --repository-format=docker \
    --location="$GCP_REGION_ID" \
    --description="Repository for images related to the ${PROJECT_NAME} cloud build project" \
    --quiet
#!/bin/bash 

CONNECTION_NAME=$1
SECRET_PATH=$2
GCP_GH_BUILD_INSTALL_ID=$3
GCP_REGION_ID=$4

# Create the github connection
gcloud builds connections create github "$CONNECTION_NAME" \
    --authorizer-token-secret-version="$SECRET_PATH" \
    --app-installation-id="$GCP_GH_BUILD_INSTALL_ID" \
    --region="$GCP_REGION_ID"
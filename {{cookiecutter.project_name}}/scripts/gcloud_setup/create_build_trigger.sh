#!/bin/bash 

REGION=$1
PROJECT_NAME=$2
AUTHOR=$3
TRIGGER_PATTERN=$4
TRIGGER_NAME=$5
SERVICE_ACCOUNT_EMAIL=$6

gcloud builds triggers create github \
    --region="$REGION" \
    --repo-name="$PROJECT_NAME" \
    --repo-owner="$AUTHOR" \
    --branch-pattern="$TRIGGER_PATTERN" \
    --build-config=cloudbuild.yaml \
    --name="$TRIGGER_NAME" \
    --service-account="$SERVICE_ACCOUNT_EMAIL"\
    --quiet
    # --require-approval \
    # --include-logs-with-status \

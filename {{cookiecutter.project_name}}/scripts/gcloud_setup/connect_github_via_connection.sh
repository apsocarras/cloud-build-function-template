#!/bin/bash

PROJECT_NAME=$1
GITHUB_URI=$2
CONNECTION_NAME=$3
REGION=$4

gcloud builds repositories create "$PROJECT_NAME" \
    --remote-uri="$GITHUB_URI" \
    --connection="$CONNECTION_NAME" \
    --region="$REGION" \
    --quiet


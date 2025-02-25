#!/bin/bash 

SECRET_NAME=$1
PROJECT_ID=$2
SECRET_VALUE=$3
SERVICE_ACCOUNT_NAME=$4

## Check if the secret exists; create if not 
if gcloud secrets describe "$SECRET_NAME" --project "$PROJECT_ID" &>/dev/null; then 
    echo "projects/$PROJECT_ID/secrets/$SECRET_NAME/versions/1"
else 
    echo "Secret $SECRET_NAME does not exist in the project $PROJECT_ID. Creating."
    echo -n "$SECRET_VALUE" | gcloud secrets create "$SECRET_NAME" --data-file=-=

    ## Grant access to the service account 
    gcloud secrets add-iam-policy-binding "$GCP_PAT_SECRET_NAME" \
        --member="serviceAccount:${SERVICE_ACCOUNT_NAME}" \
        --role="roles/secretmanager.secretAccessor"
    
    echo "projects/$PROJECT_ID/secrets/$SECRET_NAME/versions/1"
fi



#!/bin/bash 

SECRET_NAME=$1
PROJECT_ID=$2
SECRET_VALUE=$3
SERVICE_ACCOUNT_NAME=$4

temp_file="tmp_$SECRET_NAME.txt"
echo "$SECRET_VALUE" >> "$temp_file"

## Check if the secret exists; create if not 
if gcloud secrets describe "$SECRET_NAME" --project "$PROJECT_ID" &>/dev/null; then 
    echo "Secret $SECRET_NAME already exists in project $PROJECT_ID. Replacing it."
    # TODO Remove the existing secret and replace it with the new one
    gcloud secrets delete "$SECRET_NAME" --project "$PROJECT_ID"
    echo -n "$SECRET_VALUE" | gcloud secrets create "$SECRET_NAME" --data-file="$temp_file" --project "$PROJECT_ID"
    
    ## Grant access to the service account 
    gcloud secrets add-iam-policy-binding "$GCP_PAT_SECRET_NAME" \
        --member="serviceAccount:${SERVICE_ACCOUNT_NAME}" \
        --role="roles/secretmanager.secretAccessor"

else 
    echo "Secret $SECRET_NAME does not exist in the project $PROJECT_ID. Creating."
    echo -n "$SECRET_VALUE" | gcloud secrets create "$SECRET_NAME" --data-file="$temp_file" --project "$PROJECT_ID"

    ## Grant access to the service account 
    gcloud secrets add-iam-policy-binding "$GCP_PAT_SECRET_NAME" \
        --member="serviceAccount:${SERVICE_ACCOUNT_NAME}" \
        --role="roles/secretmanager.secretAccessor"
fi

rm "$temp_file"



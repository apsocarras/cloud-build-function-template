#!/bin/bash 
# if gcloud auth list --filter=status:ACTIVE --format="value(account)" > /dev/null; then
#     echo true 
# else
#     echo false
# fi

TARGET_PROJECT_ID=$1
ACTIVE_PROJECT_ID=$2  
if [[ "$ACTIVE_PROJECT_ID" != "$TARGET_PROJECT_ID" ]]; then 
    echo "Current value(core.project) ($ACTIVE_PROJECT_ID) is different from cookiecutter input ($TARGET_PROJECT_ID)."
    echo "Run 'gcloud config set project $GCP_PROJECT_ID' and rerun the script".
    return
else 
    echo true 
fi 
#!/bin/bash 

AUTHOR=$1 
REPO_NAME=$2
GITHUB_PAT=$3

response=$(curl -s -w -o response.txt \
    -H "Authorization: token ${GITHUB_PAT}" \
    https://api.github.com/repos/"${AUTHOR}"/"${REPO_NAME}")

if [[ "$response" == "Not Found" ]]; then 
    echo "Found github repo at: ${URL}"
else
    echo "WARNING: GitHub repo not found (${URL}) ($response)"
    echo "INFO: Note that your current GitHub account might have permissions to upload to the repository, but not list it programmatically."
    echo "INFO: This can happen if the repo is a private repo in an organization you're a member of."
fi 

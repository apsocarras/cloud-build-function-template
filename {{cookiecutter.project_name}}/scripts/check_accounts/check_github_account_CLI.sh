#!/bin/bash 

AUTHOR_ACCOUNT=$1
ACTIVE_ACCOUNT=$2

if [[ "$ACTIVE_ACCOUNT" == "$AUTHOR_ACCOUNT" ]]; then 
    echo "Authenticated with GitHub CLI as ${AUTHOR_ACCOUNT}"
elif [[ "$ACTIVE_ACCOUNT" != "" ]]; then
    echo "Warning: logged into GitHub CLI with $ACTIVE_ACCOUNT (!= $ACTIVE_ACCOUNT)"
    return 1
else 
    echo "Not authenticated with GitHub CLI"
    return 1
fi

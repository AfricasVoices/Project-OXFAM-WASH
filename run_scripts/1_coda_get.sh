#!/usr/bin/env bash

set -e

if [[ $# -ne 3 ]]; then
    echo "Usage: ./1_coda_get.sh <coda-auth-file> <coda-v2-root> <data-root>"
    echo "Downloads coded messages datasets from Coda to '<data-root>/Coded Coda Files'"
    exit
fi

AUTH=$1
CODA_V2_ROOT=$2
DATA_ROOT=$3

./checkout_coda_v2.sh "$CODA_V2_ROOT"

DATASETS=(
    "OXFAM_WASH_s01e01"
    "OXFAM_WASH_s01e02"
    "OXFAM_WASH_s01e03"
    "OXFAM_WASH_s01e03_Noise_Handler"
    "OXFAM_WASH_s01_Close_Out"

    "OXFAM_WASH_age"
    "OXFAM_WASH_gender"
    "OXFAM_WASH_location"
    "OXFAM_WASH_disabled"
    "OXFAM_WASH_Beneficiary_Consent"
    "OXFAM_WASH_s01_Programme_Evaluation"
    "OXFAM_WASH_s01_Accountability"
)

cd "$CODA_V2_ROOT/data_tools"
git checkout "c47977d03f96ba3e97c704c967c755f0f8b666cb"  # (master which supports incremental add)

mkdir -p "$DATA_ROOT/Coded Coda Files"

for DATASET in ${DATASETS[@]}
do
    FILE="$DATA_ROOT/Coded Coda Files/$DATASET.json"

    if [ -e "$FILE" ]; then
        echo "Getting messages data from ${DATASET} (incremental update)..."
        MESSAGES=$(pipenv run python get.py --previous-export-file-path "$FILE" "$AUTH" "${DATASET}" messages)
        echo "$MESSAGES" >"$FILE"
    else
        echo "Getting messages data from ${DATASET} (full download)..."
        pipenv run python get.py "$AUTH" "${DATASET}" messages >"$FILE"
    fi

done

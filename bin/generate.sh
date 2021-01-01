#!/usr/bin/env bash

# shellcheck disable=SC2155

cd "$(dirname "$0")/.." || exit 1

cd infra || exit 1
tf_output=$(terraform output -json)

cd .. 

export S3_BUCKET_FOR_OUTPUT=$(echo "$tf_output" | jq -r '. | .bucket_name.value')
python -m generator.util "$@"




#!/usr/bin/env bash

# shellcheck disable=SC2155

cd "$(dirname "$0")/.." || exit 1

cd infra || exit 1
tf_output=$(terraform output -json)

cd .. 

export SQS_OUTPUT_QUEUE=$(echo "$tf_output" | jq -r '. | .output_queue.value')
python -m poll "$@"

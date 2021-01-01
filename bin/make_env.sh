#!/usr/bin/env bash

# shellcheck disable=SC2155

cd "$(dirname "$0")/.." || exit 1

cd infra || exit 1
tf_output=$(terraform output -json)

cd .. 

S3_BUCKET_FOR_OUTPUT=$(echo "$tf_output" | jq -r '. | .bucket_name.value')
SQS_INPUT_QUEUE=$(echo "$tf_output" | jq -r '. | .input_queue.value')
SQS_OUTPUT_QUEUE=$(echo "$tf_output" | jq -r '. | .output_queue.value')
POLL_INTERVAL_SECONDS=1

cat > .env <<EOF
S3_BUCKET_FOR_OUTPUT=${S3_BUCKET_FOR_OUTPUT=$(echo "$tf_output" | jq -r '. | .bucket_name.value')}
SQS_INPUT_QUEUE=${SQS_INPUT_QUEUE=$(echo "$tf_output" | jq -r '. | .input_queue.value')}
SQS_OUTPUT_QUEUE=${SQS_OUTPUT_QUEUE=$(echo "$tf_output" | jq -r '. | .output_queue.value')}
POLL_INTERVAL_SECONDS=${POLL_INTERVAL_SECONDS=1}
EOF

cat .env
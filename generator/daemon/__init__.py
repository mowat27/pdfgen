from .. import S3_BUCKET_FOR_OUTPUT
import os

SQS_INPUT_QUEUE = os.environ.get('SQS_INPUT_QUEUE')
POLL_INTERVAL_SECONDS = int(os.environ.get('POLL_INTERVAL_SECONDS', '1'))

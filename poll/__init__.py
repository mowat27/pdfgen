import os

SQS_OUTPUT_QUEUE = os.environ.get('SQS_OUTPUT_QUEUE')
POLL_INTERVAL_SECONDS = int(os.environ.get('POLL_INTERVAL_SECONDS', '1'))

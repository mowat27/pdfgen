import time
from signal import SIGINT, signal

from aws import s3, sqs

from . import POLL_INTERVAL_SECONDS, SQS_OUTPUT_QUEUE


def exit_with_style(signal_received, frame):
    print('\nShutting down...')
    exit(0)


signal(SIGINT, exit_with_style)


def stdout_logger(message):
    for obj in [s3.S3Object.from_sqs_record(record) for record in message.records]:
        log = f"object={obj.s3_url} callback={obj.metadata['callback_url']}"
        print(log)


print('Starting...')
print(f'Polling Interval: {POLL_INTERVAL_SECONDS} second(s)')
sqs.poller.start(queue=SQS_OUTPUT_QUEUE,
                 poll_interval=POLL_INTERVAL_SECONDS,
                 handlers=[stdout_logger])

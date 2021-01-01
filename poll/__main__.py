
import time
from signal import SIGINT, signal

from aws import sqs, s3


from . import POLL_INTERVAL_SECONDS, SQS_OUTPUT_QUEUE


def exit_with_style(signal_received, frame):
    print('\nShutting down...')
    exit(0)


signal(SIGINT, exit_with_style)


def stdout_logger(message):
    for obj in [s3.S3Object.from_sqs_record(record) for record in message.records]:
        log = f"object={obj.s3_url} callback={obj.metadata['Metadata']['callback-url']}"
        print(log)


def start_poller(queue, *, poll_interval=1, handlers=[]):
    while True:
        for message in next(queue).messages():
            for handler in handlers:
                handler(message)
            queue.delete_message(message.receipt_handle)
        time.sleep(poll_interval)


queue = sqs.Queue(SQS_OUTPUT_QUEUE)
print('Starting...')
print(f'Polling Interval: {POLL_INTERVAL_SECONDS} second(s)')
start_poller(queue, poll_interval=POLL_INTERVAL_SECONDS,
             handlers=[stdout_logger])

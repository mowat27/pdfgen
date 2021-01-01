import sys
from signal import SIGINT, signal

import requests
from aws import s3, sqs
from aws.s3.url_signer import create_presigned_url

from . import POLL_INTERVAL_SECONDS, SQS_OUTPUT_QUEUE

ONE_WEEK = 7 * 24 * 60 * 60


def shutdown(signal_received, frame):
    print('\nShutting down...')
    exit(0)


signal(SIGINT, shutdown)


def get_s3_objects(message):
    yield from [
        s3.S3Object.from_sqs_record(record)
        for record in message.records
    ]


def log(message, error=False):
    if error:
        print(message, file=sys.stderr, flush=True)
    else:
        print(message, flush=True)


def send_documents(message):
    for obj in get_s3_objects(message):
        signed_url = create_presigned_url(
            bucket_name=obj.bucket,
            object_name=obj.key,
            expiration=ONE_WEEK)

        callback = obj.metadata['callback_url']

        if signed_url is not None:
            log(f'Notifying {callback}')
            try:
                response = requests.put(callback, data={'url': signed_url})
                if response.status_code == 200:
                    log(f'SUCCESS: Notified {callback}')
                    log(f'  S3 Object: {obj.s3_url}')
                    log(f'  Signed url: {signed_url}')
                elif response.status_code == 404:
                    log(f'{callback} Not Found.', error=True)
                else:
                    log(f'{callback} returned status {response.status_code}', error=True)
            except requests.ConnectionError as e:
                log(f'ERROR: Could not connect ', error=True)
                log(f'ERROR: {e}', error=True)
        else:
            log('Failed to generate signed url', error=True)


print('Starting Notifier...')
print(f'Queue: {SQS_OUTPUT_QUEUE}')
print(f'Polling Interval: {POLL_INTERVAL_SECONDS} second(s)')
sqs.poller.start(queue=SQS_OUTPUT_QUEUE,
                 poll_interval=POLL_INTERVAL_SECONDS,
                 handlers=[send_documents])

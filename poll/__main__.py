import json
import os
import time
from signal import SIGINT, signal

import boto3

from . import POLL_INTERVAL_SECONDS, SQS_OUTPUT_QUEUE

sqs = boto3.client('sqs')
s3 = boto3.client('s3')


def exit_with_style(signal_received, frame):
    print('\nShutting down...')
    exit(0)


signal(SIGINT, exit_with_style)


class S3Object:
    def __init__(self, record):
        self.record = record

    @property
    def bucket(self):
        return self.record["s3"]["bucket"]["name"]

    @property
    def key(self):
        return self.record["s3"]["object"]["key"]

    @property
    def filename(self):
        return os.path.basename(self.key)

    @property
    def prefix(self):
        return os.path.dirname(self.key)

    @property
    def s3_url(self):
        return f's3://{self.bucket}{self.prefix}/{self.filename}'

    @property
    def metadata(self):
        return s3.head_object(Bucket=self.bucket, Key=self.key)


class Response:
    def __init__(self, queue, response):
        self.queue = queue
        self.response = response

    def __iter__(self):
        if 'Messages' in self.response:
            for message in self.response['Messages']:
                yield message


class Queue:
    default_sqs_options = {
        "AttributeNames": [
            'SentTimestamp'
        ],
        "MaxNumberOfMessages": 1,
        "MessageAttributeNames": [
            'All'
        ],
        "VisibilityTimeout": 0,
        "WaitTimeSeconds": 10
    }

    def __init__(self, queue_url, *, handlers=None, sqs_options=None):
        self.queue_url = queue_url
        self.handlers = handlers or []
        self.sqs_options = dict(self.default_sqs_options)  # makes a copy
        self.sqs_options.update(sqs_options or {})

    def add_handler(self, f):
        self.handlers.append(f)

    def __next__(self):
        return sqs.receive_message(QueueUrl=self.queue_url, **self.sqs_options)

    def start_poller(self, *, poll_interval=1, sqs_options=None):
        while True:
            for message in Response(self, next(self)):
                for handler in self.handlers:
                    handler(message)

                sqs.delete_message(
                    QueueUrl=self.queue_url,
                    ReceiptHandle=message['ReceiptHandle'])

            time.sleep(poll_interval)


def stdout_logger(message):
    body = json.loads(message['Body'])

    for obj in [S3Object(record) for record in body['Records']]:
        log = f"object={obj.s3_url} callback={obj.metadata['Metadata']['callback-url']}"
        print(log)


queue = Queue(SQS_OUTPUT_QUEUE)
queue.add_handler(stdout_logger)
queue.start_poller(poll_interval=POLL_INTERVAL_SECONDS)

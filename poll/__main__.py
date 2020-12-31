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

    def __init__(self, queue_url, *, sqs_options=None):
        self.queue_url = queue_url
        self.sqs_options = dict(self.default_sqs_options)  # makes a copy
        self.sqs_options.update(sqs_options or {})

    def __next__(self):
        data = sqs.receive_message(
            QueueUrl=self.queue_url,
            **self.sqs_options)
        return Response(self, data)

    def delete_message(self, receipt_handle):
        sqs.delete_message(QueueUrl=self.queue_url,
                           ReceiptHandle=receipt_handle)


class Response:
    def __init__(self, queue, response):
        self.queue = queue
        self.response = response

    def messages(self):
        if 'Messages' in self.response:
            for message in self.response['Messages']:
                yield Message(self.queue, message)


class Message:
    def __init__(self, queue, message):
        self.queue = queue
        self.message = message

    @ property
    def body(self):
        return json.loads(self.message['Body'])

    @ property
    def records(self):
        for record in self.body['Records']:
            yield record

    @ property
    def receipt_handle(self):
        return self.message['ReceiptHandle']


class S3Object:
    def __init__(self, record):
        self.record = record

    @ property
    def bucket(self):
        return self.record["s3"]["bucket"]["name"]

    @ property
    def key(self):
        return self.record["s3"]["object"]["key"]

    @ property
    def filename(self):
        return os.path.basename(self.key)

    @ property
    def prefix(self):
        return os.path.dirname(self.key)

    @ property
    def s3_url(self):
        return f's3://{self.bucket}{self.prefix}/{self.filename}'

    @ property
    def metadata(self):
        return s3.head_object(Bucket=self.bucket, Key=self.key)


def stdout_logger(message):
    for obj in [S3Object(record) for record in message.records]:
        log = f"object={obj.s3_url} callback={obj.metadata['Metadata']['callback-url']}"
        print(log)


def start_poller(queue, *, poll_interval=1, handlers=[]):
    while True:
        for message in next(queue).messages():
            for handler in handlers:
                handler(message)
            queue.delete_message(message.receipt_handle)
        time.sleep(poll_interval)


queue = Queue(SQS_OUTPUT_QUEUE)
print('Starting...')
print(f'Polling Interval: {POLL_INTERVAL_SECONDS} second(s)')
start_poller(queue, poll_interval=POLL_INTERVAL_SECONDS,
             handlers=[stdout_logger])

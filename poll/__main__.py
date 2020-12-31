import boto3
import json
import time

from signal import signal, SIGINT

from . import SQS_OUTPUT_QUEUE, POLL_INTERVAL_SECONDS

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

    def __init__(self, queue_url, *, handlers=None):
        self.queue_url = queue_url
        self.handlers = handlers or []

    def add_handler(self, f):
        self.handlers.append(f)

    def start_poller(self, *, poll_interval=1, sqs_options=None):
        options = dict(self.default_sqs_options)  # makes a copy
        options.update(sqs_options or {})

        while True:
            response = sqs.receive_message(QueueUrl=self.queue_url, **options)
            if 'Messages' in response:
                for message in response['Messages']:
                    for handler in self.handlers:
                        handler(message)

                sqs.delete_message(
                    QueueUrl=self.queue_url,
                    ReceiptHandle=message['ReceiptHandle'])

            time.sleep(poll_interval)


def stdout_logger(message):
    body = json.loads(message['Body'])

    for record in body['Records']:
        bucket = record["s3"]["bucket"]["name"]
        key = record["s3"]["object"]["key"]

        metadata = s3.head_object(Bucket=bucket, Key=key)
        log = f"object=s3://{bucket}/{key} callback={metadata['Metadata']['callback-url']}"
        print(log)


queue = Queue(SQS_OUTPUT_QUEUE)
queue.add_handler(stdout_logger)
queue.start_poller(poll_interval=POLL_INTERVAL_SECONDS)

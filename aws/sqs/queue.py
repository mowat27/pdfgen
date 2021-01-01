import json

import boto3

sqs = boto3.client('sqs')


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

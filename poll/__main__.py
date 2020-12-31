import boto3
import json
import time

from . import SQS_OUTPUT_QUEUE, POLL_INTERVAL_SECONDS

sqs = boto3.client('sqs')

while True:
    response = sqs.receive_message(
        QueueUrl=SQS_OUTPUT_QUEUE,
        AttributeNames=[
            'SentTimestamp'
        ],
        MaxNumberOfMessages=1,
        MessageAttributeNames=[
            'All'
        ],
        VisibilityTimeout=0,
        WaitTimeSeconds=POLL_INTERVAL_SECONDS
    )

    if 'Messages' in response:
        for message in response['Messages']:
            body = json.loads(message['Body'])

            for record in body['Records']:
                bucket = record["s3"]["bucket"]["name"]
                key = record["s3"]["object"]["key"]
                print(f"s3://{bucket}/{key} was created")

            sqs.delete_message(
                QueueUrl=SQS_OUTPUT_QUEUE,
                ReceiptHandle=message['ReceiptHandle']
            )

    time.sleep(POLL_INTERVAL_SECONDS)

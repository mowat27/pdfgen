import boto3
import json
import time

from . import SQS_OUTPUT_QUEUE, POLL_INTERVAL_SECONDS

sqs = boto3.client('sqs')
s3 = boto3.client('s3')

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
        WaitTimeSeconds=10
    )

    if 'Messages' in response:
        for message in response['Messages']:
            body = json.loads(message['Body'])

            for record in body['Records']:
                bucket = record["s3"]["bucket"]["name"]
                key = record["s3"]["object"]["key"]

                metadata = s3.head_object(Bucket=bucket, Key=key)
                log = f"object=s3://{bucket}/{key} callback={metadata['Metadata']['callback-url']}"
                print(log)

            sqs.delete_message(
                QueueUrl=SQS_OUTPUT_QUEUE,
                ReceiptHandle=message['ReceiptHandle']
            )

    time.sleep(POLL_INTERVAL_SECONDS)

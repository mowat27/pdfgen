import os

import boto3

s3 = boto3.client('s3')


class S3Object:
    @classmethod
    def from_sqs_record(cls, record):
        bucket = record["s3"]["bucket"]["name"]
        key = record["s3"]["object"]["key"]
        return cls(bucket, key)

    def __init__(self, bucket, key):
        self.bucket = bucket
        self.key = key

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

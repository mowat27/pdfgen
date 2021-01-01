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
        response = s3.head_object(Bucket=self.bucket, Key=self.key)
        return Metadata(response)


class Metadata:
    def __init__(self, response):
        self.response = response

    @property
    def values(self):
        return self.response['Metadata']

    @property
    def raw(self):
        return self.response

    def __getitem__(self, key):
        return self.values[key]

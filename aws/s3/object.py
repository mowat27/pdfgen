import os

import boto3

s3 = boto3.client('s3')


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

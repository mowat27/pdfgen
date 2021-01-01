import boto3

from . import S3Object

s3 = boto3.resource('s3')


def save(body, bucket, key, *, metadata=None):
    obj = s3.Object(bucket, key)
    if metadata:
        obj.put(Body=body, Metadata=metadata)
    else:
        obj.put(Body=body)

    return S3Object(bucket, key)

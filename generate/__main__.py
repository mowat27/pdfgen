import pdfkit
import sys
import boto3
import uuid

from . import S3_BUCKET_FOR_OUTPUT
from aws import s3

if len(sys.argv) < 2:
    sys.exit("Please pass source file")

if not S3_BUCKET_FOR_OUTPUT:
    sys.exit("Please set S3_BUCKET_FOR_OUTPUT")

source = sys.argv[1]


def make_pdf(source):
    options = {'enable-local-file-access': None}
    return pdfkit.from_file(source, False, options=options)


def upload_to_s3(pdf, bucket):
    key = f'generated-{uuid.uuid4()}.pdf'
    return s3.save(pdf, bucket, key, metadata={
        "version": "0.1",
        "generated_by": "pdfgen",
        "callback_url": "https://example.com/docid"
    })


if source.startswith("http"):
    sys.exit("Generating pdfs from URLs is not currently supported")
else:
    pdf = make_pdf(source)
    s3_object = upload_to_s3(pdf, S3_BUCKET_FOR_OUTPUT)
    print(f'Created: {s3_object.s3_url}')
    print(f'Metadata: {s3_object.metadata.values}')

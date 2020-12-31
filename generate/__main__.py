import pdfkit
import sys
import boto3
import uuid

from . import S3_BUCKET_FOR_OUTPUT

if len(sys.argv) < 2:
    sys.exit("Please pass source file")

if not S3_BUCKET_FOR_OUTPUT:
    sys.exit("Please set S3_BUCKET_FOR_OUTPUT")

source = sys.argv[1]


def make_pdf(source):
    options = {'enable-local-file-access': None}
    return pdfkit.from_file(source, False, options=options)


def upload_to_s3(pdf, bucket):
    s3 = boto3.resource('s3')
    filename = f'generated-{uuid.uuid4()}.pdf'
    obj = s3.Object(bucket, filename)

    obj.put(Body=pdf, Metadata={
        "metadata-version": "0.1",
        "generated-by": "pdfgen",
        "callback-url": "https://example.com/docid"
    })

    print(f'Created s3://{bucket}/{filename}')
    print("aws s3api head-object --bucket", bucket,  "--key", filename)


if source.startswith("http"):
    sys.exit("Generating pdfs from URLs is not currently supported")
else:
    pdf = make_pdf(source)
    upload_to_s3(pdf, S3_BUCKET_FOR_OUTPUT)

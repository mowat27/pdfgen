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

if source.startswith("http"):
    sys.exit("Generating pdfs from URLs is not currently supported")
else:
    options = {'enable-local-file-access': None}
    pdf = pdfkit.from_file(source, False, options=options)
    s3 = boto3.resource('s3')
    filename = f'generated-{uuid.uuid4()}.pdf'
    obj = s3.Object(S3_BUCKET_FOR_OUTPUT, filename)
    obj.put(Body=pdf)
    print(f'Created s3://{S3_BUCKET_FOR_OUTPUT}/{filename}')

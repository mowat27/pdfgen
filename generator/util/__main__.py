import sys

from .. import pdf
from . import S3_BUCKET_FOR_OUTPUT

if len(sys.argv) < 2:
    sys.exit("Please pass source file")

if not S3_BUCKET_FOR_OUTPUT:
    sys.exit("Please set S3_BUCKET_FOR_OUTPUT")

source = sys.argv[1]

if source.startswith("http"):
    sys.exit("Generating pdfs from URLs is not currently supported")
else:
    body = pdf.make(source)
    s3_object = pdf.upload_to_s3(body, S3_BUCKET_FOR_OUTPUT)
    print(f'Created: {s3_object.s3_url}')
    print(f'Metadata: {s3_object.metadata.values}')

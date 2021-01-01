import uuid

import pdfkit
from aws import s3


def make(source):
    options = {'enable-local-file-access': None}
    return pdfkit.from_file(source, False, options=options)


def upload_to_s3(pdf, bucket):
    key = f'generated-{uuid.uuid4()}.pdf'
    return s3.save(pdf, bucket, key, metadata={
        "version": "0.1",
        "generated_by": "pdfgen",
        "callback_url": "https://example.com/docid"
    })

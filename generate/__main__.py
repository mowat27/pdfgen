import pdfkit
import sys

from . import S3_BUCKET_FOR_OUTPUT

if len(sys.argv) < 3:
    sys.exit("Please pass source and target")

source, target = sys.argv[1:3]

if source.startswith("http"):
    pdfkit.from_url(source, target)
else:
    options = {'enable-local-file-access': None}
    pdf = pdfkit.from_file(source, False, options=options)
    with open(target, 'wb') as f:
        f.write(pdf)

import pdfkit
import sys

if len(sys.argv) < 3:
    sys.exit("Please pass source and target")

source, target = sys.argv[1:3]

if source.startswith("http"):
    pdfkit.from_url(source, target)
else:
    pdfkit.from_file(source, target)

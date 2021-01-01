import json
import time
from signal import SIGINT, signal

import jinja2
from aws import s3, sqs

import pdfkit
from .. import pdf
from . import POLL_INTERVAL_SECONDS, SQS_INPUT_QUEUE, S3_BUCKET_FOR_OUTPUT


def shutdown(signal, frame):
    print('\nShutting down...')
    exit(0)


signal(SIGINT, shutdown)


def maker(message):
    content = json.loads(message.body['document']['content'])
    creator = message.body['generated_by']
    callback = message.body['callback_url']

    with open('./templates/simple.html.j2', 'r') as f:
        template = jinja2.Template(f.read())

    html = template.render(content=content)

    with open('templates/index.html', 'w') as f:
        f.write(html)

    document = pdfkit.from_string(html, False)
    pdf.upload_to_s3(document, S3_BUCKET_FOR_OUTPUT, metadata={
        'creator': creator,
        'callback_url': callback
    })


def logger(message):
    content = json.loads(message.body['document']['content'])
    name = content['name']
    print(f'Making a pdf for {name}', flush=True)


sqs.poller.start(queue=SQS_INPUT_QUEUE,
                 poll_interval=POLL_INTERVAL_SECONDS,
                 handlers=[maker, logger])

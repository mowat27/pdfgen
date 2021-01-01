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


def make_html(template, content):
    with open(template, 'r') as f:
        template = jinja2.Template(f.read())

    return template.render(content=content)


def pdf_from_html(html):
    return pdfkit.from_string(html, False)


def maker(message):
    content = json.loads(message.body['document']['content'])
    html = make_html('./templates/simple.html.j2', content)
    pdf.upload_to_s3(
        document=pdf_from_html(html),
        bucket=S3_BUCKET_FOR_OUTPUT,
        metadata={
            'creator': message.body['generated_by'],
            'callback_url': message.body['callback_url']
        })


def debug_file_maker(message):
    content = json.loads(message.body['document']['content'])
    html = make_html('./templates/simple.html.j2', content)
    with open('templates/index.html', 'w') as f:
        f.write(html)


def logger(message):
    content = json.loads(message.body['document']['content'])
    name = content['name']
    print(f'Making a pdf for {name}', flush=True)


sqs.poller.start(queue=SQS_INPUT_QUEUE,
                 poll_interval=POLL_INTERVAL_SECONDS,
                 handlers=[maker, logger, debug_file_maker])

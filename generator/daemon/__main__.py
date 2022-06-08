import pathlib
import json
import time
import sys
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
    html = make_html('./templates/simple.html.j2',
                     message.body['data']['attributes'])
    pdf.upload_to_s3(
        document=pdf_from_html(html),
        bucket=S3_BUCKET_FOR_OUTPUT,
        metadata={
            'owner': message.body['meta']['owner'],
            'type': message.body['data']['type'],
            'id': str(message.body['data']['id']),
            'version': message.body['data']['attributes']['version'],
            'callback_url': message.body['links']['callback']
        })


def mkdir_p(path):
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)


def debug_file_maker(message):
    html = make_html('./templates/simple.html.j2',
                     message.body['data']['attributes'])
    mkdir_p('./www/debug')
    with open('./www/debug/index.html', 'w') as f:
        f.write(html)


def logger(message):
    name = message.body['data']['attributes']['name']
    version = message.body['data']['attributes']['version']
    print(f'Making a pdf for "{name}" version {version}', flush=True)


sqs.poller.start(queue=SQS_INPUT_QUEUE,
                 poll_interval=POLL_INTERVAL_SECONDS,
                 handlers=[maker, logger, debug_file_maker])

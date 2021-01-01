import json
import time
from signal import SIGINT, signal

from aws import s3, sqs

from . import POLL_INTERVAL_SECONDS, SQS_INPUT_QUEUE
from .. import pdf


def shutdown(signal, frame):
    print('\nShutting down...')
    exit(0)


signal(SIGINT, shutdown)


def maker(message):
    content = json.loads(message.body['document']['content'])

    print(f"Making ({type(content)}) {content}")


def logger(message):
    print(message, flush=True)


sqs.poller.start(queue=SQS_INPUT_QUEUE,
                 poll_interval=POLL_INTERVAL_SECONDS,
                 handlers=[maker, logger])

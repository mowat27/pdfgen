import time
from signal import SIGINT, signal

from aws import s3, sqs

from . import POLL_INTERVAL_SECONDS, SQS_INPUT_QUEUE


def shutdown(signal, frame):
    print('\nShutting down...')
    exit(0)


signal(SIGINT, shutdown)


def logger(message):
    print(message, flush=True)


sqs.poller.start(queue=SQS_INPUT_QUEUE,
                 poll_interval=POLL_INTERVAL_SECONDS,
                 handlers=[logger])

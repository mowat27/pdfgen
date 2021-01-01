import time
from signal import SIGINT, signal

from aws import s3


def shutdown(signal, frame):
    print('\nShutting down...')
    exit(0)


signal(SIGINT, shutdown)

while True:
    print('Tick', flush=True)
    time.sleep(2)

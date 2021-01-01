import time
from signal import SIGINT, signal

from aws import s3


def shutdown(signal_received, frame):
    print('\nShutting down...')
    exit(0)


signal(SIGINT, shutdown)

while True:
    print('Tick')
    time.sleep(2)

import time

from . import Queue


def start(queue, *, poll_interval=1, handlers=[]):
    if isinstance(queue, str):
        queue = Queue(queue)

    while True:
        for message in next(queue).messages():
            for handler in handlers:
                handler(message)
            queue.delete_message(message.receipt_handle)
        time.sleep(poll_interval)

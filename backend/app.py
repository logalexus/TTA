from queue import Queue
from fastapi import FastAPI
from threading import Thread
from packets.sniffer import Sniffer, show_stream

# app = FastAPI()

sniffer = Sniffer()
streams = Queue()

sniffer_thread = Thread(
    target=sniffer.run,
    args=(streams, "enp0s3", 5000)
)
sniffer_thread.start()

while True:
    stream = streams.get()
    show_stream(stream)
    streams.task_done()

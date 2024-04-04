from fastapi import FastAPI

import packets.sniffer as sniffer

app = FastAPI()

sniffer.run(5000)

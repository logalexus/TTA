from asyncio import Queue
import asyncio
import json
from contextlib import asynccontextmanager
from typing import List
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from backend.packets.sniffer import Sniffer


@asynccontextmanager
async def lifespan(app: FastAPI):
    loop = asyncio.get_event_loop()
    loop.create_task(sniffer.run())
    loop.create_task(distribute_streams(
        sniffer.output_stream, active_websockets))
    yield

app = FastAPI(lifespan=lifespan)
active_websockets: List[WebSocket] = []
sniffer = Sniffer("enp0s3", 5000)


@app.websocket("/api/ws")
async def streams_websocket(websocket: WebSocket):
    await websocket.accept()
    active_websockets.append(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            print(data)
    except WebSocketDisconnect:
        active_websockets.remove(websocket)


@app.get("/")
def read_root():
    return {"Hello": "Worl"}


async def distribute_streams(stream_queue: Queue, clients: List[WebSocket]):
    while True:
        stream: Queue = await stream_queue.get()
        stream_json = {
            "type": "NEW_STREAM",
            "data": stream.to_json()
        }
        for client in clients:
            await client.send_text(json.dumps(stream_json))
        stream_queue.task_done()

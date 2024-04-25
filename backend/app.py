import asyncio
import json

from typing import List
from asyncio import Queue
from contextlib import asynccontextmanager
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from backend.network.sniffer import Sniffer
from backend.api.models import Stream
from backend.api.database import SessionLocal, create_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    loop = asyncio.get_event_loop()
    loop.create_task(sniffer.run())
    loop.create_task(distribute_streams(
        sniffer.output_stream, active_websockets))
    yield

create_db()
app = FastAPI(lifespan=lifespan)
active_websockets: List[WebSocket] = []
sniffer = Sniffer("any", 5000)


@app.websocket("/api/ws")
async def streams_websocket(websocket: WebSocket):
    await websocket.accept()
    active_websockets.append(websocket)
    try:
        while True:
            data = await websocket.receive_json()
    except WebSocketDisconnect:
        active_websockets.remove(websocket)


@app.get("/")
def read_root():
    return {"Hello": "World"}


async def distribute_streams(stream_queue: Queue, clients: List[WebSocket]):
    while True:
        stream: Stream = await stream_queue.get()
        with SessionLocal() as db:
            db.add(stream)
            db.refresh(stream)
            stream_json = {
                "type": "NEW_STREAM",
                "data": stream.to_dict
            }
        for client in clients:
            await client.send_text(json.dumps(stream_json))
        stream_queue.task_done()

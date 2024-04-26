import asyncio
import json
import backend.api.repository as repository

from typing import List
from asyncio import Queue
from contextlib import asynccontextmanager
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from backend.network.sniffer import Sniffer
from backend.api.models import Stream
from backend.api.database import SessionLocal, create_db
from fastapi.middleware.cors import CORSMiddleware


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
sniffer = Sniffer("wg0", 5000)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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


@app.get("/api/packets")
async def get_packets(stream_id: int):
    with SessionLocal() as db:
        return repository.get_packets(db, stream_id)
    
@app.get("/api/streams")
async def get_packets():
    with SessionLocal() as db:
        return repository.get_streams(db)


async def distribute_streams(stream_queue: Queue, clients: List[WebSocket]):
    while True:
        with SessionLocal() as db:
            stream: Stream = await stream_queue.get()
            db.add(stream)
            db.refresh(stream)
            stream_json = {
                "type": "NEW_STREAM",
                "data": stream.to_dict
            }
        for client in clients:
            await client.send_text(json.dumps(stream_json))
        stream_queue.task_done()

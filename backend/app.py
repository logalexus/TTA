import asyncio
import json
import backend.api.repository as repository


from typing import List
from asyncio import Queue
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from backend.network.sniffer import Sniffer
from backend.api.models import Pattern, Stream
from backend.api.database import SessionLocal, create_db
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.network.stream_controller import StreamContoller


@asynccontextmanager
async def lifespan(app: FastAPI):
    loop = asyncio.get_event_loop()
    loop.create_task(sniffer.run())
    loop.create_task(stream_controller.distribute_streams(
        sniffer.output_stream, active_websockets))
    yield

create_db()
active_websockets: List[WebSocket] = []
sniffer = Sniffer("enp0s3", 5000)
stream_controller = StreamContoller()

app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class PatternModel(BaseModel):
    name: str
    regex: str
    color: str


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


@app.get("/api/patterns")
async def get_packets():
    with SessionLocal() as db:
        return repository.get_patterns(db)


@app.post("/api/pattern/add")
async def add_pattern(pattern: PatternModel):
    if not pattern.name:
        raise HTTPException(status_code=400, detail="Name cannot be empty")

    if not pattern.regex:
        raise HTTPException(
            status_code=400, detail="Expression cannot be empty")

    if len(pattern.name) > 30:
        raise HTTPException(
            status_code=400, detail="Name cannot be more tham 30 symbols")

    with SessionLocal() as db:
        existing_pattern = repository.get_pattern_by_name(db, pattern.name)
        if existing_pattern:
            raise HTTPException(
                status_code=400, detail="Pattern with this name already exists")

        new_pattern = Pattern(
            name=pattern.name,
            regex=pattern.regex,
            color=pattern.color
        )
        repository.add_pattern(db, new_pattern)


@app.post("/api/pattern/remove")
async def add_pattern(name: str):
    with SessionLocal() as db:
        pattern = repository.get_pattern_by_name(db, name)
        if not pattern:
            raise HTTPException(
                status_code=400, detail="Pattern not exists")

        repository.remove_pattern(db, pattern)

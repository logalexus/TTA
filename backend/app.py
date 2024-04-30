import asyncio
import backend.api.repository as repository

from typing import List
from contextlib import asynccontextmanager
from backend.analyze.analyzer import load_rules
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from backend.network.stream_controller import StreamContoller
from backend.network.sniffer import Sniffer
from backend.api.models import Pattern
from backend.api.database import SessionLocal, create_db
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


@asynccontextmanager
async def lifespan(app: FastAPI):
    
    loop = asyncio.get_event_loop()
    loop.create_task(sniffer.run())
    loop.create_task(stream_controller.distribute_streams(
        sniffer.output_stream, active_websockets))
    yield


def get_current_port():
    with SessionLocal() as db:
        service = repository.get_service(db)
        if service:
            return service.port
        else:
            return None

create_db()
load_rules()
active_websockets: List[WebSocket] = []
stream_controller = StreamContoller()
port = get_current_port()
sniffer = Sniffer("enp0s3", stream_controller, port)

app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://192.168.0.18:8080"],
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


@app.post("/api/db/clear")
def read_root():
    with SessionLocal() as db:
        repository.clear_db(db)


@app.get("/api/packets")
async def get_packets(stream_id: int):
    with SessionLocal() as db:
        packets = repository.get_packets(db, stream_id)
        packets_json = []
        for packet in packets:
            packet_data = {
                "id": packet.id,
                "timestamp": packet.timestamp,
                "incoming": packet.incoming,
                "payload": packet.payload,
                "pattern_match": []
            }
            for match in packet.pattern_match:
                packet_data["pattern_match"].append({
                    "start_match": match.start_match,
                    "end_match": match.end_match,
                    "color": match.pattern.color,
                })
            packets_json.append(packet_data)
        return packets_json


@app.get("/api/streams")
async def get_streams():
    with SessionLocal() as db:
        streams = repository.get_streams(db)
        streams_data = []
        for stream in streams:
            stream_data = stream.to_dict()
            stream_data["suspicious"] = []
            for name, color in repository.get_patterns_by_stream(db, stream.id):
                stream_data["suspicious"].append({
                    "name": name,
                    "color": color,
                })
            streams_data.append(stream_data)
        return streams_data


@app.get("/api/patterns")
async def get_patterns():
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
async def remove_pattern(name: str):
    with SessionLocal() as db:
        pattern = repository.get_pattern_by_name(db, name)
        if not pattern:
            raise HTTPException(
                status_code=400, detail="Pattern not exists")

        repository.remove_pattern(db, pattern)


@app.post("/api/port/select")
async def select_port(port: int):
    with SessionLocal() as db:
        if port < 0 or port > 65536:
            raise HTTPException(
                status_code=400, detail="Bad port")

        repository.change_service_port(db, port)
        sniffer.target_port = port


@app.get("/api/port")
async def get_port():
    return get_current_port()

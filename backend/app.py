from queue import Queue
from fastapi import APIRouter, FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from backend.packets.stream import Stream
from backend.packets.sniffer import Sniffer

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
router = APIRouter(prefix="/api")

sniffer = Sniffer("enp0s3", 5000)
sniffer.run()


@app.websocket("/api/ws")
async def streams_websocket(websocket: WebSocket):
    await websocket.accept()
    while True:
        stream: Stream = sniffer.output_streams.get()
        await websocket.send_text(stream.to_json())
        sniffer.output_streams.task_done()


@app.get("/")
def read_root():
    return {"Hello": "World"}


app.include_router(router)

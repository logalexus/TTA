from queue import Queue
from fastapi import FastAPI, WebSocket
from backend.packets.stream import Stream
from backend.packets.sniffer import Sniffer

app = FastAPI()

sniffer = Sniffer("eth0", 5000)
sniffer.run()

# while True:
#     stream: Stream = sniffer.output_streams.get()
#     # stream.show()
#     # print(stream.to_json())
#     sniffer.output_streams.task_done()


@app.websocket("/ws")
async def streams_websocket(websocket: WebSocket):
    await websocket.accept()
    while True:
        stream: Stream = sniffer.output_streams.get()
        await websocket.send_text(stream.to_json())
        sniffer.output_streams.task_done()
        
@app.get("/")
def read_root():
    return {"Hello": "World"}

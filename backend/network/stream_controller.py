import json
import backend.analyze.analyzer as analyzer
import backend.api.repository as repository

from typing import List
from asyncio import Queue
from fastapi import WebSocket
from backend.api.models import Stream
from backend.api.database import SessionLocal
from backend.network.dirty_stream import DirtyStream


class StreamContoller():
    async def distribute_streams(self, stream_queue: Queue, clients: List[WebSocket]):
        while True:
            try:
                with SessionLocal() as db:
                    stream: Stream = await stream_queue.get()
                    analyzer.search_pattern(stream)
                    db.add(stream)
                    db.refresh(stream)
                    stream_data = stream.to_dict()
                    stream_data["suspicious"] = []
                    for name, color in repository.get_patterns_by_stream(db, stream.id):
                        stream_data["suspicious"].append({
                            "name": name,
                            "color": color,
                        })

                    stream_json = {
                        "type": "NEW_STREAM",
                        "data": stream_data
                    }
                for client in clients:
                    await client.send_text(json.dumps(stream_json))
                stream_queue.task_done()
            except Exception as e:
                print(e)

    async def save_stream(self, dirty_stream: DirtyStream) -> Stream:
       
        
        stream = Stream(
            ipsrc=dirty_stream.flow.ipsrc,
            ipdst=dirty_stream.flow.ipdst,
            portsrc=dirty_stream.flow.portsrc,
            portdst=dirty_stream.flow.portdst,
            start_timestamp=dirty_stream.packets[0].timestamp,
            end_timestamp=dirty_stream.packets[-1].timestamp,
        )

        with SessionLocal() as db:
            stream = repository.add_stream(db, stream)

            for packet in dirty_stream.packets:
                if packet.payload:
                    if packet.protocol == "HTTP":
                        stream.protocol = "HTTP"
                    packet.stream_id = stream.id
                    repository.add_packet(db, packet)
                    
            preview = str(stream.packet[0].payload).split("\r\n")[0]
            stream.preview = preview
            db.commit()

        return stream

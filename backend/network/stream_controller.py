import json
import backend.analyze.analyzer as analyzer

from typing import List
from asyncio import Queue
from fastapi import WebSocket
from backend.api.models import Stream
from backend.api.database import SessionLocal


class StreamContoller():
    async def distribute_streams(self, stream_queue: Queue, clients: List[WebSocket]):
        while True:
            with SessionLocal() as db:
                stream: Stream = await stream_queue.get()
                analyzer.search_pattern(stream)
                db.add(stream)
                db.refresh(stream)
                stream_json = {
                    "type": "NEW_STREAM",
                    "data": stream
                }
            for client in clients:
                await client.send_text(json.dumps(stream_json))
            stream_queue.task_done()

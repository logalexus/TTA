from typing import Dict, List
from backend.api.models import Packet
from backend.network.flow import Flow
from datetime import datetime


class DirtyStream():
    def __init__(self, id: int, flow: Flow):
        self.id = id
        self.flow: Flow = flow
        self.packets: List[Packet] = []
        self.creation_time = datetime.now()

    def show(self) -> None:
        for pkt in self.packets:
            if "tcp.payload" in pkt.tcp._all_fields:
                data = pkt.tcp.payload
                data = bytes.fromhex(data.replace(":", ""))
                data = data.decode(errors="ignore")
                print(data)


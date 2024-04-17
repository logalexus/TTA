import json
from backend.packets.flow import Flow
from datetime import datetime


class Stream():
    def __init__(self, flow: Flow):
        self.flow: Flow = flow
        self.packets = []
        self.creation_time = datetime.now()

    def show(self) -> None:
        for pkt in self.packets:
            if "tcp.payload" in pkt.tcp._all_fields:
                data = pkt.tcp.payload
                data = bytes.fromhex(data.replace(":", ""))
                data = data.decode(errors="ignore")
                print(data)

    def to_json(self) -> str:
        data = {}
        data["packets"] = []
        for pkt in self.packets:
            if "tcp.payload" in pkt.tcp._all_fields:
                raw_data = pkt.tcp.payload
                raw_data = bytes.fromhex(raw_data.replace(":", ""))
                raw_data = raw_data.decode(errors="ignore")
                data["packets"].append(raw_data)
        return json.dumps(data)

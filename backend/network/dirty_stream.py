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

    def to_dict(self) -> Dict[str, any]:
        stream_info = {}
        stream_info["id"] = self.id
        stream_info["ipsrc"] = self.flow.ipsrc
        stream_info["ipdst"] = self.flow.ipdst
        stream_info["portsrc"] = self.flow.portsrc
        stream_info["portdst"] = self.flow.portdst
        stream_info["start_timestamp"] = self.packets[0].timestamp
        stream_info["end_timestamp"] = self.packets[-1].timestamp
        stream_info["protocol"] = "TCP"
        stream_info["packets"] = []
        for pkt in self.packets:
            if pkt.payload != None:
                packet_info = {}
                if pkt.protocol == "HTTP":
                    stream_info["protocol"] = "HTTP"
                    if hasattr(pkt.raw.http, "request"):
                        packet_info["type"] = "request"
                    else:
                        packet_info["type"] = "response"
                        stream_info["status"] = pkt.raw.http.response_code
                packet_info["id"] = pkt.id
                packet_info["payload"] = pkt.payload
                packet_info["ipsrc"] = pkt.ipsrc
                packet_info["ipdst"] = pkt.ipdst
                packet_info["portsrc"] = pkt.portsrc
                packet_info["portdst"] = pkt.portdst
                packet_info["timestamp"] = pkt.timestamp
                packet_info["protocol"] = pkt.protocol
                stream_info["packets"].append(packet_info)
        return stream_info

from typing import Dict
from pyshark.tshark.tshark import get_tshark_interfaces
from packets.flow import Flow
from packets.stream import Stream
from queue import Queue

import pyshark


class Sniffer():
    def __init__(self) -> None:
        self.streams: Dict[Flow, Stream] = {}
        self.completedStreams: Queue = None

    def assembly_streams(self, pkt, target_port: int):
        ip = pkt.ip
        tcp = pkt.tcp
        flow = Flow(ip.src, ip.dst, int(tcp.srcport), int(tcp.dstport))

        if flow.portdst == target_port or flow.portsrc == target_port:
            if flow in self.streams:
                stream = self.streams[flow]
                stream.packets.append(pkt)
                if tcp.flags_fin == "1" and tcp.flags_ack == "1":
                    self.streams.pop(flow)
                    completedStreams.put(stream)
            elif tcp.flags_syn == "1":
                stream = Stream(flow)
                stream.packets.append(pkt)
                self.streams[flow] = stream

    def run(self, streams: Queue, interface: str, port: int):
        global completedStreams
        completedStreams = streams
        cap = pyshark.LiveCapture(interface=interface,
                                  display_filter='tcp.port == 5000')
        cap.set_debug()

        for pkt in cap.sniff_continuously():
            self.assembly_streams(pkt, target_port=port)


def show_stream(stream: Stream):
    for pkt in stream.packets:
        if "tcp.payload" in pkt.tcp._all_fields:
            data = pkt.tcp.payload
            data = bytes.fromhex(data.replace(":", ""))
            data = data.decode(errors="ignore")
            print(data)

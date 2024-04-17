from threading import Thread
from typing import Dict
from pyshark.tshark.tshark import get_tshark_interfaces
from backend.packets.flow import Flow
from backend.packets.stream import Stream
from asyncio import Queue

import pyshark


class Sniffer():
    def __init__(self, interface: str, port: int) -> None:
        self.streams: Dict[Flow, Stream] = {}
        self.output_streams = Queue()
        self.interface = interface
        self.target_port = port

    def run(self):
        sniffer_thread = Thread(
            target=self.__run,
            args=(self.output_streams, self.interface, self.target_port)
        )
        sniffer_thread.start()

    
    
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

    def __run(self, streams: Queue, interface: str, port: int):
        global completedStreams
        completedStreams = streams
        cap = pyshark.LiveCapture(interface=interface,
                                  display_filter='tcp.port == 5000')
        cap.set_debug()

        for pkt in cap.sniff_continuously():
            self.assembly_streams(pkt, target_port=port)



from typing import Dict
from backend.api.models import Packet
from backend.network.async_capture import AsyncLiveCapture
from backend.network.flow import Flow
from backend.network.dirty_stream import DirtyStream
from asyncio import Queue
from urllib.parse import unquote, unquote_plus
from backend.network.stream_controller import StreamContoller

import netifaces


class Sniffer():
    def __init__(self, interface: str, stream_controller: StreamContoller, port: int = None) -> None:
        self.dirty_streams: Dict[Flow, DirtyStream] = {}
        self.interface = interface
        self.target_port = port
        self.output_stream = Queue()
        self.packet_counter = 0
        self.stream_counter = 0
        self.stream_controller = stream_controller
        self.local_ip = self.get_ip_address(self.interface)

    def get_ip_address(self, interface):
        try:
            addresses = netifaces.ifaddresses(interface)
            ip = addresses[netifaces.AF_INET][0]['addr']
            return ip
        except (KeyError, ValueError):
            return None

    async def assembly_streams(self, pkt: Packet, raw_packet: any,  target_port: int):
        flow = Flow(pkt.ipsrc, pkt.ipdst, int(pkt.portsrc), int(pkt.portdst))

        if flow.portdst == target_port or flow.portsrc == target_port:
            if flow in self.dirty_streams:
                dirty_stream = self.dirty_streams[flow]
                dirty_stream.packets.append(pkt)
                if raw_packet.tcp.flags_fin == "1" and raw_packet.tcp.flags_ack == "1":
                    self.dirty_streams.pop(flow)
                    stream = await self.stream_controller.save_stream(dirty_stream)
                    await self.output_stream.put(stream)
            elif raw_packet.tcp.flags_syn == "1":
                dirty_stream = DirtyStream(self.stream_counter, flow)
                dirty_stream.packets.append(pkt)
                self.dirty_streams[flow] = dirty_stream

    def handle_packet(self, raw_packet) -> Packet:
        packet = Packet(
            ipsrc=raw_packet.ip.src,
            ipdst=raw_packet.ip.dst,
            portsrc=int(raw_packet.tcp.srcport),
            portdst=int(raw_packet.tcp.dstport),
            timestamp=int(float(raw_packet.sniff_timestamp)),
        )

        packet.incoming = self.local_ip == packet.ipdst

        if "tcp.payload" in raw_packet.tcp._all_fields:
            if hasattr(raw_packet, "http"):
                packet.protocol = "HTTP"
            payload = raw_packet.tcp.payload
            payload = bytes.fromhex(payload.replace(":", ""))
            payload = payload.decode(errors="ignore")
            payload = unquote(payload)
            payload = unquote_plus(payload)
            packet.payload = payload

        return packet

    async def run(self):
        cap = AsyncLiveCapture(interface=self.interface,
                               display_filter='tcp')
        cap.set_debug()

        async for raw_packet in cap.sniff_continuously():
            if self.target_port:
                packet = self.handle_packet(raw_packet)
                await self.assembly_streams(packet, raw_packet, target_port=self.target_port)

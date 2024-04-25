from typing import Dict
from backend.api.database import SessionLocal
from backend.api.models import Packet, Stream
from backend.network.async_capture import AsyncLiveCapture
from backend.network.flow import Flow
from backend.network.dirty_stream import DirtyStream
from asyncio import Queue

import backend.api.repository as repository


class Sniffer():
    def __init__(self, interface: str, port: int) -> None:
        self.dirty_streams: Dict[Flow, DirtyStream] = {}
        self.interface = interface
        self.target_port = port
        self.output_stream = Queue()
        self.packet_counter = 0
        self.stream_counter = 0

    async def assembly_streams(self, pkt: Packet, raw_packet: any,  target_port: int):
        flow = Flow(pkt.ipsrc, pkt.ipdst, int(pkt.portsrc), int(pkt.portdst))

        if flow.portdst == target_port or flow.portsrc == target_port:
            if flow in self.dirty_streams:
                dirty_stream = self.dirty_streams[flow]
                dirty_stream.packets.append(pkt)
                if raw_packet.tcp.flags_fin == "1" and raw_packet.tcp.flags_ack == "1":
                    self.dirty_streams.pop(flow)
                    stream = await self.save_stream(dirty_stream)
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

        if "tcp.payload" in raw_packet.tcp._all_fields:
            if hasattr(raw_packet, "http"):
                packet.protocol = "HTTP"
            payload = raw_packet.tcp.payload
            payload = bytes.fromhex(payload.replace(":", ""))
            payload = payload.decode(errors="ignore")
            packet.payload = payload

        return packet

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
                if packet.protocol == "HTTP":
                    stream.protocol = "HTTP"
                    db.commit(stream)
                packet.stream_id = stream.id
                repository.add_packet(db, packet)

        return stream

    async def run(self):
        cap = AsyncLiveCapture(interface=self.interface,
                               display_filter='tcp')
        cap.set_debug()

        async for raw_packet in cap.sniff_continuously():
            packet = self.handle_packet(raw_packet)
            await self.assembly_streams(packet, raw_packet, target_port=self.target_port)

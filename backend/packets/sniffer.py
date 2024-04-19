from threading import Thread
from typing import Dict
from backend.packets.flow import Flow
from backend.packets.stream import Stream
from asyncio import Queue

import pyshark


class AsyncLiveCapture(pyshark.LiveCapture):
    async def sniff_continuously(self, packet_count=None):
        tshark_process = await self._get_tshark_process()
        packets_captured = 0
        parser = self._setup_tshark_output_parser()

        data = b''
        try:
            while True:
                try:
                    packet, data = await parser.get_packets_from_stream(tshark_process.stdout, data,
                                                                        got_first_packet=packets_captured > 0)
                except EOFError:
                    self._log.debug('EOF reached (sync)')
                    self._eof_reached = True
                    break

                if packet:
                    packets_captured += 1
                    yield packet
                if packet_count and packets_captured >= packet_count:
                    break
        finally:
            if tshark_process in self._running_processes:
                await self._cleanup_subprocess(tshark_process)


class Sniffer():
    def __init__(self, interface: str, port: int) -> None:
        self.streams: Dict[Flow, Stream] = {}
        self.interface = interface
        self.target_port = port
        self.output_stream = Queue()

    async def assembly_streams(self, pkt, target_port: int):
        ip = pkt.ip
        tcp = pkt.tcp
        flow = Flow(ip.src, ip.dst, int(tcp.srcport), int(tcp.dstport))

        if flow.portdst == target_port or flow.portsrc == target_port:
            if flow in self.streams:
                stream = self.streams[flow]
                stream.packets.append(pkt)
                if tcp.flags_fin == "1" and tcp.flags_ack == "1":
                    self.streams.pop(flow)
                    await self.output_stream.put(stream)
            elif tcp.flags_syn == "1":
                stream = Stream(flow)
                stream.packets.append(pkt)
                self.streams[flow] = stream

    async def run(self):
        cap = AsyncLiveCapture(interface=self.interface,
                               display_filter='tcp.port == 5000')
        cap.set_debug()

        async for pkt in cap.sniff_continuously():
            await self.assembly_streams(pkt, target_port=self.target_port)

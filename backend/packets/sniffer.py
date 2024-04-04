from pyshark.tshark.tshark import get_tshark_interfaces
from packets.flow import Flow
from packets.stream import Stream

import pyshark


streams = {}


def assembly_streams(pkt, target_port: int):
    ip = pkt.ip
    tcp = pkt.tcp
    flow = Flow(ip.src, ip.dst, int(tcp.srcport), int(tcp.dstport))

    if flow.portdst == target_port or flow.portsrc == target_port:
        if flow in streams:
            stream = streams[flow]
            stream.packets.append(pkt)
            if tcp.flags_fin == "1" and tcp.flags_ack == "1":
                show_stream(stream)
                streams.pop(flow)
        elif tcp.flags_syn == "1":
            stream = Stream(flow)
            stream.packets.append(pkt)
            streams[flow] = stream


def show_stream(stream: Stream):
    for pkt in stream.packets:
        if "tcp.payload" in pkt.tcp._all_fields:
            data = pkt.tcp.payload
            data = bytes.fromhex(data.replace(":", ""))
            data = data.decode(errors="ignore")
            print(data)


def run(port: int):
    print(get_tshark_interfaces())
    interface = "eth0"
    cap = pyshark.LiveCapture(interface=interface,
                              display_filter='tcp.port == 5000')
    cap.set_debug()

    for pkt in cap.sniff_continuously():
        assembly_streams(pkt, target_port=port)

import pyshark
from pyshark.tshark.tshark import get_tshark_interfaces


def assembly_streams(packets):
    streams = {}
    for pkt in packets:
        ip = pkt.ip
        tcp = pkt.tcp
        flow = (ip.src, ip.dst, tcp.srcport, tcp.dstport)
        if pkt.tcp.stream not in streams:
            streams[pkt.tcp.stream] = []
            streams[pkt.tcp.stream].append(pkt)
    return streams


def show_streams(streams):
    for stream in list(streams.values()):
        for pkt in stream:
            if "http" in pkt.tcp._all_fields:
                data = stream.tcp.payload
                data = bytes.fromhex(data.replace(":", ""))
                data = data.decode(errors="ignore")
                print(data)


# pkts = pyshark.FileCapture("./dump.pcap", use_json=False)
interface = get_tshark_interfaces()[4]
cap = pyshark.LiveCapture(interface=interface, display_filter="http")
live = cap.sniff_continuously()

print(interface)


PKT_COUNT = 50

while True:
    packets = [next(live) for _ in range(PKT_COUNT)]
    streams = assembly_streams(packets)
    show_streams(streams)

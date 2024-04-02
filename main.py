import pyshark

from datetime import datetime
from pyshark.tshark.tshark import get_tshark_interfaces

streams = {}


class Flow():
    def __init__(self, ipsrc: str, ipdst: str, portsrc: int, portdst: int) -> None:
        self.ipsrc = ipsrc
        self.ipdst = ipdst
        self.portsrc = portsrc
        self.portdst = portdst

    def __hash__(self) -> int:
        PRIME = 59
        result = self.ipsrc.__hash__() * self.ipdst.__hash__()
        result = result * PRIME + (self.portsrc * self.portdst)
        return result

    def __eq__(self, other):
        ipeq1 = self.ipsrc == other.ipsrc and self.ipdst == other.ipdst
        ipeq2 = self.ipsrc == other.ipdst and self.ipdst == other.ipsrc
        porteq1 = self.portsrc == other.portsrc and self.portdst == other.portdst
        porteq2 = self.portsrc == other.portdst and self.portdst == other.portsrc
        return (ipeq1 or ipeq2) and (porteq1 or porteq2)


class Stream():
    def __init__(self, flow: Flow):
        self.flow: Flow = flow
        self.packets = []
        self.creation_time = datetime.now()


def assembly_streams(pkt, target_port: int):
    ip = pkt.ip
    tcp = pkt.tcp
    flow = Flow(ip.src, ip.dst, int(tcp.srcport), int(tcp.dstport))

    if flow.portdst == target_port or flow.portsrc == target_port:
        if flow in streams:
            stream = streams[flow]
            stream.packets.append(pkt)
            if tcp.flags_fin == "1" and tcp.flags_ack == "1":
                # show_stream(stream)
                print(stream)
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


# pkts = pyshark.FileCapture("./dump.pcap", use_json=False)
# interface = get_tshark_interfaces()[4]
print(get_tshark_interfaces())
interface = "eth0"
cap = pyshark.LiveCapture(interface=interface,
                          display_filter='tcp.port == 5000')
cap.set_debug()
live = cap.sniff_continuously()

print(interface)

PKT_COUNT = 100

for pkt in live:
    assembly_streams(pkt, target_port=5000)

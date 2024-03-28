import pyshark
from pyshark.tshark.tshark import get_tshark_interfaces


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


def assembly_streams(packets, target_port: int):
    streams = {}
    for pkt in packets:
        ip = pkt.ip
        tcp = pkt.tcp
        flow = Flow(ip.src, ip.dst, int(tcp.srcport), int(tcp.dstport))
        if flow.portdst == target_port or flow.portsrc == target_port:
            if flow not in streams:
                streams[flow] = []
            streams[flow].append(pkt)
    return streams


def show_streams(streams):
    for stream in streams.values():
        for pkt in stream:
            if "tcp.payload" in pkt.tcp._all_fields:
                data = pkt.tcp.payload
                data = bytes.fromhex(data.replace(":", ""))
                data = data.decode(errors="ignore")
                print(data)


# pkts = pyshark.FileCapture("./dump.pcap", use_json=False)
# interface = get_tshark_interfaces()[4]
print(get_tshark_interfaces())
interface = "enp0s3"
cap = pyshark.LiveCapture(
    interface=interface, display_filter='tcp.port == 5000')
cap.set_debug()
live = cap.sniff_continuously()

print(interface)

PKT_COUNT = 100

while True:
    packets = [next(live) for _ in range(PKT_COUNT)]
    streams = assembly_streams(packets, target_port=5000)
    show_streams(streams)

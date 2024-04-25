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

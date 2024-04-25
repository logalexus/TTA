from backend.packets.stream import Stream


def handle_stream(stream: Stream):
    packet = stream.packets[0]
    
    if packet.
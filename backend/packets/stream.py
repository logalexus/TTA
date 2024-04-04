from packets.flow import Flow
from datetime import datetime

class Stream():
    def __init__(self, flow: Flow):
        self.flow: Flow = flow
        self.packets = []
        self.creation_time = datetime.now()
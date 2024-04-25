from typing import Dict
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from backend.api.database import Base


class Packet(Base):
    __tablename__ = "packet"

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    ipsrc = Column(String)
    ipdst = Column(String)
    portsrc = Column(Integer)
    portdst = Column(Integer)
    timestamp = Column(Integer)
    payload = Column(String, nullable=True)
    protocol = Column(String, default="TCP")
    stream_id = Column(Integer, ForeignKey('stream.id'))

    stream = relationship("Stream", back_populates="packet")


class Stream(Base):
    __tablename__ = "stream"

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    ipsrc = Column(String)
    ipdst = Column(String)
    portsrc = Column(Integer)
    portdst = Column(Integer)
    start_timestamp = Column(Integer)
    end_timestamp = Column(Integer)
    protocol = Column(String, default="TCP")

    packet = relationship("Packet", back_populates="stream")
    
    @property
    def to_dict(self) -> Dict[str, any]:
        stream_info = {}
        stream_info["id"] = self.id
        stream_info["ipsrc"] = self.ipsrc
        stream_info["ipdst"] = self.ipdst
        stream_info["portsrc"] = self.portsrc
        stream_info["portdst"] = self.portdst
        stream_info["start_timestamp"] = self.start_timestamp
        stream_info["end_timestamp"] = self.end_timestamp
        stream_info["protocol"] = self.protocol
        return stream_info

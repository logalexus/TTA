from typing import Dict
from sqlalchemy import Column, String, Integer, Boolean
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
    incoming = Column(Boolean)
    payload = Column(String, nullable=True)
    protocol = Column(String, default="TCP")
    stream_id = Column(Integer, ForeignKey('stream.id'))

    stream = relationship("Stream", back_populates="packet")
    pattern_match = relationship("PatternMatch", back_populates="packet")


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


class PatternMatch(Base):
    __tablename__ = "pattern_match"

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    pattern_id = Column(Integer, ForeignKey('pattern.id'))
    packet_id = Column(Integer, ForeignKey('packet.id'))
    start_match = Column(Integer)
    end_match = Column(Integer)
    
    pattern = relationship("Pattern", back_populates="pattern_match")
    packet = relationship("Packet", back_populates="pattern_match")


class Pattern(Base):
    __tablename__ = "pattern"

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    name = Column(String)
    regex = Column(String)
    color = Column(String)
    active = Column(Boolean)
    
    pattern_match = relationship("PatternMatch", back_populates="pattern")

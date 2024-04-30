import datetime
import json
from typing import Dict
from uuid import UUID
from sqlalchemy import Column, String, Integer, Boolean
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from backend.api.database import Base

from sqlalchemy.ext.declarative import DeclarativeMeta


class OutputMixin(object):
    RELATIONSHIPS_TO_DICT = False

    def __iter__(self):
        return self.to_dict().iteritems()

    def to_dict(self, rel=None, backref=None):
        if rel is None:
            rel = self.RELATIONSHIPS_TO_DICT
        res = {column.key: getattr(self, attr)
               for attr, column in self.__mapper__.c.items()}
        if rel:
            for attr, relation in self.__mapper__.relationships.items():
                # Avoid recursive loop between to tables.
                if backref == relation.table:
                    continue
                value = getattr(self, attr)
                if value is None:
                    res[relation.key] = None
                elif isinstance(value.__class__, DeclarativeMeta):
                    res[relation.key] = value.to_dict(backref=self.__table__)
                else:
                    res[relation.key] = [i.to_dict(backref=self.__table__)
                                         for i in value]
        return res

    def to_json(self, rel=None):
        def extended_encoder(x):
            if isinstance(x, datetime):
                return x.isoformat()
            if isinstance(x, UUID):
                return str(x)
        if rel is None:
            rel = self.RELATIONSHIPS_TO_DICT
        return json.dumps(self.to_dict(rel), default=extended_encoder)


class Packet(OutputMixin, Base):
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


class Stream(OutputMixin, Base):
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


class PatternMatch(OutputMixin, Base):
    __tablename__ = "pattern_match"

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    pattern_id = Column(Integer, ForeignKey('pattern.id'))
    packet_id = Column(Integer, ForeignKey('packet.id'))
    start_match = Column(Integer)
    end_match = Column(Integer)

    pattern = relationship("Pattern", back_populates="pattern_match")
    packet = relationship("Packet", back_populates="pattern_match")


class Pattern(OutputMixin, Base):
    __tablename__ = "pattern"

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    name = Column(String)
    regex = Column(String)
    color = Column(String)
    active = Column(Boolean)

    pattern_match = relationship("PatternMatch", back_populates="pattern")


class Service(OutputMixin, Base):
    __tablename__ = "service"

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    port = Column(String)

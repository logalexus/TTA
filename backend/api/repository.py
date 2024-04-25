from typing import List
from sqlalchemy.orm import Session, joinedload
from backend.api.models import Packet, Stream


def add_stream(db: Session, stream: Stream):
    db.add(stream)
    db.commit()
    db.refresh(stream)
    return stream


def add_packet(db: Session, packet: Packet):
    db.add(packet)
    db.commit()
    db.refresh(packet)
    return packet


def get_stream_by_id(db: Session, stream_id: int) -> Stream:
    return db.query(Stream).filter(Stream.id == stream_id).first()

from typing import List
from sqlalchemy.orm import Session, joinedload
from backend.api.models import Packet, Pattern, Stream


def add_stream(db: Session, stream: Stream) -> Stream:
    db.add(stream)
    db.commit()
    db.refresh(stream)
    return stream


def add_packet(db: Session, packet: Packet) -> Packet:
    db.add(packet)
    db.commit()
    db.refresh(packet)
    return packet


def add_pattern(db: Session, pattern: Pattern) -> Pattern:
    db.add(pattern)
    db.commit()
    db.refresh(pattern)
    return pattern


def get_pattern_by_name(db: Session, name: str) -> Pattern:
    return db.query(Pattern).filter(Pattern.name == name).first()


def remove_pattern(db: Session, pattern: Pattern) -> None:
    db.delete(pattern)
    db.commit()


def get_streams(db: Session) -> Stream:
    return db.query(Stream).all()


def get_stream_by_id(db: Session, stream_id: int) -> Stream:
    return db.query(Stream).filter(Stream.id == stream_id).first()


def get_packets(db: Session, stream_id: int) -> List[Packet]:
    stream = get_stream_by_id(db, stream_id)
    return stream.packet


def get_patterns(db: Session) -> List[Pattern]:
    return db.query(Pattern).all()

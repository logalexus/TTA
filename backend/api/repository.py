from typing import List, Tuple, Union
from sqlalchemy.orm import Session, joinedload
from backend.api.models import Packet, Pattern, PatternMatch, Service, Stream


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


def add_pattern_match(db: Session, pattern_match: PatternMatch) -> PatternMatch:
    db.add(pattern_match)
    db.commit()
    db.refresh(pattern_match)
    return pattern_match


def add_pattern(db: Session, pattern: Pattern) -> Pattern:
    db.add(pattern)
    db.commit()
    db.refresh(pattern)
    return pattern


def add_service(db: Session, service: Service) -> Service:
    db.add(service)
    db.commit()
    db.refresh(service)
    return service


def change_service_port(db: Session, port: int) -> None:
    service = get_service(db)
    if not service:
        service = Service(port=port)
        add_service(db, service)
    else:
        service.port = port
        db.commit()


def get_service(db: Session) -> Service:
    return db.query(Service).first()


def get_pattern_by_name(db: Session, name: str) -> Pattern:
    return db.query(Pattern).filter(Pattern.name == name).first()


def remove_pattern(db: Session, pattern: Pattern) -> None:
    db.delete(pattern)
    db.commit()


def get_streams(db: Session) -> List[Stream]:
    service = get_service(db)
    if service:
        return db.query(Stream).filter(Stream.portsrc == service.port or Stream.portdst == service.port).all()
    else:
        return []


def get_patterns_by_stream(db: Session, stream_id: int) -> List[Tuple[str, str]]:
    return (
        db.query(Pattern.name, Pattern.color)
        .join(PatternMatch, Pattern.id == PatternMatch.pattern_id)
        .join(Packet, Packet.id == PatternMatch.packet_id)
        .join(Stream, Stream.id == Packet.stream_id)
        .filter(Stream.id == stream_id)
        .distinct(Pattern.name, Pattern.color)
        .all()
    )


def get_stream_by_id(db: Session, stream_id: int) -> Stream:
    return db.query(Stream).filter(Stream.id == stream_id).first()


def get_packets(db: Session, stream_id: int) -> List[Packet]:
    stream = get_stream_by_id(db, stream_id)
    return stream.packet


def get_patterns(db: Session) -> List[Pattern]:
    return db.query(Pattern).all()


def clear_db(db: Session) -> None:
    db.query(Packet).delete()
    db.query(Stream).delete()
    db.query(PatternMatch).delete()
    db.commit()
    
def count_patterns(db: Session) -> int:
    return db.query(Pattern).count()

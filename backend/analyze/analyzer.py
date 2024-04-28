import re
import backend.api.repository as repository

from typing import List
from backend.api.database import SessionLocal
from backend.api.models import Packet, PatternMatch, Stream


def search_pattern(stream: Stream):
    with SessionLocal() as db:
        db.add(stream)
        db.refresh(stream)
        packets: List[Packet] = stream.packet
        patterns = repository.get_patterns(db)

        for pattern in patterns:
            pattern_compiled = re.compile(pattern.regex)
            for packet in packets:
                matches = re.finditer(pattern_compiled, packet.payload)
                for match in matches:
                    new_match = PatternMatch()
                    new_match.packet_id = packet.id
                    new_match.start_match = match.start()
                    new_match.end_match = match.end()
                    new_match.pattern_id = pattern.id
                    print(match.group())

        db.expunge(stream)

import json
import re
import backend.api.repository as repository

from typing import List
from backend.api.database import SessionLocal
from backend.api.models import Packet, Pattern, PatternMatch, Stream
import random


def random_color():
    color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
    return color


def load_rules():
    with open("backend/rules.json", "r") as file:
        rules = dict(json.loads(file.read()))
        with SessionLocal() as db:
            if not repository.count_patterns(db) > 0:
                for name, regex in rules.items():
                    pattern = Pattern()
                    pattern.name = name
                    pattern.regex = regex
                    pattern.color = random_color()

                    repository.add_pattern(db, pattern)


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
                    repository.add_pattern_match(db, new_match)

        db.expunge(stream)

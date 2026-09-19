"""Tiny dependency-free random-data helpers.

Reproduces the seeded LCG of the reference implementation (JS) with its exact
float64 arithmetic and bitwise masking semantics, so both apps generate
compatible sequences.
"""

from __future__ import annotations

import math
from datetime import datetime, timedelta, timezone
from typing import Any, Sequence

_seed = 1337
_id_counter = 1_000_000


def _next() -> float:
    global _seed

    # JS: seed = (seed * 1103515245 + 12345) & 0x7fffffff
    # JS multiplies in float64 and the bitwise AND truncates modulo 2^32 first.
    value = _seed * 1103515245.0 + 12345.0
    modulus = math.fmod(value, 4294967296.0)
    _seed = int(modulus) & 0x7FFFFFFF

    return _seed / 0x7FFFFFFF


def int_(min_value: int, max_value: int) -> int:
    return math.floor(_next() * (max_value - min_value + 1)) + min_value


def round_half_up(value: float) -> int:
    """JS Math.round semantics (half rounds toward +infinity)."""
    return math.floor(value + 0.5)


def float_(min_value: float, max_value: float, decimals: int = 1) -> float:
    value = _next() * (max_value - min_value) + min_value
    factor = 10**decimals

    return round_half_up(value * factor) / factor


def bool_(probability_true: float = 0.5) -> bool:
    return _next() < probability_true


def pick(items: Sequence[Any]) -> Any:
    return items[int_(0, len(items) - 1)]


def pick_some(items: Sequence[Any], min_count: int = 0, max_count: int | None = None) -> list[Any]:
    if max_count is None:
        max_count = len(items)

    count = int_(min_count, min(max_count, len(items)))
    pool = list(items)
    result: list[Any] = []

    for _ in range(count):
        if not pool:
            break

        remove_at = int_(0, len(pool) - 1)

        result.append(pool.pop(remove_at))

    return result


def maybe(value: Any, probability: float = 0.5) -> Any:
    return value if bool_(probability) else None


def iso_z(value: datetime) -> str:
    """Format a datetime like JS toISOString (UTC, millisecond precision, Z)."""
    utc = value.astimezone(timezone.utc)
    milliseconds = utc.microsecond // 1000

    return (
        f"{utc.year:04d}-{utc.month:02d}-{utc.day:02d}"
        f"T{utc.hour:02d}:{utc.minute:02d}:{utc.second:02d}.{milliseconds:03d}Z"
    )


def now_iso() -> str:
    return iso_z(datetime.now(timezone.utc))


def past_date(max_minutes_ago: int = 60 * 24 * 30) -> str:
    minutes_ago = int_(0, max_minutes_ago)

    return iso_z(datetime.now(timezone.utc) - timedelta(minutes=minutes_ago))


def future_date(max_minutes_ahead: int = 60 * 24 * 30) -> str:
    minutes_ahead = int_(0, max_minutes_ahead)

    return iso_z(datetime.now(timezone.utc) + timedelta(minutes=minutes_ahead))


def time_of_day() -> str:
    return f"{int_(0, 23):02d}:{int_(0, 59):02d}"


def date_only(day_offset: int = 0) -> str:
    """JS uses the local calendar date (then serializes as UTC ISO date)."""
    local = datetime.now().astimezone() + timedelta(days=day_offset)

    return local.astimezone(timezone.utc).strftime("%Y-%m-%d")


FIRST_NAMES = [
    "Anna",
    "Ben",
    "Clara",
    "David",
    "Emma",
    "Felix",
    "Greta",
    "Hannes",
    "Ida",
    "Jonas",
    "Katja",
    "Lukas",
    "Mia",
    "Noah",
    "Olga",
    "Paul",
]

LAST_NAMES = [
    "Müller",
    "Schmidt",
    "Schneider",
    "Fischer",
    "Weber",
    "Meyer",
    "Wagner",
    "Becker",
    "Hoffmann",
    "Koch",
    "Bauer",
    "Richter",
    "Klein",
    "Wolf",
]

BUILDING_NAMES = [
    "Hauptgebäude",
    "Verwaltung",
    "Nordflügel",
    "Südflügel",
    "Werkstatt",
    "Lagerhalle",
    "Bürohaus",
    "Ostgebäude",
    "Westgebäude",
    "Technikzentrum",
]

ROOM_NAMES = [
    "Büro",
    "Konferenzraum",
    "Lager",
    "Küche",
    "Empfang",
    "Flur",
    "Labor",
    "Serverraum",
    "Aufenthaltsraum",
    "Werkstatt",
    "Archiv",
    "Besprechung",
]

CITIES = ["Berlin", "Hamburg", "München", "Köln", "Frankfurt", "Dresden"]


def first_name() -> str:
    return pick(FIRST_NAMES)


def last_name() -> str:
    return pick(LAST_NAMES)


def full_name() -> str:
    return f"{first_name()} {last_name()}"


def building_name() -> str:
    return f"{pick(BUILDING_NAMES)} {pick(CITIES)}"


def room_name() -> str:
    return f"{pick(ROOM_NAMES)} {int_(100, 499)}"


def hex_(length: int) -> str:
    chars = "0123456789ABCDEF"

    return "".join(chars[int_(0, len(chars) - 1)] for _ in range(length))


def dev_eui() -> str:
    return hex_(16)


def postcode() -> str:
    return f"{int_(10000, 99999)}"


def next_id() -> int:
    global _id_counter

    _id_counter += 1

    return _id_counter


def reset_seed(value: int = 1337) -> None:
    global _seed, _id_counter

    _seed = value
    _id_counter = 1000

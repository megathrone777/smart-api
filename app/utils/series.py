from __future__ import annotations

import time
from datetime import datetime, timezone
from typing import Optional

from app.utils.random_data import float_, iso_z


def _parse_ms(value: Optional[str]) -> Optional[int]:
    if not value:
        return None

    text = value.strip()

    if text.endswith("Z"):
        text = text[:-1] + "+00:00"

    try:
        parsed = datetime.fromisoformat(text)
    except ValueError:
        return None

    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)

    return int(parsed.timestamp() * 1000)


def series(from_: str, to_: str, points: int) -> list[dict]:
    now_ms = int(time.time() * 1000)
    start = _parse_ms(from_) or now_ms - 7 * 24 * 60 * 60 * 1000
    end = _parse_ms(to_) or now_ms
    step = (end - start) / max(points - 1, 1)

    return [
        {
            "createdAt": iso_z(datetime.fromtimestamp((start + step * index) / 1000, tz=timezone.utc)),
            "value": float_(0, 25, 2),
        }
        for index in range(points)
    ]

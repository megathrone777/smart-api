from __future__ import annotations

from app.globals.collections import collections
from app.helpers.get_all import get_all


def get_all_rooms() -> list[dict]:
    return get_all(collections.room)

from __future__ import annotations

from app.utils.random_data import int_


def empty_conflict(action: str) -> dict:
    return {
        "action": action,
        "hasConflicts": False,
        "invalidRows": [],
        "totalSlots": int_(1, 10),
        "validSlots": int_(1, 10),
    }

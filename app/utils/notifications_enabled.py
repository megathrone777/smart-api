from __future__ import annotations

from app.store.get_flag import get_flag


def notifications_enabled() -> bool:
    value = get_flag("notificationsEnabled")

    return value if value is not None else True

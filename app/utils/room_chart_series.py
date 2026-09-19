from __future__ import annotations

from typing import Callable

from app.utils.series import series


def room_chart_points(metric: Callable[[], float]) -> list[dict]:
    return [
        {"createdAt": point["createdAt"], "value": metric()}
        for point in series("", "", 48)
    ]

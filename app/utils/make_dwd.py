from __future__ import annotations

from app.utils.random_data import bool_, building_name, date_only, float_, int_, next_id


def make_dwd(heating_threshold: float) -> dict:
    return {
        "consecutiveDaysAboveThreshold": int_(0, 6),
        "forecast": [
            {"avgTemp": float_(8, 22), "date": date_only(index + 1)}
            for index in range(7)
        ],
        "heatingThreshold": heating_threshold,
        "historical": [
            {
                "aboveThreshold": bool_(0.5),
                "avgTemp": float_(8, 22),
                "date": date_only(-(7 - index)),
            }
            for index in range(7)
        ],
        "station": {"mosmixStationId": f"{next_id()}", "name": building_name()},
        "statusMessage": "Wetterdaten vom Deutschen Wetterdienst",
    }

from __future__ import annotations

from typing import Any, Mapping

DEFAULT_LIMIT = 10
DEFAULT_PAGE = 1


def _to_number(value: Any, default: int) -> int:
    """Reproduce JS `+(x) || default` semantics: invalid/0 values fall back."""
    if value is None:
        return default

    if isinstance(value, bool):
        return int(value) or default

    if isinstance(value, (int, float)):
        number = int(value)
    else:
        try:
            number = int(str(value).strip())
        except (TypeError, ValueError):
            try:
                number = int(float(str(value).strip()))
            except (TypeError, ValueError):
                return default

    return number if number else default


def paginate(
    rows: list[Any], query: Mapping[str, Any] | None = None
) -> dict[str, Any]:
    query = query or {}
    limit = _to_number(query.get("limit"), DEFAULT_LIMIT)
    page = _to_number(query.get("page"), DEFAULT_PAGE)
    start = (page - 1) * limit

    return {
        "count": len(rows),
        "rows": rows[start : start + limit],
    }

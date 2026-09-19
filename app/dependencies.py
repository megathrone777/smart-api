from __future__ import annotations

from typing import Any

from fastapi import Query, Request

from app.core.errors import UnauthorizedError


def pagination(
    page: str | None = Query(default=None),
    limit: str | None = Query(default=None),
) -> dict[str, str | None]:
    """Reproduce the Fastify `page`/`limit` querystring contract."""
    return {"page": page, "limit": limit}


def get_current_user(request: Request) -> dict[str, Any]:
    """Return the JWT payload verified by the auth hook middleware."""
    user = getattr(request.state, "user", None)

    if not user:
        raise UnauthorizedError()

    return user

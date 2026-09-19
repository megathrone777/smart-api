from __future__ import annotations

import jwt
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.base import RequestResponseEndpoint
from urllib.parse import urlparse

from app.core.config import settings
from app.core.errors import register_error_handlers
from app.routers import (
    auth,
    devices,
    energy,
    health,
    heating,
    locations,
    notifications,
    occupancy,
    operations,
    overview,
    season,
    tags,
    users,
)

PUBLIC_PREFIXES = ("/auth/", "/docs", "/health", "/openapi.json")
LOCAL_HOSTNAMES = {"127.0.0.1", "192.168.0.227", "::1", "localhost"}
ALLOWED_HEADERS = ["Authorization", "Content-Type", "Pass"]
ALLOWED_METHODS = ["DELETE", "GET", "HEAD", "OPTIONS", "PATCH", "POST", "PUT"]


def is_allowed_origin(origin: str) -> bool:
    try:
        hostname = urlparse(origin).hostname
    except ValueError:
        return False

    if not hostname:
        return False

    return hostname in LOCAL_HOSTNAMES or "smartheating" in hostname


class CorsMiddleware(BaseHTTPMiddleware):
    """Reproduces the @fastify/cors configuration of the reference app."""

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        origin = request.headers.get("origin")
        allowed = origin is None or is_allowed_origin(origin)

        if (
            request.method == "OPTIONS"
            and "access-control-request-method" in request.headers
        ):
            if not allowed:
                return Response(status_code=204)

            response = Response(status_code=204)
        else:
            response = await call_next(request)

        if allowed and origin is not None:
            response.headers["access-control-allow-origin"] = origin
            response.headers["vary"] = "Origin"
            response.headers["access-control-allow-methods"] = ",".join(ALLOWED_METHODS)
            response.headers["access-control-allow-headers"] = ",".join(ALLOWED_HEADERS)

        return response


class AuthHookMiddleware(BaseHTTPMiddleware):
    """Reproduces the onRequest hook of the reference app.

    Public prefixes are skipped, the `Pass` header with the bypass password is
    accepted, everything else must carry a valid JWT (Authorization: Bearer).
    """

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        path = request.url.path

        if not any(path.startswith(prefix) for prefix in PUBLIC_PREFIXES):
            if request.headers.get("pass") != settings.app_bypass_pass:
                authorization = request.headers.get("authorization") or ""
                token = (
                    authorization[7:].strip()
                    if authorization.lower().startswith("bearer ")
                    else ""
                )

                try:
                    payload = jwt.decode(
                        token, settings.app_jwt_secret, algorithms=["HS256"]
                    )
                except Exception:
                    return JSONResponse(
                        status_code=401,
                        content={"message": "Unauthorized", "statusCode": 401},
                    )

                request.state.user = payload

        return await call_next(request)


app = FastAPI(title="Smartheating API", version="1.0.0")

# Auth hook first (inner), CORS last (outer) so preflight requests are
# answered before authentication, like in the Fastify app.
app.add_middleware(AuthHookMiddleware)
app.add_middleware(CorsMiddleware)

register_error_handlers(app)

app.include_router(auth.router)
app.include_router(health.router)
app.include_router(locations.router)
app.include_router(devices.router)
app.include_router(tags.router)
app.include_router(users.router)
app.include_router(heating.router)
app.include_router(energy.router)
app.include_router(season.router)
app.include_router(occupancy.router)
app.include_router(overview.router)
app.include_router(notifications.router)
app.include_router(operations.router)


@app.get("/")
async def root():
    return {"message": "Hello"}

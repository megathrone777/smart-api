"""Fastify-compatible error types and handlers."""

from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


class ApiError(Exception):
    """Raised by services to reproduce a custom Fastify `reply.code(x).send(y)`."""

    def __init__(self, status_code: int, content: dict) -> None:
        super().__init__(str(content))
        self.status_code = status_code
        self.content = content


class UnauthorizedError(ApiError):
    def __init__(self) -> None:
        super().__init__(401, {"message": "Unauthorized", "statusCode": 401})


def api_error_handler(_request: Request, exc: ApiError) -> JSONResponse:
    return JSONResponse(status_code=exc.status_code, content=exc.content)


def validation_error_handler(_request: Request, exc: RequestValidationError) -> JSONResponse:
    # Fastify/Ajv answers schema violations with 400 + {statusCode, error, message}
    parts = [
        f"{'/'.join(str(loc) for loc in error['loc'])}: {error['msg']}"
        for error in exc.errors()
    ]
    message = "; ".join(parts) if parts else "Bad Request"

    return JSONResponse(
        status_code=400,
        content={"statusCode": 400, "error": "Bad Request", "message": message},
    )


def server_error_handler(_request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content={
            "statusCode": 500,
            "error": "Internal Server Error",
            "message": str(exc),
        },
    )


def register_error_handlers(app: FastAPI) -> None:
    app.add_exception_handler(ApiError, api_error_handler)
    app.add_exception_handler(RequestValidationError, validation_error_handler)
    app.add_exception_handler(Exception, server_error_handler)

from __future__ import annotations

import bcrypt
import jwt

from app.core.config import settings
from app.core.errors import ApiError
from app.globals.collections import collections
from app.helpers import get_by_id, put

SALT_ROUNDS = 10


def create_token(email: str, role: str) -> str:
    return jwt.encode(
        {"email": email, "role": role}, settings.app_jwt_secret, algorithm="HS256"
    )


def login(email: str, password: str) -> dict:
    existing_user = get_by_id(collections.authUser, email)

    if not existing_user:
        raise ApiError(401, {"error": "Invalid credentials"})

    valid = bcrypt.checkpw(
        password.encode(), (existing_user.get("passwordHash") or "").encode()
    )

    if not valid:
        raise ApiError(401, {"error": "Invalid credentials"})

    return {
        "role": existing_user["role"],
        "token": create_token(existing_user["email"], existing_user["role"]),
    }


def register(
    email: str, first_name: str, last_name: str, password: str, role: str
) -> dict:
    existing_user = get_by_id(collections.authUser, email)

    if existing_user:
        raise ApiError(409, {"error": "User already exists"})

    password_hash = bcrypt.hashpw(
        password.encode(), bcrypt.gensalt(rounds=SALT_ROUNDS)
    ).decode()

    put(
        collections.authUser,
        {
            "email": email,
            "firstName": first_name,
            "lastName": last_name,
            "passwordHash": password_hash,
            "role": role,
        },
    )

    return {"role": role, "token": create_token(email, role)}

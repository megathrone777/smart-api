from __future__ import annotations

from typing import Any

from app.globals.collections import collections
from app.helpers import get_all, paginate, patch, put, remove
from app.schemas.user import UserBody
from app.utils import random_data


def get_profile(jwt_user: dict[str, Any]) -> dict[str, Any]:
    email = jwt_user.get("email")
    managed = get_all(collections.managedUser)
    match = next((user for user in managed if user.get("email") == email), None)

    first_name = match.get("firstName") if match else None
    last_name = match.get("lastName") if match else None

    return {
        "email": email,
        "firstName": first_name if first_name is not None else "Admin",
        "lastName": last_name if last_name is not None else "User",
        "role": jwt_user.get("role"),
    }


def get_users(query: dict[str, Any]) -> dict[str, Any]:
    users = get_all(collections.managedUser)

    name = query.get("name")

    if name:
        needle = name.lower()
        users = [
            user
            for user in users
            if needle in f"{user.get('firstName')} {user.get('lastName')}".lower()
            or needle in f"{user.get('email')}".lower()
        ]

    roles = query.get("roles")

    if roles:
        role_list = roles.split(",")
        users = [user for user in users if user.get("role") in role_list]

    return paginate(users, query)


def create_user(body: UserBody) -> dict[str, Any]:
    user: dict[str, Any] = {
        "email": body.email
        if body.email is not None
        else f"user{random_data.int_(1, 999)}@example.com",
        "firstName": body.firstName
        if body.firstName is not None
        else random_data.first_name(),
        "id": random_data.next_id(),
        "inviteIsPending": True,
        "lastName": body.lastName
        if body.lastName is not None
        else random_data.last_name(),
        "locations": body.locations if body.locations is not None else [],
        "notificationsEnabled": (
            body.notificationsEnabled if body.notificationsEnabled is not None else False
        ),
        "role": body.role if body.role is not None else "operator",
    }

    put(collections.managedUser, user)

    return user


def update_user(user_id: str, body: UserBody) -> dict[str, Any]:
    updated = patch(
        collections.managedUser, user_id, body.model_dump(exclude_unset=True)
    )

    return updated if updated is not None else {"success": False}


def delete_user(user_id: str) -> dict[str, bool]:
    remove(collections.managedUser, user_id)

    return {"success": True}

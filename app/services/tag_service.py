from __future__ import annotations

from typing import Any

from app.globals.collections import collections
from app.helpers import get_all, paginate, patch, put, remove
from app.schemas.tag import TagBody
from app.utils import random_data


def create_tag(body: TagBody) -> dict[str, Any]:
    now = random_data.now_iso()

    tag: dict[str, Any] = {
        "assignedRoomsCount": 0,
        "color": body.color if body.color is not None else "blue",
        "createdAt": now,
        "customerId": 1,
        "id": random_data.next_id(),
        "lastUsed": now,
        "name": body.name if body.name is not None else "Neue Markierung",
        "updatedAt": now,
    }

    put(collections.tag, tag)

    return tag


def delete_tag(tag_id: str) -> dict[str, bool]:
    remove(collections.tag, tag_id)

    return {"success": True}


def get_recent_tags() -> list[dict[str, Any]]:
    tags = get_all(collections.tag)

    return tags[:5]


def get_tags(query: dict[str, Any]) -> dict[str, Any]:
    tags = get_all(collections.tag)

    name = query.get("name")

    if name:
        needle = name.lower()
        tags = [tag for tag in tags if needle in f"{tag.get('name')}".lower()]

    return paginate(tags, query)


def update_tag(tag_id: str, body: TagBody) -> dict[str, Any]:
    changes: dict[str, Any] = {}

    if body.color is not None:
        changes["color"] = body.color

    if body.name is not None:
        changes["name"] = body.name

    changes["updatedAt"] = random_data.now_iso()

    updated_tag = patch(collections.tag, tag_id, changes)

    return updated_tag if updated_tag is not None else {"success": False}

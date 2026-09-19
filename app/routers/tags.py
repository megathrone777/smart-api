from typing import Any

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.dependencies import pagination
from app.schemas.tag import TagBody
from app.services import tag_service

router = APIRouter()


@router.delete("/tags/{tag_id}")
def delete_tag(tag_id: str):
    return tag_service.delete_tag(tag_id)


@router.delete("/tags/{tag_id}/room/unassign")
def unassign_tag_room(tag_id: str):
    return {"success": True}


@router.get("/tags/list")
def get_tags(query: dict[str, Any] = Depends(pagination), name: str | None = None):
    return tag_service.get_tags({**query, "name": name})


@router.get("/tags/recent")
def get_recent_tags():
    return tag_service.get_recent_tags()


@router.post("/tags")
def create_tag(body: TagBody):
    tag = tag_service.create_tag(body)

    return JSONResponse(status_code=201, content=tag)


@router.post("/tags/{tag_id}/room/assign")
def assign_tag_room(tag_id: str):
    return {"success": True}


@router.put("/tags/{tag_id}")
def update_tag(tag_id: str, body: TagBody):
    return tag_service.update_tag(tag_id, body)

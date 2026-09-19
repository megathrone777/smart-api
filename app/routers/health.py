from fastapi import APIRouter

from app.store.get_flag import get_flag

router = APIRouter()


@router.get("/health")
def health():
    get_flag("__health")

    return {"status": "ok"}

from fastapi import APIRouter
from core.supabase_client import supabase

router = APIRouter()

@router.get("/tags")

async def list_tags():
  try:
    response = supabase.table("tag").select("*").limit(10).execute()
    return response.data
  except Exception as error:
    return { "status": "database error", "detail": str(error) }
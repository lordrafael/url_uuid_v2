from fastapi import APIRouter, HTTPException
from ..cache_conn import cache

cache_router = APIRouter()

def get_url_by_uuid_cache(url_uuid):
    url = cache.get(url_uuid)
    return url if url else None

@cache_router.get("/{url_uuid}")
async def read_url_from_cache(url_uuid: str):
    url = get_url_by_uuid_cache(url_uuid)
    if url is None:
        raise HTTPException(status_code=404, detail="URL not found")
    return {"uuid": url_uuid, "url": url}

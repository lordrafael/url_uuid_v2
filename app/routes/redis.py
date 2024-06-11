from fastapi import APIRouter, HTTPException
from ..redis_conn import create_redis_connection

redis_router = APIRouter()

def get_url_by_uuid_redis(url_uuid):
    redis_connection = create_redis_connection()
    url = redis_connection.get(url_uuid)
    return url.decode('utf-8') if url else None

@redis_router.get("/{url_uuid}")
async def read_url_from_redis(url_uuid: str):
    url = get_url_by_uuid_redis(url_uuid)
    if url is None:
        raise HTTPException(status_code=404, detail="URL not found")
    return {"uuid": url_uuid, "url": url}

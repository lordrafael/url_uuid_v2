import logging
from fastapi import APIRouter, HTTPException, Query, UploadFile
from ..service.handlers import get_url_by_uuid_mysql, get_url_by_uuid_redis, get_url_by_uuid_cache

get_router = APIRouter()

logger = logging.getLogger(__name__)

@get_router.get("/{url_uuid}")
def read_url(url_uuid: str, db: str = Query(..., description="Database to use ('mysql',redis' or 'cache')")):
    if db == "mysql":
        url = get_url_by_uuid_mysql(url_uuid)
    elif db == "redis":
        url = get_url_by_uuid_redis(url_uuid)
    elif db == "cache":
        url = get_url_by_uuid_cache(url_uuid)
    else:
        logger.error("Database not found or defined")
        raise HTTPException(status_code=400, detail="database naiiiiiiiiii")
        
    
    if url is None:
        logging.error("URL not found")
        raise HTTPException(status_code=404, detail="URL naiiiiiiiiii")
    
    return {"uuid": url_uuid, "url": url}


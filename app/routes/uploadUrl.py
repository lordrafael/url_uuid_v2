import io
import logging
from fastapi import APIRouter, File, HTTPException, UploadFile
from ..service.handlers import process_csv

post_router = APIRouter()

logger = logging.getLogger(__name__)

@post_router.post("/")
async def upload_csv(file: UploadFile = File(...)):
    try:
        #print("hit paiseeeeeeeeee")
        content = await file.read()
        file_like_object = io.StringIO(content.decode('utf-8'))
        total_mysql_time, total_redis_time, total_cache_time = process_csv(file_like_object)
        logger.info("Successfully uploaded file")

        return {
                "message": "CSV processed successfully",
                "elapsed_mysql_time": total_mysql_time,
                "elapsed_redis_time": total_redis_time, 
                "elapsed_cache_time": total_cache_time
                }
    except Exception as e:
        logger.error("Failed to process file")
        raise HTTPException(status_code=500, detail=str(e))
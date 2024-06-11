import uuid
from fastapi import APIRouter, Form,  HTTPException
from ..mysql_conn import create_mysql_connection, execute_query
from ..redis_conn import create_redis_connection
from ..cache_conn import cache
import time

url_router = APIRouter()

def process_url(url: str):
    
    
    insert_url_query = """
    INSERT INTO urls (uuid, url) VALUES (%s, %s)
    """
    
    url_uuid = str(uuid.uuid4())
    
    start_mysql_time = time.time() 
    mysql_connection = create_mysql_connection()
    execute_query(mysql_connection, insert_url_query, (url_uuid, url))
    end_mysql_time = time.time()
    elapsed_mysql_time = end_mysql_time - start_mysql_time
    #print(f"elapsed mysql time = {elapsed_mysql_time}")
    
    start_redis_time = time.time() 
    redis_connection = create_redis_connection()
    redis_connection.set(url_uuid, url)
    end_redis_time = time.time()
    elapsed_redis_time = end_redis_time - start_redis_time
    #print(f"elapsed redis time = {elapsed_redis_time}")
    
    start_cache_time = time.time() 
    cache[url_uuid] = url
    end_cache_time = time.time()
    elapsed_cache_time = end_cache_time - start_cache_time
    #print(f"elapsed cache time = {elapsed_cache_time}")
    
    #return url_uuid
    return url_uuid, elapsed_mysql_time, elapsed_redis_time, elapsed_cache_time

@url_router.post("/")
async def process_single_url(url: str = Form(...)):
    try:
        #url_uuid = process_url(url)
        url_uuid, elapsed_mysql_time, elapsed_redis_time, elapsed_cache_time = process_url(url)
        #return {"uuid": url_uuid}
        return {
            "uuid": url_uuid,
            "elapsed_mysql_time": elapsed_mysql_time,
            "elapsed_redis_time": elapsed_redis_time,
            "elapsed_cache_time": elapsed_cache_time
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
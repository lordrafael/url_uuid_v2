import time
import uuid
import pandas as pd
from fastapi import APIRouter, File, UploadFile, HTTPException
import io
from ..mysql_conn import create_mysql_connection, execute_query
from ..redis_conn import create_redis_connection
from ..cache_conn import cache

csv_router = APIRouter()

def process_csv(file):
    start_time = time.time()
    df = pd.read_csv(file)
    mysql_connection = create_mysql_connection()
    redis_connection = create_redis_connection()
    
    insert_url_query = """
    INSERT INTO urls (uuid, url) VALUES (%s, %s)
    """
    
    for _, row in df.iterrows():
        url = row['url']
        url_uuid = str(uuid.uuid4())
        
        start_mysql_time = time.time()
        execute_query(mysql_connection, insert_url_query, (url_uuid, url))
        end_mysql_time = time.time()
        mysql_elapsed_time = end_mysql_time - start_mysql_time
        
        start_redis_time = time.time()
        redis_connection.set(url_uuid, url)
        end_redis_time = time.time()
        redis_elapsed_time = end_redis_time - start_redis_time
        
        start_cache_time = time.time()
        cache[url_uuid] = url
        end_cache_time = time.time()
        cache_elapsed_time = end_cache_time - start_cache_time
        
    end_time = time.time()
    total_elapsed_time = end_time - start_time    
    print(f"Total time taken to process CSV and store data: {total_elapsed_time} seconds")
    print(f"Total time taken to store in mysql: {mysql_elapsed_time} seconds")
    print(f"Total time taken to store in redis: {redis_elapsed_time} seconds")
    print(f"Total time taken to store in cache: {cache_elapsed_time} seconds")

@csv_router.post("/")
async def upload_csv(file: UploadFile = File(...)):
    try:
        content = await file.read()
        file_like_object = io.StringIO(content.decode('utf-8'))
        process_csv(file_like_object)
        return {"message": "CSV processed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

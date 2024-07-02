
from contextlib import contextmanager
import logging
import time
from app.db.mysql_conn import create_mysql_connection
from app.db.redis_conn import create_redis_connection
from app.db.cache_conn import cache

logger = logging.getLogger(__name__)

@contextmanager
def get_mysql_connection():
    conn = create_mysql_connection()
    try:
        yield conn
    finally:
        conn.close()

@contextmanager
def get_redis_connection():
    conn = create_redis_connection()
    try:
        yield conn
    finally:
        conn.close()

def insert_into_mysql(data_to_insert):
    insert_url_query = """
    INSERT INTO urls (uuid, url) VALUES (%s, %s)
    """
    with get_mysql_connection() as mysql_connection:
        try:
            start_mysql_time = time.time()
            cursor = mysql_connection.cursor()
            
            cursor.executemany(insert_url_query, data_to_insert)
            mysql_connection.commit()
            cursor.close()
    
            total_mysql_time = time.time() - start_mysql_time

            logger.info("Successfully stored in MySQL")
            return total_mysql_time
        
        except Exception as e:
            mysql_connection.rollback()
            print(f"Error during batch insert: {e}")
            logger.error(f"Error during MySQL insert: {e}")
            return None

def insert_into_redis(data_to_insert):
    with get_redis_connection() as redis_connection:
                
        start_redis_time = time.time()
        for url_uuid, url in data_to_insert:
            try:
                redis_connection.set(url_uuid, url)
            except Exception as e:
                print(f"Error during Redis insert: {e}")
                logger.error(f"Error during Redis insert: {e}")

        logger.info("Successfully stored in Redis")

        total_redis_time = time.time() - start_redis_time

        return total_redis_time

def insert_into_cache(data_to_insert):
    
    start_cache_time = time.time()
    for url_uuid, url in data_to_insert:
        try:
            cache[url_uuid] = url
            
        except Exception as e:
            print(f"Error inserting into cache: {e}")
            logger.error(f"Error during Cache insert: {e}")
            
    logger.info("Successfully stored in Cache")

    total_cache_time = time.time() - start_cache_time

    return total_cache_time
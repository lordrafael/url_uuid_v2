from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
import time
import uuid
import pandas as pd
from ..db.redis_conn import create_redis_connection
from ..db.mysql_conn import create_mysql_connection
from ..db.cache_conn import cache

def get_url_by_uuid_mysql(url_uuid):
    start_time = time.time()
    mysql_connection = create_mysql_connection()
    select_url_query = "SELECT url FROM urls WHERE uuid = %s"
    cursor = mysql_connection.cursor()
    cursor.execute(select_url_query, (url_uuid,))
    result = cursor.fetchone()
    end_time = time.time()
    total_elapsed_time = end_time - start_time
    print(f"Time taken to retrieve URL from MySQL: {total_elapsed_time} seconds")
    return result[0] if result else None

def get_url_by_uuid_redis(url_uuid):
    redis_connection = create_redis_connection()
    url = redis_connection.get(url_uuid)
    return url.decode('utf-8') if url else None

def get_url_by_uuid_cache(url_uuid):
    url = cache.get(url_uuid)
    return url if url else None

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

            return total_mysql_time
        
        except Exception as e:
            mysql_connection.rollback()
            print(f"Error during batch insert: {e}")
            return None

def insert_into_redis(data_to_insert):
    with get_redis_connection() as redis_connection:
        
        total_redis_time = 0
        
        start_redis_time = time.time()
        for url_uuid, url in data_to_insert:
            try:
                redis_connection.set(url_uuid, url)
            except Exception as e:
                print(f"Error inserting into Redis: {e}")
        total_redis_time += time.time() - start_redis_time

        return total_redis_time

def insert_into_cache(data_to_insert):
    
    total_cache_time = 0

    start_cache_time = time.time()
    for url_uuid, url in data_to_insert:
        try:
            cache[url_uuid] = url
        except Exception as e:
            print(f"Error inserting into cache: {e}")
            
    total_cache_time += time.time() - start_cache_time

    return total_cache_time

def process_csv(file):
    try:
        df = pd.read_csv(file)
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return

    data_to_insert = [(str(uuid.uuid4()), row['url']) for _, row in df.iterrows()]
    
    
    with ThreadPoolExecutor(max_workers=3) as executor:
        mysql_future = executor.submit(insert_into_mysql, data_to_insert)
        redis_future = executor.submit(insert_into_redis, data_to_insert)
        cache_future = executor.submit(insert_into_cache, data_to_insert)
        
        elapsed_mysql_time = mysql_future.result()
        elapsed_redis_time = redis_future.result()
        elapsed_cache_time = cache_future.result()

    return elapsed_mysql_time, elapsed_redis_time, elapsed_cache_time

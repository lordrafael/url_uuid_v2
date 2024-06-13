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
        
def process_csv(file):
    try:
        df = pd.read_csv(file)
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return

    insert_url_query = """
    INSERT INTO urls (uuid, url) VALUES (%s, %s)
    """

    # Collect all data to be inserted in a list of tuples
    data_to_insert = []

    with get_mysql_connection() as mysql_connection, get_redis_connection() as redis_connection:
        for _, row in df.iterrows():
            try:
                url = row['url']
                url_uuid = str(uuid.uuid4())
                
                data_to_insert.append((url_uuid, url))
                
                # Cache in Redis and local cache
                start_redis_time = time.time()     
                redis_connection.set(url_uuid, url)
                end_redis_time = time.time()
                elapsed_redis_time = end_redis_time - start_redis_time
                start_cache_time = time.time() 
                cache[url_uuid] = url
                end_cache_time = time.time()
                elapsed_cache_time = end_cache_time - start_cache_time
            except Exception as e:
                print(f"Error processing row {row}: {e}")

        # Execute batch insert
        if data_to_insert:
            try:
                start_mysql_time = time.time() 
                cursor = mysql_connection.cursor()
                cursor.executemany(insert_url_query, data_to_insert)
                mysql_connection.commit()
                cursor.close()
                end_mysql_time = time.time()
                elapsed_mysql_time = end_mysql_time - start_mysql_time
            except Exception as e:
                mysql_connection.rollback()
                print(f"Error during batch insert: {e}")
    
    return elapsed_mysql_time, elapsed_redis_time, elapsed_cache_time



from concurrent.futures import ThreadPoolExecutor
import time
import uuid
import pandas as pd
from app.db.redis_conn import create_redis_connection
from app.db.mysql_conn import create_mysql_connection
from app.db.cache_conn import cache
from app.repository.store_data import insert_into_mysql,insert_into_redis,insert_into_cache


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

import time
from fastapi import APIRouter, HTTPException
from ..mysql_conn import create_mysql_connection

mysql_router = APIRouter()

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

@mysql_router.get("/{url_uuid}")
async def read_url_from_mysql(url_uuid: str):
    url = get_url_by_uuid_mysql(url_uuid)
    if url is None:
        raise HTTPException(status_code=404, detail="URL not found")
    return {"uuid": url_uuid, "url": url}

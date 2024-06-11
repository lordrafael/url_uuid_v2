import redis
from .config import REDIS_HOST, REDIS_PORT, REDIS_DB

def create_redis_connection():
    try:
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
        print("Connection to Redis successful")
        return r
    except Exception as e:
        print(f"The error '{e}' occurred")
        return None

import logging
import redis
from app.config import REDIS_HOST, REDIS_PORT, REDIS_DB

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def create_redis_connection():
    try:
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
        print("Successfully connected to Redis")
        logger.info("Successfully connected to Redis")

        return r
    except Exception as e:
        print(f"Error during Redis connection: {e}")
        logger.error(f"Error during Redis connection: {e}")

        return None

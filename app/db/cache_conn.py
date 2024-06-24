import logging
from cachetools import LRUCache
from ..config import CACHE_MAXSIZE

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

cache = LRUCache(maxsize=CACHE_MAXSIZE)
logger.info("Initialized Least Recently Used Cache with maximum size")
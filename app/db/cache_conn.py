import logging
from cachetools import LRUCache
from ..config import CACHE_MAXSIZE

logger = logging.getLogger(__name__)
logging.basicConfig(filename='urlUuid.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', encoding='utf-8')

cache = LRUCache(maxsize=CACHE_MAXSIZE)
logger.info("Initialized Least Recently Used Cache with maximum size")



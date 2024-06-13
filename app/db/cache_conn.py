from cachetools import LRUCache
from ..config import CACHE_MAXSIZE

cache = LRUCache(maxsize=CACHE_MAXSIZE)

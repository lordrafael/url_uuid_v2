from fastapi import FastAPI
from .routes.csv import csv_router
from .routes.mysql import mysql_router
from .routes.redis import redis_router
from .routes.cache import cache_router
from .routes.single_url import url_router

app = FastAPI()

app.include_router(csv_router, prefix="/process_csv", tags=["CSV"])
app.include_router(mysql_router, prefix="/url/mysql", tags=["MySQL"])
app.include_router(redis_router, prefix="/url/redis", tags=["Redis"])
app.include_router(cache_router, prefix="/url/cache", tags=["Cache"])
app.include_router(url_router, prefix="/process_url", tags=["Url"])



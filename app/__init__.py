from fastapi import FastAPI
from .routes.single_url import url_router
from .routes.get import get_router
from .routes.post import post_router

app = FastAPI()

app.include_router(url_router, prefix="/process_url", tags=["Url"])
app.include_router(get_router, prefix="/url", tags=["GET"])
app.include_router(post_router, prefix="/csv", tags=["POST"])

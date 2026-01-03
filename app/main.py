import logging
from fastapi import FastAPI

from app.core.logging import setup_logging
from app.api.routers import movies


setup_logging()

app = FastAPI()

logger = logging.getLogger(__name__)

@app.get("/healthz")
def healthz():
    logger.info("application is healthy")
    return {"status": "ok"}

app.include_router(movies.router)
import logging
from fastapi import FastAPI, Request

from app.core.logging import setup_logging
from app.api.routers import movies
from app.core.exception_handlers import register_exception_handlers

setup_logging()

app = FastAPI()

logger = logging.getLogger(__name__)

# register global exception handlers
register_exception_handlers(app)

app.include_router(movies.router)

@app.get("/healthz")
def healthz():
    logger.info("application is healthy")
    return {"status": "ok"}

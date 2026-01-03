import logging
from fastapi import FastAPI, Request

from app.core.logging import setup_logging
from app.api.routers import movies
from app.core.exception_handlers import register_exception_handlers

from app.core.database import init_db, engine

setup_logging()

app = FastAPI()

logger = logging.getLogger(__name__)

@app.on_event("startup")
async def startup():
    await init_db(engine)

# register global exception handlers
register_exception_handlers(app)

app.include_router(movies.router)

@app.get("/healthz")
def healthz():
    logger.info("application is healthy")
    return {"status": "ok"}

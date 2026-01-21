import logging
from fastapi import FastAPI, Request

from app.core.middleware import logging_context_middleware
from app.core.logging import setup_logging
from app.core.exception_handlers import register_exception_handlers
from app.api.routers import movies, reviews, auth, users

setup_logging()

app = FastAPI()

app.middleware("http")(logging_context_middleware)

logger = logging.getLogger(__name__)

# register global exception handlers
register_exception_handlers(app)

app.include_router(movies)
app.include_router(reviews)
app.include_router(auth)
app.include_router(users)


@app.get("/healthz")
def healthz():
    logger.info("application is healthy")
    return {"status": "ok"}

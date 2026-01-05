import logging
from fastapi import FastAPI, Request

from app.core.middleware import logging_context_middleware
from app.core.logging import setup_logging
from app.api.routers import movies, auth
from app.core.exception_handlers import register_exception_handlers


setup_logging()

app = FastAPI()

app.middleware("http")(logging_context_middleware)

logger = logging.getLogger(__name__)

# register global exception handlers
register_exception_handlers(app)

app.include_router(movies.router)
app.include_router(auth.router)

@app.get("/healthz")
def healthz():
    logger.info("application is healthy")
    return {"status": "ok"}

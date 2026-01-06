import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.core.exceptions import DomainError, NotFoundError, ValidationError, UnauthorizedError, ForbiddenError

EXCEPTION_STATUS_MAP = {
    NotFoundError: 404,
    ValidationError: 400,
    UnauthorizedError: 401,
    ForbiddenError: 403,
}

# @app.exception_handler(DomainError)
# async def domain_exception_handler(request: Request, exc: DomainError):
#     status_code = EXCEPTION_STATUS_MAP.get(type(exc), 400)
#     return JSONResponse(
#         status_code=status_code,
#         content={
#             "error": type(exc).__name__,
#             "detail": exc.message,
#         },
#     )

# async def domain_exception_handler(request: Request, exc: DomainError):
#     status_code = EXCEPTION_STATUS_MAP.get(type(exc), 400)
#     return JSONResponse(
#         status_code=status_code,
#         content={
#             "error": type(exc).__name__,
#             "detail": exc.message,
#         },
#     )

# logger = logging.getLogger("app.domain")
logger = logging.getLogger(__name__)

def get_status_code(exc: DomainError) -> int:
    for exc_type, status_code in EXCEPTION_STATUS_MAP.items():
        if isinstance(exc, exc_type):
            return status_code
    return 400

async def domain_exception_handler(request: Request, exc: DomainError):
    # status_code = EXCEPTION_STATUS_MAP.get(type(exc), 400)
    status_code = get_status_code(exc)

    logger.warning(
        "Domain error",
        extra={
            "error": type(exc).__name__,
            "detail": exc.message,
            "path": request.url.path,
            "status_code": status_code,
        },
    )

    return JSONResponse(
        status_code=status_code,
        content={
            "error": type(exc).__name__,
            "detail": exc.message,
        },
    )

def register_exception_handlers(app: FastAPI):
    """Register all global exception handlers for the app"""
    app.add_exception_handler(DomainError, domain_exception_handler)

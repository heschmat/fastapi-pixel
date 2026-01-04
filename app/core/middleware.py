import uuid
from fastapi import Request

from app.core.request_context import request_id_ctx, request_method_ctx


async def logging_context_middleware(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    request_id_ctx.set(request_id)
    request_method_ctx.set(request.method)

    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response

import uuid
from fastapi import Request

from app.core.request_context import request_id_ctx, request_method_ctx


# async def logging_context_middleware(request: Request, call_next):
#     request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
#     request_id_ctx.set(request_id)
#     request_method_ctx.set(request.method)

#     response = await call_next(request)
#     response.headers["X-Request-ID"] = request_id
#     return response

async def logging_context_middleware(request: Request, call_next):
    # Get request ID from incoming headers if present,
    # otherwise generate a new UUID
    request_id = request.headers.get("x-request-id", str(uuid.uuid4()))

    # Store the request_id in a ContextVar
    # `set()` returns a token representing the previous value
    # which is needed to restore the context later
    request_id_token = request_id_ctx.set(request_id)
    method_token = request_method_ctx.set(request.method)

    try:
        # Pass the request to the next middleware / route handler
        response = await call_next(request)

        # Add the request ID to the response headers
        # so clients can correlate requests and logs
        response.headers["x-request-id"] = request_id

        return response
    finally:
        # Always restore the previous ContextVar value
        # This prevents request data from leaking into
        # other concurrent requests or background tasks
        request_id_ctx.reset(request_id_token)
        request_method_ctx.reset(method_token)

import logging
from fastapi import Request

# def get_logger(name: str, request: Request | None = None):
#     logger = logging.getLogger(name)
#     if request:
#         return logging.LoggerAdapter(
#             logger,
#             {"request_id": request.state.request_id},
#         )
#     return logger

def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)

import logging
import sys
from pythonjsonlogger import jsonlogger

from app.core.request_context import request_id_ctx, request_method_ctx

LOG_FORMAT = (
    "%(asctime)s %(levelname)s %(name)s "
    "%(message)s %(request_id)s %(request_method)s"
)

class RequestContextFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = request_id_ctx.get() or "-"
        record.request_method = request_method_ctx.get() or "-"
        return True


# def setup_logging(log_level: str = "INFO"):
#     logging.basicConfig(
#         level=log_level,
#         format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
#         handlers=[logging.StreamHandler(sys.stdout)],
#     )

#     # Optional: reduce obvious noise
#     logging.getLogger("uvicorn.access").setLevel(logging.WARNING)

def setup_logging(log_level: str = "INFO"):
    handler = logging.StreamHandler(sys.stdout)

    # register the filter
    handler.addFilter(RequestContextFilter())

    # formatter = logging.Formatter(
    #     "%(asctime)s | %(levelname)s | %(name)s | request_id=%(request_id)s | %(message)s"
    # )
    formatter = jsonlogger.JsonFormatter(LOG_FORMAT)
    handler.setFormatter(formatter)

    root = logging.getLogger()
    root.setLevel(log_level)

    # Clear default handlers (uvicorn adds its own)
    root.handlers.clear()
    root.handlers = [handler]

    # Reduce noise from libraries
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    # logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy").setLevel(logging.WARNING)

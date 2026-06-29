"""
Logging Middleware
=================
Structured request logging with timing.
"""

import time
import logging
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

logger = logging.getLogger("app")


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        # Process the request
        response = await call_next(request)

        # Calculate duration
        duration = (time.time() - start_time) * 1000

        # Log the request
        logger.info(
            "request_completed",
            extra={
                "method": request.method,
                "path": request.url.path,
                "status_code": response.status_code,
                "duration_ms": round(duration, 2),
                "client_ip": request.client.host if request.client else None,
            },
        )

        # Add timing header
        response.headers["X-Process-Time"] = f"{duration:.2f}ms"
        return response

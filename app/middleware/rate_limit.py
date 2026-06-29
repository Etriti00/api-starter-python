"""
Rate Limiting Middleware
========================
Simple in-memory rate limiter per client IP.
Upgrade to Redis for distributed production.
"""

import time
from collections import defaultdict
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, requests_per_minute: int = 60):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self.hits: dict[str, list[float]] = defaultdict(list)

    async def dispatch(self, request: Request, call_next):
        # Skip health checks and docs
        if request.url.path in ["/api/v1/health", "/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)

        client_ip = request.client.host if request.client else "unknown"
        now = time.time()
        window = 60  # 1 minute

        # Clean up old entries
        self.hits[client_ip] = [
            t for t in self.hits[client_ip] if now - t < window
        ]

        if len(self.hits[client_ip]) >= self.requests_per_minute:
            return JSONResponse(
                status_code=429,
                content={"detail": "Too many requests", "retry_after": window},
            )

        self.hits[client_ip].append(now)
        response = await call_next(request)

        # Add rate limit headers
        remaining = self.requests_per_minute - len(self.hits[client_ip])
        response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
        response.headers["X-RateLimit-Remaining"] = str(max(0, remaining))
        response.headers["X-RateLimit-Reset"] = str(int(now + window))

        return response

import time
import logging
from starlette.requests import Request
from starlette.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware
from app.logging.logger import app_logger


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware to log API requests and responses
    """
    
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        # Process the request
        response = await call_next(request)
        
        # Calculate process time
        process_time = time.time() - start_time
        
        # Get user info if available
        user_info = getattr(request.state, 'user', None)
        user_id = user_info['id'] if user_info else 'anonymous'
        
        # Log the request
        app_logger.info(
            f"{request.method} {request.url.path} | "
            f"Status: {response.status_code} | "
            f"User: {user_id} | "
            f"Process Time: {process_time:.4f}s"
        )
        
        # Add process time to response headers
        response.headers["X-Process-Time"] = str(process_time)
        
        return response
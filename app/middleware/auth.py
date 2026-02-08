from fastapi import HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.requests import Request
from starlette.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
import jwt
from typing import Optional

from app.core.config import settings


class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.security = HTTPBearer(auto_error=False)  # Don't auto-error, we'll handle it manually

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        # Extract token from Authorization header
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header[len("Bearer "):]
            try:
                # Decode the token to get user info
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
                user_id = payload.get("sub")
                email = payload.get("email")
                
                if user_id and email:
                    # Add user info to request state
                    request.state.user = {
                        "id": user_id,
                        "email": email
                    }
            except jwt.ExpiredSignatureError:
                # Token is expired, but we won't stop the request here
                # Some endpoints might be public
                pass
            except jwt.JWTError:
                # Invalid token, but we won't stop the request here
                # Some endpoints might be public
                pass
        
        response = await call_next(request)
        return response


def get_current_user_optional(request: Request):
    """
    Get current user if authenticated, otherwise return None
    """
    return getattr(request.state, 'user', None)


def get_current_user_required(request: Request):
    """
    Get current user if authenticated, otherwise raise HTTPException
    """
    user = getattr(request.state, 'user', None)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
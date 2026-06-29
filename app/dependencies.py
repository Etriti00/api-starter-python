"""
Shared Dependencies
====================
FastAPI dependency functions for auth, pagination, etc.
"""

from typing import Optional
from fastapi import Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import User, UserRole
from app.auth.jwt import verify_access_token
from app.schemas import PaginatedRequest


async def get_current_user(
    token: str = Depends(lambda: None),  # Will be replaced with OAuth2
    db: AsyncSession = Depends(get_db),
) -> User:
    """Get the current authenticated user from the JWT token."""
    # This is simplified — in production, use OAuth2PasswordBearer
    from fastapi import Request
    # Note: In a full implementation, extract Bearer token from headers
    raise HTTPException(status_code=401, detail="Not authenticated")


async def require_admin(current_user: User = Depends(get_current_user)) -> User:
    """Require that the current user has admin role."""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=403,
            detail="Admin access required",
        )
    return current_user


def pagination_params(
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(20, ge=1, le=100, description="Items per page"),
    search: Optional[str] = Query(None, description="Search query"),
    sort_by: Optional[str] = Query(None, description="Sort field"),
    sort_order: str = Query("asc", regex="^(asc|desc)$", description="Sort order"),
) -> PaginatedRequest:
    """Common pagination parameters."""
    return PaginatedRequest(
        page=page,
        per_page=per_page,
        search=search,
        sort_by=sort_by,
        sort_order=sort_order,
    )

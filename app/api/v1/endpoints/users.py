"""User endpoints."""

from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status

from app.models.user import User, UserCreate, UserUpdate
from app.schemas.common import ResponseModel
from app.services.user_service import UserService
from app.api.v1.endpoints.auth import get_current_active_user, get_current_active_superuser

router = APIRouter()


@router.post("/", response_model=ResponseModel[User])
async def create_user(
    user_in: UserCreate,
    user_service: UserService = Depends(),
) -> Any:
    """Create new user."""
    user = await user_service.get_by_email(user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    
    user = await user_service.create(user_in)
    return ResponseModel(data=user, message="User created successfully")


@router.get("/me", response_model=ResponseModel[User])
async def read_user_me(
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """Get current user."""
    return ResponseModel(data=current_user)


@router.put("/me", response_model=ResponseModel[User])
async def update_user_me(
    user_in: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    user_service: UserService = Depends(),
) -> Any:
    """Update current user."""
    user = await user_service.update(current_user.id, user_in)
    return ResponseModel(data=user, message="User updated successfully")


@router.get("/{user_id}", response_model=ResponseModel[User])
async def read_user_by_id(
    user_id: str,
    current_user: User = Depends(get_current_active_user),
    user_service: UserService = Depends(),
) -> Any:
    """Get a specific user by ID."""
    user = await user_service.get_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this ID does not exist in the system",
        )
    
    # Users can only access their own data unless they are superusers
    if user.id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=403,
            detail="Not enough permissions"
        )
    
    return ResponseModel(data=user)


@router.get("/", response_model=ResponseModel[List[User]])
async def read_users(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_superuser),
    user_service: UserService = Depends(),
) -> Any:
    """Retrieve users (superuser only)."""
    users = await user_service.get_multi(skip=skip, limit=limit)
    return ResponseModel(data=users)



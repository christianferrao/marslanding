"""Common schemas."""

from typing import Any, Dict, Generic, List, Optional, TypeVar

from pydantic import BaseModel, Field

DataT = TypeVar('DataT')


class ResponseModel(BaseModel, Generic[DataT]):
    """Generic response model."""
    
    success: bool = True
    message: str = "Success"
    data: Optional[DataT] = None


class ErrorResponse(BaseModel):
    """Error response model."""
    
    success: bool = False
    message: str
    errors: Optional[Dict[str, Any]] = None


class PaginationParams(BaseModel):
    """Pagination parameters."""
    
    page: int = Field(1, ge=1, description="Page number")
    size: int = Field(10, ge=1, le=100, description="Page size")


class PaginatedResponse(BaseModel, Generic[DataT]):
    """Paginated response model."""
    
    items: List[DataT]
    total: int
    page: int
    size: int
    pages: int


class Token(BaseModel):
    """Token response model."""
    
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    """Token payload model."""
    
    sub: Optional[str] = None
    exp: Optional[int] = None
    type: Optional[str] = None

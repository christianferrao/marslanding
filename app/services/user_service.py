"""User service."""

from typing import Any, Dict, Optional, Union

from app.core.security import get_password_hash, verify_password
from app.db.mongodb import get_collection
from app.models.user import User, UserCreate, UserInDB, UserUpdate
from app.core.logging import get_logger

logger = get_logger(__name__)


class UserService:
    """User service for database operations."""
    
    def __init__(self):
        self.collection = get_collection("users")
    
    async def get_by_id(self, user_id: str) -> Optional[User]:
        """Get user by ID."""
        try:
            from bson import ObjectId
            user_doc = await self.collection.find_one({"_id": ObjectId(user_id)})
            if user_doc:
                return User(**user_doc)
            return None
        except Exception as e:
            logger.error("Error getting user by ID", user_id=user_id, error=str(e))
            return None
    
    async def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        try:
            user_doc = await self.collection.find_one({"email": email})
            if user_doc:
                return User(**user_doc)
            return None
        except Exception as e:
            logger.error("Error getting user by email", email=email, error=str(e))
            return None
    
    async def get_multi(
        self, *, skip: int = 0, limit: int = 100
    ) -> list[User]:
        """Get multiple users."""
        try:
            cursor = self.collection.find().skip(skip).limit(limit)
            users = []
            async for user_doc in cursor:
                users.append(User(**user_doc))
            return users
        except Exception as e:
            logger.error("Error getting multiple users", error=str(e))
            return []
    
    async def create(self, user_in: UserCreate) -> User:
        """Create new user."""
        try:
            # Check if user already exists
            existing_user = await self.get_by_email(user_in.email)
            if existing_user:
                raise ValueError("User with this email already exists")
            
            # Create user document
            user_dict = user_in.dict()
            user_dict["hashed_password"] = get_password_hash(user_in.password)
            del user_dict["password"]  # Remove plain password
            
            user_in_db = UserInDB(**user_dict)
            result = await self.collection.insert_one(user_in_db.dict(by_alias=True))
            
            # Return created user without password
            created_user = await self.get_by_id(str(result.inserted_id))
            return created_user
        except Exception as e:
            logger.error("Error creating user", error=str(e))
            raise
    
    async def update(
        self, user_id: str, user_in: UserUpdate
    ) -> Optional[User]:
        """Update user."""
        try:
            from bson import ObjectId
            from datetime import datetime
            
            update_data = user_in.dict(exclude_unset=True)
            if "password" in update_data:
                update_data["hashed_password"] = get_password_hash(update_data["password"])
                del update_data["password"]
            
            update_data["updated_at"] = datetime.utcnow()
            
            result = await self.collection.update_one(
                {"_id": ObjectId(user_id)},
                {"$set": update_data}
            )
            
            if result.modified_count:
                return await self.get_by_id(user_id)
            return None
        except Exception as e:
            logger.error("Error updating user", user_id=user_id, error=str(e))
            raise
    
    async def delete(self, user_id: str) -> bool:
        """Delete user."""
        try:
            from bson import ObjectId
            result = await self.collection.delete_one({"_id": ObjectId(user_id)})
            return result.deleted_count > 0
        except Exception as e:
            logger.error("Error deleting user", user_id=user_id, error=str(e))
            return False
    
    async def authenticate(self, email: str, password: str) -> Optional[User]:
        """Authenticate user."""
        try:
            user_doc = await self.collection.find_one({"email": email})
            if not user_doc:
                return None
            
            user_in_db = UserInDB(**user_doc)
            if not verify_password(password, user_in_db.hashed_password):
                return None
            
            # Return user without password
            return User(**user_doc)
        except Exception as e:
            logger.error("Error authenticating user", email=email, error=str(e))
            return None

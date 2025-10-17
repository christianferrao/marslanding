"""MongoDB connection and configuration."""

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo.errors import ConnectionFailure

from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)

# Global database client
client: AsyncIOMotorClient = None
database: AsyncIOMotorDatabase = None


async def connect_to_mongo() -> None:
    """Create database connection."""
    global client, database
    
    try:
        client = AsyncIOMotorClient(
            settings.MONGODB_URL,
            maxPoolSize=settings.MONGODB_MAX_CONNECTIONS,
            minPoolSize=settings.MONGODB_MIN_CONNECTIONS,
        )
        
        # Test the connection
        await client.admin.command('ping')
        
        database = client[settings.MONGODB_DATABASE]
        logger.info("Successfully connected to MongoDB")
        
    except ConnectionFailure as e:
        logger.error("Failed to connect to MongoDB", error=str(e))
        raise


async def close_mongo_connection() -> None:
    """Close database connection."""
    global client
    
    if client:
        client.close()
        logger.info("Disconnected from MongoDB")


def get_database() -> AsyncIOMotorDatabase:
    """Get database instance."""
    if database is None:
        raise RuntimeError("Database not initialized. Call connect_to_mongo() first.")
    return database


def get_collection(collection_name: str):
    """Get a collection from the database."""
    db = get_database()
    return db[collection_name]

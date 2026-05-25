from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection

from src.config.settings import settings


_client: MongoClient | None = None


def get_mongo_client() -> MongoClient:
    """
    Creates and returns a MongoDB client.
    Reuses the same client during the app lifecycle.
    """
    global _client

    if _client is None:
        if not settings.MONGO_URI:
            raise ValueError("MONGO_URI is missing. Please check your .env file.")

        _client = MongoClient(settings.MONGO_URI)

    return _client


def get_database() -> Database:
    """
    Returns the configured MongoDB database.
    """
    client = get_mongo_client()
    return client[settings.MONGO_DB_NAME]


def get_ticket_collection() -> Collection:
    """
    Returns the tickets collection.
    """
    db = get_database()
    return db[settings.MONGO_TICKET_COLLECTION]


def close_mongo_connection() -> None:
    """
    Closes MongoDB connection.
    Useful for tests or graceful shutdown.
    """
    global _client

    if _client is not None:
        _client.close()
        _client = None
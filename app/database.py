# from motor.motor_asyncio import AsyncIOMotorClient
# from dotenv import load_dotenv
# import os

# # Load .env file
# load_dotenv()

# # Retrieve MONGO_URL
# MONGO_URL = os.getenv('MONGO_URL')
# if not MONGO_URL:
#     raise ValueError("MONGO_URL is not set in the environment variables or .env file")

# print(f"Connecting to MongoDB with URL: {MONGO_URL}")

# # MongoDB Client
# client = AsyncIOMotorClient(MONGO_URL)
# db = client.student_management  # Database name


# from motor.motor_asyncio import AsyncIOMotorClient

# client = None
# db = None

# async def connect_to_mongo(mongo_url, db_name):
#     global client, db
#     client = AsyncIOMotorClient(mongo_url)
#     db = client[db_name]
#     print("Connected to MongoDB!")

# async def close_mongo_connection():
#     global client
#     if client:
#         client.close()
#         print("Disconnected from MongoDB!")
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional
from fastapi import HTTPException
import logging

# Initialize logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global variables for the MongoDB client and database
client: Optional[AsyncIOMotorClient] = None
db: Optional = None

# Connect to MongoDB
async def connect_to_mongo(mongo_url: str, db_name: str):
    """
    Establish a connection to the MongoDB database.

    :param mongo_url: MongoDB connection URL
    :param db_name: Name of the database to use
    """
    global client, db  # Declare global variables before use
    try:
        # Validate input parameters
        print(db)
        if not mongo_url or not db_name:
            raise ValueError("MongoDB connection URL or database name is missing.")

        client = AsyncIOMotorClient(mongo_url)
        db = client[db_name]

        print("This is client "," ",client)
        print("this is db  " , " ", db)

        # Test the connection
        
        await db.command("ping")  # Pings the MongoDB server to confirm connection
        logger.info("Successfully connected to MongoDB!")
        
    except Exception as e:
        logger.error(f"Error connecting to MongoDB: {e}")
        raise Exception("Failed to connect to MongoDB.") from e

# Close MongoDB connection
async def close_mongo_connection():
    """
    Close the connection to the MongoDB database.
    """
    global client, db  # Declare global variables before use
    if client:
        try:
            client.close()
            logger.info("Disconnected from MongoDB!")
        except Exception as e:
            logger.error(f"Error closing MongoDB connection: {e}")
        finally:
            # Clean up the global variables
            client = None
            db = None
    else:
        logger.warning("No active MongoDB connection to close.")


def get_database():
    print("this is db in database.py ", db)
    if db is None:
        raise ValueError("Database is not initialized. Did you call `connect_to_mongo()`?")
    return db



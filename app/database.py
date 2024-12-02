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
from motor.motor_asyncio import AsyncIOMotorClient

client = None
db = None

async def connect_to_mongo(mongo_url, db_name):
    global client, db
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    print("Connected to MongoDB!")

async def close_mongo_connection():
    global client
    if client:
        client.close()
        print("Disconnected from MongoDB!")

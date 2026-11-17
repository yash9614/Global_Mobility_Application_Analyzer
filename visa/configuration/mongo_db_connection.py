import os
from pymongo import MongoClient

def get_mongo_client():
    url = os.getenv("MONGODB_URL")
    if not url:
        raise ValueError("MONGODB_URL not set")
    return MongoClient(url)

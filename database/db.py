"""
Connects to the MongoDB database
"""
import os

from pymongo import MongoClient
from dotenv import load_dotenv

CXN = None
DB = None

uri = os.getenv("MONGODB_URI").format(
        os.getenv("MONGODB_USER"), os.getenv("MONGODB_PASSWORD")
    )
port = os.getenv("MONGODB_PORT")

if port is None:
    CXN = MongoClient(uri, serverSelectionTimeoutMS=3000)
else:
    CXN = MongoClient(uri, port=port, serverSelectionTimeoutMS=3000)
DB = CXN[os.getenv("MONGODB_DATABASE")]

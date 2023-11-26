"""
Functions for retrieving host information and connecting to MongoDB databases
"""

import os

from pymongo import MongoClient
from dotenv import load_dotenv


def load_uri():
    load_dotenv()

    # Create a new client and connect to the server
    uri = os.getenv("MONGODB_URI").format(
        os.getenv("MONGODB_USER"), os.getenv("MONGODB_PASSWORD")
    )
    port = int(os.getenv("MONGODB_PORT"))

    return [uri, port]


def load_client(uri, port=None):
    if port is None:
        client = MongoClient(uri, serverSelectionTimeoutMS=3000)
    else:
        client = MongoClient(uri, port=port, serverSelectionTimeoutMS=3000)

    return client


def connect_mongo(client):
    DB = None

    # Send a ping to confirm a successful connection
    try:
        client.admin.command("ping")
        DB = client[os.getenv("MONGODB_DATABASE")]
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:  # pylint: disable=broad-except
        print(e)
        DB = None

    return DB

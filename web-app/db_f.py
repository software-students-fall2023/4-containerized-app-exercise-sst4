"""
Functions for retrieving host information and connecting to MongoDB databases
"""

import os

from pymongo import MongoClient
from dotenv import load_dotenv


def load_uri():
    """
    Creates a uri from the .env and optionally a port and returns them as a string array.
    @return: An array of string where element 0 is the uri with the user and password and element 1 is the port.
    """
    load_dotenv()

    # Create a new client and connect to the server
    uri = os.getenv("MONGODB_URI").format(
        os.getenv("MONGODB_USER"), os.getenv("MONGODB_PASSWORD")
    )
    port = os.getenv("MONGODB_PORT")
    if port is not None:
        port = int(port)

    return [uri, port]


def load_client(uri, port=None):
    """
    Creates a MongoClient from a uri and optionally a port.
    @param uri: A string representing an address to a Mongo Database
    @param port: A port from which to access the address.
    @return: The created MongoClient
    """
    if port is None:
        client = MongoClient(uri, serverSelectionTimeoutMS=3000)
    else:
        client = MongoClient(uri, port=port, serverSelectionTimeoutMS=3000)

    return client


def connect_mongo(client):
    """
    Connects to the Mongo database specified by the client, thrown an Exception if fails.
    @param client: An initialized MongoClient
    @return: The connection to the database.
    """
    db = None

    # Send a ping to confirm a successful connection
    try:
        client.admin.command("ping")
        db = client[os.getenv("MONGODB_DATABASE")]
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:  # pylint: disable=broad-except
        print(' *', "Failed to connect to MongoDB at", os.getenv('MONGO_URI'))
        print('Database connection error:', e)  # debug
        db = None

    return db

"""
Connects to the MongoDB database
"""
import os
import pymongo

from dotenv import load_dotenv

CXN = None
DB = None

def connect(): # pylint: disable=inconsistent-return-statements
    '''Connects to the MongoDB database'''
    global CXN, DB # pylint: disable=global-statement
    if CXN is not None:
        return
    load_dotenv()  # take environment variables from .env.

    # connect to the database
    CXN = pymongo.MongoClient(os.getenv('MONGO_URI'),
                            serverSelectionTimeoutMS=5000)

    try:
        # verify the connection works by pinging the database
        # The ping command is cheap and does not require auth.
        CXN.admin.command('ping')
        DB = CXN[os.getenv('MONGO_DBNAME')]  # store a reference to the database
        # if we get here, the connection worked!
        print(' *', 'Connected to MongoDB!')
        return DB
    except Exception as e: # pylint: disable=broad-except
        # the ping command failed, so the connection is not available.
        print(' *', "Failed to connect to MongoDB at", os.getenv('MONGO_URI'))
        print('Database connection error:', e)  # debug
        return None


connect()

"""
Connects to the MongoDB database
"""

import db_f

CXN = None
DB = None


def connect():
    """
    Connect to a MongoDB database from the information stored in the .env
    """
    global CXN, DB
    if CXN is not None:
        return

    load = db_f.load_uri()
    CXN = db_f.load_client(load[0], load[1])
    DB = db_f.connect_mongo(client=CXN)


connect()

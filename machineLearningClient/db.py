"""
Connects to the MongoDB database
"""

import db_f

CXN = None
DB = None

load = db_f.load_uri()
CXN = db_f.load_client(load[0], load[1])
DB = db_f.connect_mongo(client=CXN)

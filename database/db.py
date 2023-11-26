"""
Connects to the MongoDB database
"""

import db_f

cxn = None
db = None


def connect():
    global cxn, db
    if cxn is not None:
        return

    load = db_f.load_uri()
    cxn = db_f.load_client(load[0], load[1])
    db = db_f.connect_mongo(client=cxn)


#connect()
load = db_f.load_uri()
cxn = db_f.load_client(load[0])
print(cxn)
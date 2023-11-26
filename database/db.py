"""
Connects to the MongoDB database
"""

import db_f

load = db_f.load_uri()
db_f.connect_docker(db_f.load_client(load[0], load[1]))

"""
Unit tests for db.py and db_f.py
"""

from io import StringIO
import tempfile
import pytest
from dotenv import load_dotenv
from database import db_f


# tests for load_uri()
def test_uri_loads():
    uri = db_f.load_uri()[0]
    assert uri is not None


def test_port_loads():
    port = db_f.load_uri()[1]
    assert port is not None


# tests for load_client()
def test_client_connects_no_port():
    uri = "mongo"
    cxn = db_f.load_client(uri)
    assert str(cxn) == ("MongoClient(host=['mongo:27017'], document_class=dict, tz_aware=False, connect=True, serverselectiontimeoutms=3000)")

def test_client_connects_port():
    cxn = db_f.load_client("mongo", 27017)
    assert str(cxn) == ("MongoClient(host=['mongo:27017'], document_class=dict, tz_aware=False, connect=True, serverselectiontimeoutms=3000)")

# tests for connect_mongo()
def test_connect():
    cxn = db_f.load_client("mongodb://mongo:27017/", 27017)
    db = db_f.connect_mongo(cxn)

    assert db is not None

def test_fail_connect():
    cxn = db_f.load_client("bad", 27017)
    db = db_f.connect_mongo(cxn)

    assert db is None

def test_connects_from_docker():
    from database import db
    assert db is not None
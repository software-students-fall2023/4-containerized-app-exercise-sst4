from io import StringIO
import tempfile
import pytest
from dotenv import load_dotenv


def test_envLoads():
    # load_dotenv()
    from database import db

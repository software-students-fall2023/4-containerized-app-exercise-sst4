"""
Unit tests for the Web App
"""
import io
import os
import pytest

from unittest.mock import Mock, patch
from web_app.app import app

CURR_DIR = os.path.dirname(os.path.abspath(__file__))


@pytest.fixture
def client():
    """configuring Flask application to run in testing"""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_index_template(client):
    """Test the index page view."""
    response = client.get("/")
    assert response.status_code == 200


def test_recognize_no_input(client):
    """Test the regonize post feature without image."""
    response = client.post("/recognize")
    assert b"error" in response.data


def test_recognize(client):
    """Test the regonize post feature with image."""
    image_data = io.open(CURR_DIR + "/test_encoding_0.txt", "r").readline()
    mock_request = Mock()
    mock_request.get_json.return_value = {"image": image_data}
    with patch("web_app.app.request", new=mock_request):
        response = client.post("/recognize")
        assert response.status_code == 200


def test_register_no_input(client):
    """Test the register feature without image."""
    response = client.post("/register")
    assert b"error" in response.data


def test_register(client):
    """Test register post feature."""
    image_data = io.open(CURR_DIR + "/test_encoding_0.txt", "r").readline()
    mock_request = Mock()
    mock_request.get_json.return_value = {"image": image_data, "name": "test"}
    with patch("web_app.app.request", new=mock_request):
        response = client.post("/register")
        assert response.status_code == 200

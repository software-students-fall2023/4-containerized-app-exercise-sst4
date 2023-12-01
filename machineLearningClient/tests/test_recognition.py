"""
Unit tests for the Machine Learning Client
"""
import io
import base64
import unittest
import pytest
from unittest.mock import Mock, patch

from machineLearningClient import recognition

@pytest.fixture()
def app():
    app = recognition.recognize_app
    app.config.update({
        "TESTING": True,
    })

    yield app


def test_finds_face(app):
    """Tests that recognition method finds a face."""
    image_data = io.open("test_encoding_0.txt", 'r')
    image_data = image_data.readline()
    mock_request = Mock()
    mock_request.get_json.return_value = json = {"image": image_data}
    with patch("machineLearningClient.recognition.request", new=mock_request):
        with patch("machineLearningClient.recognition.users"):
            with patch("machineLearningClient.recognition.jsonify", new=mock_request):
                response = recognition.recognize_user()
                assert response.status_code == 200

def test_finds_no_face(self, mock_requests):
    """Tests that recognition method does not find a face."""

def test_face_recognized(self, mock_requests):
    """Tests that recognition method recognizes a face from the database."""

def test_face_not_recognized(self, mock_requests):
    """Tests that recognition method does not match face with face from database."""

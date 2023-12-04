"""
Unit tests for the Machine Learning Client
"""
import io
import os

import pytest
from unittest.mock import Mock, patch
from machine_learning_client import recognition

CURR_DIR = os.path.dirname(os.path.abspath(__file__))


@pytest.fixture()
def app():
    app = recognition.recognize_app
    app.config.update(
        {
            "TESTING": True,
        }
    )

    yield app


def test_finds_face(app):
    """Tests that recognition method finds a face."""
    test_lines = io.open(CURR_DIR + "/test_encoding_0.txt", "r")
    image_data = test_lines.readline()
    mock_request = Mock()
    mock_request.get_json.return_value = {"image": image_data}
    mock_jsonify = Mock()
    with patch("machine_learning_client.recognition.request", new=mock_request):
        with patch("machine_learning_client.recognition.users"):
            with patch("machine_learning_client.recognition.jsonify", new=mock_jsonify):
                response = recognition.recognize_user()
                assert response.status_code == 200
                mock_jsonify.assert_called_with({"message": "Face Not Recognized"})


def test_finds_no_face(app):
    """Tests that recognition method does not find a face."""
    test_lines = io.open(CURR_DIR + "/test_encoding_1.txt", "r")
    image_data = test_lines.readline()
    mock_request = Mock()
    mock_request.get_json.return_value = {"image": image_data}
    mock_jsonify = Mock()
    with patch("machine_learning_client.recognition.request", new=mock_request):
        with patch("machine_learning_client.recognition.users"):
            with patch("machine_learning_client.recognition.jsonify", new=mock_jsonify):
                response = recognition.recognize_user()
                assert response.status_code == 200
                mock_jsonify.assert_called_with(
                    {"message": "No faces found in the captured image."}
                )


def test_face_recognized(app):
    """Tests that recognition method recognizes a face from the database."""
    test_lines = io.open(CURR_DIR + "/test_encoding_0.txt", "r")
    image_data = test_lines.readline()
    mock_request = Mock()
    mock_request.get_json.return_value = {"image": image_data}
    mock_jsonify = Mock()
    mock_users = Mock()
    mock_users.find.return_value = [{"image": image_data, "name": "Obama"}]
    with patch("machine_learning_client.recognition.request", new=mock_request):
        with patch("machine_learning_client.recognition.users", new=mock_users):
            with patch("machine_learning_client.recognition.jsonify", new=mock_jsonify):
                response = recognition.recognize_user()
                assert response.status_code == 200
                mock_jsonify.assert_called_with(
                    {"message": "Face Recognized! Hello Obama"}
                )


def test_face_not_recognized(app):
    """Tests that recognition method does not match face with face from database."""
    test_lines = io.open(CURR_DIR + "/test_encoding_0.txt", "r")
    image_data = test_lines.readline()
    test_lines1 = io.open(CURR_DIR + "/test_encoding_2.txt", "r")
    image_data1 = test_lines1.readline()
    mock_request = Mock()
    mock_request.get_json.return_value = {"image": image_data}
    mock_jsonify = Mock()
    mock_users = Mock()
    mock_users.find.return_value = [{"image": image_data1, "name": "Obama"}]
    with patch("machine_learning_client.recognition.request", new=mock_request):
        with patch("machine_learning_client.recognition.users", new=mock_users):
            with patch("machine_learning_client.recognition.jsonify", new=mock_jsonify):
                response = recognition.recognize_user()
                assert response.status_code == 200
                mock_jsonify.assert_called_with({"message": "Face Not Recognized"})

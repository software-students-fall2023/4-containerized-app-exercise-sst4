"""
Machine Learning Client
"""
import base64
import cv2
import face_recognition
import numpy as np

from flask import Flask, request, jsonify

from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = "mongodb://mongodb:27017/"

client = MongoClient(MONGO_URI)
db = client["database1"]
users = db["users"]

recognize_app = Flask(__name__)


@recognize_app.route("/test", methods=["POST"])
def recognize_user():  # pylint: disable=too-many-locals
    """Returns ML client data from trying to recognize the user."""
    users_find = users.find({})

    data = request.get_json()
    user = data.get("image")

    image_bytes = base64.b64decode(user.split(",")[1])

    image_np = np.frombuffer(image_bytes, dtype=np.uint8)

    img = cv2.imdecode(image_np, cv2.IMREAD_COLOR)

    # Convert BGR to RGB
    rgb_frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    if not face_encodings:
        response = jsonify({"message": "No faces found in the captured image."})
        response.status_code = 200
        return response

    for document in users_find:
        reference_image = document["image"]

        reference_bytes = base64.b64decode(reference_image.split(",")[1])

        reference_np = np.frombuffer(reference_bytes, dtype=np.uint8)

        ref_img = cv2.imdecode(reference_np, cv2.IMREAD_COLOR)

        rgb_frame = cv2.cvtColor(ref_img, cv2.COLOR_BGR2RGB)

        ref_face_locations = face_recognition.face_locations(rgb_frame)
        reference_encodings = face_recognition.face_encodings(
            rgb_frame, ref_face_locations
        )

        results = face_recognition.compare_faces(
            reference_encodings, face_encodings[0], tolerance=0.4
        )

        if results[0]:  # Should only be here if match
            name = document["name"]
            message = "Face Recognized! Hello " + name
            response = jsonify({"message": message})
            response.status_code = 200
            return response
    response = jsonify({"message": "Face Not Recognized"})
    response.status_code = 200
    return response


if __name__ == "__main__":
    recognize_app.run(debug=True, host="0.0.0.0", port=6000)

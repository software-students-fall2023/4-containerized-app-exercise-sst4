"""
Machine Learning Client
"""
import base64
import cv2
import face_recognition
import numpy as np

from flask import Flask, request, jsonify

import os

from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

CXN = None
DB = None

uri = os.getenv("MONGODB_URI").format(
        os.getenv("MONGODB_USER"), os.getenv("MONGODB_PASSWORD")
    )
port = os.getenv("MONGODB_PORT")

if port is None:
    CXN = MongoClient(uri, serverSelectionTimeoutMS=3000)
else:
    CXN = MongoClient(uri, port=port, serverSelectionTimeoutMS=3000)
DB = CXN[os.getenv("MONGODB_DATABASE")]

recognize_app = Flask(__name__)

@recognize_app.route("/recognize", methods=["POST"])
def recognize_user(): # pylint: disable=too-many-locals
    '''Returns ML client data from trying to recognize the user.'''

    data = request.get_json() # Recieves image from frontend
    user = data.get('image')

    image_bytes = base64.b64decode(user.split(',')[1])

    image_np = np.frombuffer(image_bytes, dtype=np.uint8) #new

    img = cv2.imdecode(image_np, cv2.IMREAD_COLOR) #new

    # Convert BGR to RGB
    rgb_frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) #new

    face_locations = face_recognition.face_locations(rgb_frame) #new
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations) #new

    if not face_encodings:
        return jsonify({"message":'No faces found in the captured image.'})

    users_collection = DB["users"]
    users_find = users_collection.find({}) # Finds all users
    for document in users_find: #Cycles through all users
        reference_image = document["image"] # Gets the image for each user

        #Same as above removes the first part
        reference_bytes = base64.b64decode(reference_image.split(',')[1])

        reference_np = np.frombuffer(reference_bytes, dtype=np.uint8) #new

        ref_img = cv2.imdecode(reference_np, cv2.IMREAD_COLOR) #new

        rgb_frame = cv2.cvtColor(ref_img, cv2.COLOR_BGR2RGB) #new

        ref_face_locations = face_recognition.face_locations(rgb_frame) #new
        reference_encodings = face_recognition.face_encodings(rgb_frame, ref_face_locations) #new

        results = face_recognition.compare_faces(reference_encodings, face_encodings[0],
                                                 tolerance=0.4)

        if results[0]: # Should only be here if match
            name = document["name"]
            message = "Face Recognized! Hello " + name
            return jsonify({"message": message})
    return jsonify({"message": "Face Not Recognized"}) # Not recognized

if __name__ == "__main__":
    recognize_app.run(debug=True, host="0.0.0.0", port=6000)

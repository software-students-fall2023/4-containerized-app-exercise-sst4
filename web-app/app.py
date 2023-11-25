# app.py

import os
import requests
import base64

from flask import Flask, render_template, request, jsonify
from PIL import Image
from io import BytesIO
import io
import face_recognition
import sys
sys.path.append('/Users/richardli/Desktop/swe/4-containerized-app-exercise-sst4')

from machineLearningClient import recognition
from database.db import db

app = Flask(__name__)

usersCollection = db["users"]



def get_user_data():
    # image_path = os.path.join(app.static_folder, "richard.jpg")
    
    # with open(image_path, "rb") as image_file:
    #     base64_image = base64.b64encode(image_file.read()).decode('utf-8')
    
    # return base64_image
    image_path = os.path.join(app.static_folder, "richard.jpg")
    return image_path

def get_user_data_two():
    # image_path = os.path.join(app.static_folder, "richard.jpg")
    
    # with open(image_path, "rb") as image_file:
    #     base64_image = base64.b64encode(image_file.read()).decode('utf-8')
    
    # return base64_image
    image_path = os.path.join(app.static_folder, "obama.jpg")
    image = Image.open(image_path)
    return image_path


@app.route("/")
def index():
    return render_template("index.html")

reference_image_path = get_user_data_two()
reference_image = face_recognition.api.load_image_file(reference_image_path)
reference_encoding = face_recognition.face_encodings(reference_image)[0]

@app.route("/recognize", methods=["POST"])
def recognize_user_api():
    try:
        data = request.get_json()
        image_data = data.get('image')

        image_bytes = base64.b64decode(image_data.split(',')[1])
        image = Image.open(io.BytesIO(image_bytes))

        image_np = face_recognition.api.load_image_file(io.BytesIO(image_bytes))

        face_encodings = face_recognition.face_encodings(image_np)

        if not face_encodings:
            return jsonify({'message': 'No faces found in the captured image.'})

        results = face_recognition.compare_faces([reference_encoding], face_encodings[0])

        if results[0]:
            response = {'message': 'Face recognized!'}
        else:
            response = {'message': 'Face not recognized.'}

        return jsonify(response)

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == "__main__":
    app.run(debug=True)

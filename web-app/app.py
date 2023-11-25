# app.py

import os
import requests
import base64

from flask import Flask, render_template, request, jsonify
from PIL import Image
from io import BytesIO
import io
import face_recognition
from bson.binary import Binary
import sys

current_script_path = os.path.abspath(__file__)

# Navigate to the project directory
project_path = os.path.dirname(os.path.dirname(current_script_path))

# Add the project directory to the sys.path
sys.path.append(project_path)

# sys.path.append('/Users/richardli/Desktop/swe/4-containerized-app-exercise-sst4')

from machineLearningClient import recognition
from database.db import db

app = Flask(__name__)

usersCollection = db["users"] # Collection for users



# def get_user_data():
#     # image_path = os.path.join(app.static_folder, "richard.jpg")
    
#     # with open(image_path, "rb") as image_file:
#     #     base64_image = base64.b64encode(image_file.read()).decode('utf-8')
    
#     # return base64_image
#     image_path = os.path.join(app.static_folder, "richard.jpg")
#     return image_path

# def get_user_data_two():
#     # image_path = os.path.join(app.static_folder, "richard.jpg")
    
#     # with open(image_path, "rb") as image_file:
#     #     base64_image = base64.b64encode(image_file.read()).decode('utf-8')
    
#     # return base64_image
#     image_path = os.path.join(app.static_folder, "obama.jpg")
#     image = Image.open(image_path)
#     return image_path


@app.route("/") # Route for /
def index():
    return render_template("index.html")
@app.route("/register") # Route for Register
def register():
    return render_template("register.html")

# reference_image_path = get_user_data_two()
# reference_image = face_recognition.api.load_image_file(reference_image_path)
# reference_encoding = face_recognition.face_encodings(reference_image)[0]

@app.route("/recognize", methods=["POST"]) # Post method for recognize
def recognize_user_api():
    try:
        # image_binary = base64.b64encode(get_user_data_two.read()).decode('utf-8')

        # # Insert the Base64-encoded image into MongoDB
        # data = {'image': image_binary}
        # usersCollection.insert_one(data)

        # # data = {'image': image_binary}
        # # usersCollection.insert_one(data)
        # return jsonify({"image": "people"})

        data = request.get_json() # Recieves image from frontend
        image_data = data.get('image')

        results = recognition.recognize_user(image_data) # passes the users image to recognition

        return jsonify({"message": results})

    except Exception as e:
        return jsonify({'error': str(e)})
    
@app.route("/register", methods=["POST"])
def register_user():
    req = request.get_json() # Recieves name and image from user
    image_data = req["image"]
    name_data = req["name"]
    data = {'image': image_data, "name": name_data}
    usersCollection.insert_one(data) # Pushes it to mongoDB

    return jsonify({"world": "hello"}) # Dummy response for now

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

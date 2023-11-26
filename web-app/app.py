"""
Web app for the face recognition project.
"""
import os
import sys

from flask import Flask, render_template, request, jsonify

current_script_path = os.path.abspath(__file__)

# Navigate to the project directory
project_path = os.path.dirname(os.path.dirname(current_script_path))

# Add the project directory to the sys.path
sys.path.append(project_path)

import os # pylint: disable=wrong-import-position

from pymongo import MongoClient # pylint: disable=wrong-import-position
from dotenv import load_dotenv # pylint: disable=wrong-import-position

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
from machineLearningClient import recognition # pylint: disable=wrong-import-position

app = Flask(__name__)

usersCollection = DB["users"] # Collection for users

@app.route("/") # Route for /

def index():
    '''Returns index page.'''
    return render_template("index.html")

@app.route("/register") # Route for Register

def register():
    '''Returns registration page.'''
    return render_template("register.html")

@app.route("/recognize", methods=["POST"]) # Post method for recognize
def recognize_user_api():
    '''Returns ML client data from trying to recognize the user.'''
    try:

        data = request.get_json() # Recieves image from frontend
        image_data = data.get('image')

        results = recognition.recognize_user(image_data) # passes the users image to recognition

        return jsonify({"message": results})

    except Exception as e: # pylint: disable=broad-except
        return jsonify({'error': str(e)})

@app.route("/register", methods=["POST"])
def register_user():
    '''Registers the user to the database.'''
    req = request.get_json() # Recieves name and image from user
    image_data = req["image"]
    name_data = req["name"]
    data = {'image': image_data, "name": name_data}
    usersCollection.insert_one(data) # Pushes it to mongoDB

    return jsonify({"world": "hello"}) # Dummy response for now

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

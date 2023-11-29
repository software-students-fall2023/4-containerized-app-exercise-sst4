"""
Web app for the face recognition project.
"""
import os
import sys
import requests

from flask import Flask, render_template, request, jsonify

current_script_path = os.path.abspath(__file__)

project_path = os.path.dirname(os.path.dirname(current_script_path))

sys.path.append(project_path)

from pymongo import MongoClient  # pylint: disable=wrong-import-position
from dotenv import load_dotenv  # pylint: disable=wrong-import-position

load_dotenv()

MONGO_URI = "mongodb://mongodb:27017/"

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client["database1"]

app = Flask(__name__)


@app.route("/")  # Route for /
def index():
    """Returns index page."""
    return render_template("index.html")


@app.route("/recognize", methods=["POST"])  # Post method for recognize
def recognize_user_api():
    """Returns ML client data from trying to recognize the user."""
    try:
        data = request.get_json()  # Recieves image from frontend
        image_data = data.get("image")

        ml_client_url = "http://machine_learning_client:6000/test"
        headers = {"Content-Type": "application/json"}
        ml_client_response = requests.post(
            ml_client_url, json={"image": image_data}, headers=headers, timeout=10
        )

        return ml_client_response.json()

    except Exception as e:  # pylint: disable=broad-except
        return jsonify({"error": str(e)})


@app.route("/register", methods=["POST"])
def register_user():
    """Registers the user to the database."""
    try:
        req = request.get_json()

        image_data = req["image"]
        name_data = req["name"]
        data = {"image": image_data, "name": name_data}
        db["users"].insert_one(data)

        return jsonify({"message": "Face was added to database"})
    except Exception as e:  # pylint: disable=broad-except
        return jsonify({"error": str(e)})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

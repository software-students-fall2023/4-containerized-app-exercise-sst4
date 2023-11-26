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

from machineLearningClient import recognition # pylint: disable=wrong-import-position
from db import DB # pylint: disable=wrong-import-position

# sys.path.append('/Users/richardli/Desktop/swe/4-containerized-app-exercise-sst4')
# sys.path.append('/Users/richardli/Desktop/swe/4-containerized-app-exercise-sst4')

app = Flask(__name__)

usersCollection = DB["users"] # Collection for users

# @app.route("/login", methods=["POST"])
# def login():
#     """login. POST with photo in body."""
#     # take image from body

#     bodystr = request.get_data(cache=False, as_text=True, parse_form_data=False)
#     imgdata = bodystr.split(";")[1].split(",")[1]
#     # use with PIL:
#     with Image.open(BytesIO(b64decode(imgdata))) as im:
#         print(im.size)
#         # im.show()

#     # @TODO send image to ML client
#     sleep(2)

#     # dummy return @TODO
#     status = "ok"
#     username = "TestUser123"
#     sid = "132uygsfd76f12"
#     content = "this is my private diary!!!\n~~~~\nI put all \
#         my secrets here and they will be locked with my face."
#     return {
#         "status": status,
#         "username": username,
#         "sid": sid,
#         "content": content,
#     }

@app.route("/") # Route for /

def index():
    '''Returns index page.'''
    return render_template("index.html")

@app.route("/register") # Route for Register

def register():
    '''Returns registration page.'''
    return render_template("register.html")

# reference_image_path = get_user_data_two()
# reference_image = face_recognition.api.load_image_file(reference_image_path)
# reference_encoding = face_recognition.face_encodings(reference_image)[0]

@app.route("/recognize", methods=["POST"]) # Post method for recognize
def recognize_user_api():
    '''Returns ML client data from trying to recognize the user.'''
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

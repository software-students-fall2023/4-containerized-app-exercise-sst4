"""
Machine Learning Client
"""
import base64
import cv2
import face_recognition
import numpy as np

from database.db import db

def recognize_user(user): # pylint: disable=too-many-locals
    '''Returns ML client data from trying to recognize the user.'''
    # Takes out the data:image/jpeg;base64, since frontend sends as jpeg
    image_bytes = base64.b64decode(user.split(',')[1])

    image_np = np.frombuffer(image_bytes, dtype=np.uint8) #new

    img = cv2.imdecode(image_np, cv2.IMREAD_COLOR) #new

    # Convert BGR to RGB
    rgb_frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) #new

    face_locations = face_recognition.face_locations(rgb_frame) #new
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations) #new

    if not face_encodings:
        return 'No faces found in the captured image.'

    users_collection = db["users"]
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

        # reference_np = face_recognition.api.load_image_file(io.BytesIO(reference_bytes))

        # reference_encodings = face_recognition.face_encodings(reference_np)
        # print(len(reference_encodings[0]))

        results = face_recognition.compare_faces(reference_encodings, face_encodings[0],
                                                 tolerance=0.4)

        if results[0]: # Should only be here if match
            name = document["name"]
            return "Face Recognized! Hello " + name # Returns name from mongo
    return "Face Not Recognized" # Not recognized

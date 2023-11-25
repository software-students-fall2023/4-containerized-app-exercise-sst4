# recognition.py

import base64
import cv2
import face_recognition
import numpy as np
from PIL import Image
import io
from io import BytesIO
from database.db import db
import binascii

def recognize_user(user):
    # try:
        image_bytes = base64.b64decode(user.split(',')[1]) # Takes out the data:image/jpeg;base64, since frontend sends as jpeg

        image_np = face_recognition.api.load_image_file(io.BytesIO(image_bytes)) # Loads the file as a bytefile

        face_encodings = face_recognition.face_encodings(image_np) #Does the libraries encoding preparing for comaprison

        if not face_encodings:
            return 'No faces found in the captured image.'

        usersCollection = db["users"]
        usersFind = usersCollection.find({}) # Finds all users
        for document in usersFind: #Cycles through all users
            reference_image = document["image"] # Gets the image for each user

            reference_bytes = base64.b64decode(reference_image.split(',')[1]) #Same as above removes the first part

            reference_np = face_recognition.api.load_image_file(io.BytesIO(reference_bytes))

            reference_encodings = face_recognition.face_encodings(reference_np)

            results = face_recognition.compare_faces(reference_encodings, face_encodings[0]) # Compares the two faces, not sure why one is [0] but i trialed and errored and this is what worked
        
            if results[0]: # Should only be here if match
                name = document["name"]
                return "Face Recognized! Hello " + name # Returns name from mongo
        return "Face Not Recognized" # Not recognized


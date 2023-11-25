# recognition.py

import base64
import cv2
import face_recognition
import numpy as np

def recognize_user(image_base64, user_data):
    try:
        known_image = face_recognition.load_image_file(image_base64)


        biden_encoding = face_recognition.face_encodings(known_image)[0]
        unknown_encoding = face_recognition.face_encodings(user_data)[0]

        results = face_recognition.compare_faces([biden_encoding], unknown_encoding)

        return results

    except Exception as e:
        return {"recognized": False, "name": "Error", "error": str(e)}

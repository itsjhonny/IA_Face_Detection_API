# This is a _very simple_ example of a web service that recognizes faces in uploaded images.
# Upload an image file and it will check if the image contains a picture of Barack Obama.
# The result is returned as json. For example:
#
# $ curl -XPOST -F "file=@obama2.jpg" http://127.0.0.1:5001
#
# Returns:
#
# {
#  "face_found_in_image": true,
#  "is_picture_of_obama": true
# }
#
# This example is based on the Flask file upload example: http://flask.pocoo.org/docs/0.12/patterns/fileuploads/

# NOTE: This example requires flask to be installed! You can install it with pip:
# $ pip3 install flask

import face_recognition
from flask import Flask, jsonify, request, redirect
import os
import sys
import numpy as np
# You can change this to any folder on your system
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_image():
    # Check if a valid image file was uploaded
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            return redirect(request.url)

        if file and allowed_file(file.filename):
            # The image file seems valid! Detect faces and return the result.
            return detect_faces_in_image(file)

    # If no valid image file was uploaded, show the file upload form:
    return '''
    <!doctype html>
    <title></title>
    <h1>John testes File</h1>
    <form method="POST" enctype="multipart/form-data">
      <input type="file" name="file">
      <input type="submit" value="Upload">
    </form>
    '''


dbImgs = []


def detect_faces_in_image(file_stream):
    # Pre-calculated face encoding of Obama generated with face_recognition.face_encodings(img)
    known_face_encoding = any

    # Load the uploaded image file
    img = face_recognition.load_image_file(file_stream)
    # Get face encodings for any faces in the uploaded image
    unknown_face_encodings = face_recognition.face_encodings(img)
    print(unknown_face_encodings)

    face_found = False

    if len(unknown_face_encodings) > 0:
        face_found = True
        result = {
            "face_found_in_image": face_found,
            "Pessoa": ''
        }

        for unknown_face in unknown_face_encodings:
            for img in dbImgs:
                for known_face_encoding in img['face_encoding']:
                    match_results = face_recognition.compare_faces(known_face_encoding, unknown_face)
                    face_distances = face_recognition.face_distance(known_face_encoding, unknown_face)
                    best_match_index = np.argmin(face_distances)
                    if(match_results[best_match_index]):
                        print(img['name'])
                        if(img['name'] not in result['Pessoa']):
                            result['Pessoa'] += img['name'] + ' '

    return '''<script src='https://code.responsivevoice.org/responsivevoice.js'></script> <input id='speak' onclick='responsiveVoice.speak(''' + '"' + result['Pessoa'] + '"' + ''', "Brazilian Portuguese Female");' type="button" value="🔊 Play" /> 
    <script>
    (function () {
    document.getElementById("speak").click();
})();</script>'''
    # See if the first face in the uploaded image matches the known face of Obama
    # print(img[0]['name'])

    # Return the result as json


def checkDB(DIR):

    if(len(os.listdir(DIR)) != len(dbImgs)):
        for index, name in enumerate(os.listdir(DIR)):
            modalImg = {
                'name': '', 'face_encoding': []
            }
            modalImg['name'] = name.replace("_", " ")
            dbImgs.append(modalImg)

            for picture in os.listdir(DIR + name):
                imgPath = DIR + name + '/' + picture
                image = face_recognition.load_image_file(imgPath)
                face_encoding = face_recognition.face_encodings(image)
                dbImgs[index]['face_encoding'].append(face_encoding)

    return app.run(host='0.0.0.0', port=5000, debug=True)


if __name__ == "__main__":
    checkDB('DBimagens/')

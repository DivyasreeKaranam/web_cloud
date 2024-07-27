from flask import Flask, render_template, request, jsonify, Response
from camera import Camera
from face_recognition import FaceRecognition
import cv2
import numpy as np

app = Flask(__name__)
camera = Camera()
face_recognition = FaceRecognition()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

def gen_frames():
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/take_images', methods=['POST'])
def take_images():
    id = request.form.get('id')
    name = request.form.get('name')
    images = []
    for _ in range(5):  # Take 5 images
        frame = camera.get_frame()
        images.append(frame)
    face_recognition.save_face(id, name, images)
    return jsonify({"success": True, "message": "Images captured successfully"})

@app.route('/save_profile', methods=['POST'])
def save_profile():
    face_recognition.train_model()
    return jsonify({"success": True, "message": "Profile saved successfully"})

@app.route('/track_images', methods=['POST'])
def track_images():
    frame = camera.get_frame()
    attendance = face_recognition.recognize_face(frame)
    return jsonify({"success": True, "attendance": attendance})

if __name__ == '__main__':
    app.run(debug=True)
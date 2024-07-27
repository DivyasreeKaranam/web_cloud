import cv2
import numpy as np
import os

class FaceRecognition:
    def __init__(self):
        self.recognizer = cv2.face_LBPHFaceRecognizer.create()
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.id_name_map = {}

    def save_face(self, id, name, images):
        if not os.path.exists('dataset'):
            os.makedirs('dataset')
        for i, image_bytes in enumerate(images):
            nparr = np.frombuffer(image_bytes, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                cv2.imwrite(f"dataset/{name}.{id}.{i}.jpg", gray[y:y+h, x:x+w])
        self.id_name_map[id] = name

    def train_model(self):
        path = 'dataset'
        faces, ids = [], []
        for filename in os.listdir(path):
            if filename.endswith('.jpg'):
                img = cv2.imread(os.path.join(path, filename), 0)
                id = int(filename.split('.')[1])
                faces.append(img)
                ids.append(id)
        self.recognizer.train(faces, np.array(ids))
        self.recognizer.save('trainer.yml')

    def recognize_face(self, image_bytes):
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            id, confidence = self.recognizer.predict(gray[y:y+h, x:x+w])
            if confidence < 50:
                name = self.id_name_map.get(str(id), "Unknown")
                return {"id": id, "name": name}
        return None
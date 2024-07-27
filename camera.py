import cv2

class Camera:
    def __init__(self):
        self.camera = cv2.VideoCapture(0)

    def get_frame(self):
        success, frame = self.camera.read()
        if not success:
            return None
        ret, buffer = cv2.imencode('.jpg', frame)
        return buffer.tobytes()

    def __del__(self):
        self.camera.release()
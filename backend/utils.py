import cv2
import numpy as np

def preprocess(frame):
    frame = cv2.resize(frame, (64, 64))
    frame = frame / 255.0
    return frame


def encode_image(frame):
    _, buffer = cv2.imencode(".jpg", frame)
    return buffer.tobytes()


def decode_image(bytes_data):
    npimg = np.frombuffer(bytes_data, np.uint8)
    return cv2.imdecode(npimg, cv2.IMREAD_COLOR)
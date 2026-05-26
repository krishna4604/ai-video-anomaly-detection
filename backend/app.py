from flask import Flask, Response, jsonify
import cv2
import time
import threading
import os

from detector import detect_objects
from model import load_model, get_score
from database import init_db, insert_log
from telegram_bot import send_alert

app = Flask(__name__)

init_db()
model = load_model()

THRESHOLD = 0.001
ALERT_COOLDOWN = 10

last_alert = 0
latest_frame = None

os.makedirs("data/anomalies", exist_ok=True)

camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)

if not camera.isOpened():
    print("Camera failed")
    exit()


def ai_loop():
    global latest_frame
    global last_alert

    while True:

        success, frame = camera.read()

        if not success:
            continue

        latest_frame = frame.copy()

        crops = detect_objects(frame)

        scores=[]

        for crop in crops:
            try:
                score=get_score(model,crop)
                scores.append(score)
            except:
                pass

        if len(scores)==0:
            continue

        final_score=max(scores)

        anomaly=final_score>THRESHOLD

        if anomaly:

            cv2.putText(
                frame,
                "ANOMALY",
                (20,40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0,0,255),
                2
            )

            if time.time()-last_alert > ALERT_COOLDOWN:

                last_alert=time.time()

                filename=f"data/anomalies/{int(time.time())}.jpg"

                cv2.imwrite(filename,frame)

                try:
                    send_alert(filename,final_score)
                except Exception as e:
                    print(e)


threading.Thread(
    target=ai_loop,
    daemon=True
).start()


@app.route("/")
def home():
    return "Backend running"


@app.route("/video")
def video():

    def generate():

        global latest_frame

        while True:

            if latest_frame is None:
                continue

            _,buffer=cv2.imencode(
                '.jpg',
                latest_frame
            )

            frame=buffer.tobytes()

            yield(
                b'--frame\r\n'
                b'Content-Type:image/jpeg\r\n\r\n'
                +frame+
                b'\r\n'
            )

    return Response(
        generate(),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )


@app.route("/status")
def status():
    return jsonify({
        "camera":"online"
    })


if __name__=="__main__":
    app.run(port=5001)
import cv2
import requests
import threading

API_URL = "http://127.0.0.1:5001/predict"

latest_frame = None

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

if not cap.isOpened():
    print("Camera not accessible")
    exit()


def process_ai(frame):
    _, img_encoded = cv2.imencode(".jpg", frame)

    try:
        response = requests.post(
            API_URL,
            files={"image": img_encoded.tobytes()},
            timeout=5
        )

        result = response.json()

        anomaly = result["anomaly"]
        score = result["score"]

        if anomaly:
            cv2.putText(
                frame,
                f"ANOMALY {score:.4f}",
                (20,40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0,0,255),
                2
            )
        else:
            cv2.putText(
                frame,
                f"NORMAL {score:.4f}",
                (20,40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0,255,0),
                2
            )

    except Exception as e:
        print(e)


while True:

    ret, frame = cap.read()

    if not ret:
        break

    latest_frame = frame.copy()

    threading.Thread(
        target=process_ai,
        args=(frame.copy(),),
        daemon=True
    ).start()

    cv2.imshow("AI Surveillance", frame)

    if cv2.waitKey(1) == ord("q"):
        break


cap.release()
cv2.destroyAllWindows()
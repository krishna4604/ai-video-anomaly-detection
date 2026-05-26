from ultralytics import YOLO

yolo = YOLO("yolov8n.pt")


def detect_objects(frame):
    results = yolo(frame, verbose=False)

    crops = []

    for r in results:
        for box in r.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])

            crop = frame[y1:y2, x1:x2]

            if crop is not None and crop.size != 0:
                crops.append(crop)

    return crops
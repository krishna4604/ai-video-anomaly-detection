import cv2
import numpy as np
import os

from telegram_bot import send_alert

os.makedirs("data/anomalies", exist_ok=True)

img = np.zeros((300,300,3), dtype=np.uint8)

path = "data/anomalies/test.jpg"

cv2.imwrite(path, img)

send_alert(path, 0.99)
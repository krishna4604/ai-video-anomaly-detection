import requests
import os

BOT_TOKEN = "8938543900:AAFbpzQ4kJ66JcCoodXi8CtNonnQG78Gi6k"
CHAT_ID = "5409847398"


def send_alert(image_path, score):

    print("[TELEGRAM] Triggered")

    if not os.path.exists(image_path):
        print("[TELEGRAM] Image missing")
        return

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"

    try:
        with open(image_path, "rb") as img:
            response = requests.post(
                url,
                data={
                    "chat_id": CHAT_ID,
                    "caption": f"🚨 ANOMALY DETECTED\nScore: {score}"
                },
                files={"photo": img}
            )

        print("[TELEGRAM RESPONSE]", response.text)

    except Exception as e:
        print("[TELEGRAM ERROR]", e)
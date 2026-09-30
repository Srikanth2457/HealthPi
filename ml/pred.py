import os
import time

import joblib
import requests

MODEL_PATH = os.getenv("MODEL_PATH", "vehicle_monitoring_model.pkl")
THINGSPEAK_URL = os.getenv(
    "THINGSPEAK_URL",
    "https://api.thingspeak.com/channels/3516531/feeds.json?results=1",
)
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


def get_thingspeak_data():
    response = requests.get(THINGSPEAK_URL, timeout=10)
    response.raise_for_status()
    data = response.json()
    if not data.get("feeds"):
        print("No ThingSpeak data available yet.")
        return None

    feeds = data["feeds"][0]

    engine_temp = float(feeds["field1"])
    runtime = int(feeds["field4"])
    throttle = int(feeds["field5"])
    rpm = int(feeds["field7"])

    print([engine_temp, runtime, throttle, rpm])
    return [[engine_temp, runtime, throttle, rpm]]


def send_telegram_message(message):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        raise RuntimeError(
            "Set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID before running pred.py."
        )
    import telepot

    bot = telepot.Bot(TELEGRAM_BOT_TOKEN)
    bot.sendMessage(TELEGRAM_CHAT_ID, message)


def status_from_prediction(prediction):
    if prediction == 0:
        return "Vehicle Status: Normal"
    if prediction == 1:
        return "Vehicle Status: Needs Maintenance"
    if prediction == 2:
        return "Vehicle Status: Abnormal Condition Detected!"
    return f"Vehicle Status: Unknown prediction ({prediction})"


def main():
    model = joblib.load(MODEL_PATH)

    while True:
        try:
            input_data = get_thingspeak_data()
            if input_data is None:
                time.sleep(20)
                continue
            prediction = model.predict(input_data)[0]
            status_message = status_from_prediction(prediction)
            print(status_message)
            send_telegram_message(status_message)
        except Exception as exc:
            print(f"Monitoring error: {exc}")

        time.sleep(20)


if __name__ == "__main__":
    main()

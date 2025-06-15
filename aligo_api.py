import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("ALIGO_API_KEY")
USER_ID = os.getenv("ALIGO_USER_ID")
SENDER_KEY = os.getenv("ALIGO_SENDER_KEY")
SENDER_PHONE = os.getenv("ALIGO_SENDER_PHONE")

def send_friend_talk(name, phone, message):
    url = "https://kakaoapi.aligo.in/akv10/friend/send/"
    payload = {
        'apikey': API_KEY,
        'userid': USER_ID,
        'senderkey': SENDER_KEY,
        'sender': SENDER_PHONE,
        'receiver_1': phone,
        'recvname_1': name,
        'subject_1': '날씨 알림',
        'message_1': message
    }
    response = requests.post(url, data=payload)
    return response.json()

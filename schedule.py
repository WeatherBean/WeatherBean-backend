import schedule
import time
import json
import requests
from weather import get_weather
from db import get_connection

KAKAO_ACCESS_TOKEN = "YOUR_ACCESS_TOKEN"

# 지역명, 지역 좌표 딕셔너리리
region_xy = {
    "서울": (60, 127),
    "부산": (98, 76),
    "대구": (89, 90),
    "인천": (55, 124),
    "광주": (58, 74),
    "대전": (67, 100),
    "울산": (102, 84),
    "세종": (66, 103),
    "경기도": (60, 120),
    "강원도": (73, 134),
    "충북": (69, 107),
    "충남": (68, 100),
    "전북": (64, 89),
    "전남": (51, 67),
    "경북": (87, 106),
    "경남": (91, 77),
    "제주": (52, 38)
}


# db에서 저장된 사용자의 아이디와 지역명을 불러오는 함수
def get_users():
   pass

# 카카오톡으로 api를 보내는 함수
def send_kakao_message(text):
    headers = {
        "Authorization": f"Bearer {KAKAO_ACCESS_TOKEN}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    data = {
        "object_type": "text",
        "text": text,
        "link": {
            "web_url": "https://your-site.com",
            "mobile_web_url": "https://your-site.com"
        }
    }

    response = requests.post(
        "https://kapi.kakao.com/v2/api/talk/memo/default/send",
        headers=headers,
        data={"template_object": json.dumps(data)}
    )

    if response.status_code == 200:
        print("메시지 전송 성공")
    else:
        print(f"메시지 전송 실패: {response.text}")

# 
def job():
    users = get_users()
    for kakao_id, region in users:
        nx, ny = region_xy.get(region, (60, 127))
        weather = get_weather(region, nx, ny, service_key="http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst")
        send_kakao_message(weather)

schedule.every().day.at("07:00").do(job)

while True:
    schedule.run_pending()
    time.sleep(30)
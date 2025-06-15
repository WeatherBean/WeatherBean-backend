import schedule
import time
import json
import requests
import random
from weather import get_weather
from db import get_connection
from db import save_user

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

#지역명 오류
def uesr_input(kakao_id, user_input):
    if user_input not in region_xy:
        send_kakao_message(f"{kakao_id}님 `{user_input}`은 올바른 지역명이 아닙니다. 다시 입력해주세요.")
        return False
    else:
        save_user(kakao_id, user_input)
        send_kakao_message(f"{kakao_id}님 `{uesr_input}` 지역이 등록되었습니다. 매일 아침 7시에 날씨를 보내드리겠습니다.")
        return True
    
#운세
def luck():
    fortune = [
        "오늘은 좋은 일이 생길 예간이 가득한 하루예요",
        "웃는 얼굴이 행운을 불러올 거예요",
        "예상치 못한 기획 당신을 기다리고 있어요",
        "오늘은 당신의 작은 용기가 큰 결과를 만들 거예요",
        "평소보다 에너지가 넘치는 하루가 될 거예요",
        "뜻밖의 인연이 가까운 곳에 있습니다. 주변을 잘 살펴보세요!!",
        "오늘은 생각지도 못 한 곳에서 돈이 들어올지도 몰라요. 지갑을 열어볼 준비되셨나요?",
        "사랑운이 좋은 날이에요. 마음을 표현해도 좋은 결과가 있을 거에요",
        "돈보다 중요한 건 타이밍! 오늘은 소비보단 저축에 유리한 날입니다",
        "오늘은 행운이 따라붙는 날! 복권을 사야 하나 고민된다면... 질러보세요!!",
        "연애운 상승 중!! 설레는 대화가 시작될 수 있어요",
        "미뤄뒀던 고백, 오늘이라면 성공 확률이 높아요",
        "예상치 못한 이득이 생길 수 있어요. 작은 기회도 놓치지 마세요",
        "금전운이 강한 날입니다. 오늘은 손해 보기 어려워요!!",
        "새로운 사람돠의 연결이 오늘의 키포인트!! 열려있느 자세가 중요해요",
        "감정 기복이 있지만, 결국 좋은 쪽으로 흐르게 될 거예요!!",
        "커피 한 잔이 뜻밖의 인연을 부를 수 있어요. 주변 제안을 거절하지 마세요.",
        "비싼 물건은 피하고, 소소한 사치엔 행운이 따를 거예요",
        "주변 사람들에게 호감도가 높아지는 하루?? 인기폭발 조짐!!!??",
        "생각하고 계신 일이 있다면 오늘 시작하면 결과가 좋은 확률 97%"
    ]
    return random.choice(fortune)

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


def job():
    users = get_users()
    for kakao_id, region in users:
        nx, ny = region_xy.get(region, (60, 127))
        weather = get_weather(region, nx, ny, service_key="http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst")
        send_kakao_message(weather)

        #운세 메시지 추가
        fortune = luck()
        send_kakao_message(f"오늘의 운세 : {fortune}")

schedule.every().day.at("07:00").do(job)

while True:
    schedule.run_pending()
    time.sleep(30)
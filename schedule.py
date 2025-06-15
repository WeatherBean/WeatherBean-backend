import schedule
import time
from weather import get_weather
from aligo_api import send_friend_talk
from fortune import luck
from message_builder import build_message


# DB에서 사용자의 (전화번호, 지역명) 데이터를 가져오는 함수
def get_users():
    # 실제 DB에서 가져올 예정
    return []


# 지역 코드 매핑
region_xy = {
    "서울": (60, 127), "부산": (98, 76), "대구": (89, 90), "인천": (55, 124),
    "광주": (58, 74), "대전": (67, 100), "울산": (102, 84), "세종": (66, 103),
    "경기도": (60, 120), "강원도": (73, 134), "충북": (69, 107), "충남": (68, 100),
    "전북": (64, 89), "전남": (51, 67), "경북": (87, 106), "경남": (91, 77), "제주": (52, 38)
}

# 매일 실행되는 작업
def job():
    users = get_users()
    for phone, region in users:
        if region not in region_xy:
            print(f"[WARN] 등록되지 않은 지역: {region}")
            continue

        nx, ny = region_xy[region]

        # 날씨 정보 가져오기
        weather_data = get_weather(region, nx, ny)
        if isinstance(weather_data, str):  # 에러 메시지일 경우
            print(f"[ERROR] {weather_data}")
            continue

        tmx = weather_data.get("tmx")
        tmn = weather_data.get("tmn")
        pop = weather_data.get("pop")

        # 운세 가져오기
        fortune = luck()

        # 메시지 구성
        message = build_message(region, tmx, tmn, pop, fortune)

        # 메시지 전송
        res = send_friend_talk("사용자", phone, message)
        if res.get("result_code") == "1":
            print(f"[SUCCESS] 메시지 전송 성공: {phone}")
        else:
            print(f"[FAIL] 메시지 전송 실패: {phone} | {res.get('message')}")

# 스케줄 설정 (실제는 오전 8시, 테스트용으로는 아래 주석 해제)
schedule.every().day.at("08:00").do(job)
# schedule.every(1).minutes.do(job)  # ← 테스트용

if __name__ == "__main__":
    print("✅ 스케줄러 실행 중 (매일 08:00 친구톡 발송)")
    while True:
        schedule.run_pending()
        time.sleep(30)

import schedule
import time
from weather import get_weather
from aligo_api import send_friend_talk

# db에서 사용자의 데이터 값을 리스트로 반환하는 함수
def get_users():
    # ("전화번호", "지역명") 튜플 리스트 반환
    # 실제 DB에서 가져올 예정
    return []

region_xy = {
    "서울": (60, 127), "부산": (98, 76), "대구": (89, 90), "인천": (55, 124),
    "광주": (58, 74), "대전": (67, 100), "울산": (102, 84), "세종": (66, 103),
    "경기도": (60, 120), "강원도": (73, 134), "충북": (69, 107), "충남": (68, 100),
    "전북": (64, 89), "전남": (51, 67), "경북": (87, 106), "경남": (91, 77), "제주": (52, 38)
}

def job():
    users = get_users()
    for phone, region in users:
        if region not in region_xy:
            print(f"[WARN] 등록되지 않은 지역: {region}")
            continue

        nx, ny = region_xy[region]
        weather_text = get_weather(region, nx, ny)
        res = send_friend_talk("사용자", phone, weather_text)
        if res.get("result_code") == "1":
            print(f"[SUCCESS] 메시지 전송 성공: {phone}")
        else:
            print(f"[FAIL] 메시지 전송 실패: {phone} | {res.get('message')}")

schedule.every().day.at("08:00").do(job)

if __name__ == "__main__":
    print("✅ 스케줄러 실행 중 (매일 07:00 친구톡 발송)")
    while True:
        schedule.run_pending()
        time.sleep(30)

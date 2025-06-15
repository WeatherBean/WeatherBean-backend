from datetime import datetime

def build_message(city_name, tmx, tmn, pop, lucky):
    today = datetime.now().strftime("%Y-%m-%d")
    
    message = (
        f"[{today} 날씨 정보]\n"
        f"📍 지역: {city_name}\n"
        f"🌡 기온: 최고 {tmx}℃ / 최저 {tmn}℃\n"
        f"☔ 강수확률: {pop}%\n"
    )

    if int(pop)>=50:
        message += "우산 챙기세요!\n"
    if int(tmx) - int(tmn) >= 10:
        message += "💡 오늘 일교차 심하니까 겉옷 챙기세요!\n"

    message += f"🔮 오늘의 운세: {lucky}"
    return message
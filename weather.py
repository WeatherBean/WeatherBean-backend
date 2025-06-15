import requests
import datetime

def get_weather(city_name, nx, ny, service_key):
    # 오늘 날짜
    today = datetime.datetime.now().strftime("%Y%m%d")

    # 기본 api키
    url = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst"
    
    params = {
        "serviceKey": service_key,
        "dataType": "JSON",
        "numOfRows": "1000",
        "pageNo": "1",
        "base_date": today,
        "base_time": "0200",
        "nx": nx,
        "ny": ny
    }
    
    response = requests.get(url, params=params)
    if response.status_code != 200:
        return f"{city_name}: API 호출 실패 ({response.status_code})"
    
    items = response.json().get('response', {}).get('body', {}).get('items', {}).get('item', [])
    tmx, tmn, pop_list = None, None, []

    for item in items:
        if item['fcstDate'] == today:
            category = item['category']
            value = item['fcstValue']
            if category == 'TMX':
                tmx = value
            elif category == 'TMN':
                tmn = value
            elif category == 'POP':
                pop_list.append(int(value))

    pop = max(pop_list) if pop_list else "정보 없음"

    return f"{city_name} 날씨 🌤\n🔺 최고기온: {tmx}℃\n🔻 최저기온: {tmn}℃\n☔ 강수확률: {pop}%"
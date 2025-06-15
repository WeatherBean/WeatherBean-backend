from flask import Flask, request
from db import get_connection

app = Flask(__name__)

#db 저장 함수(채은)
def save_user(kakao_id, region):
    pass

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    user_id = data.get("userRequest", {}).get("user", {}).get("id")
    region = data.get("action", {}).get("params", {}).get("지역")

    if user_id and region:
        save_user(user_id, region)
        return {
            "version": "2.0",
            "template": {
                "outputs": [{
                    "simpleText": {
                        "text": f"{region} 지역으로 설정했어요! 내일부터 날씨를 알려드릴게요 ☀️"
                    }
                }]
            }
        }
    else:
        return {
            "version": "2.0",
            "template": {
                "outputs": [{
                    "simpleText": {
                        "text": "지역 설정에 실패했어요."
                    }
                }]
            }
        }
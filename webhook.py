from flask import Blueprint, request

webhook = Blueprint("webhook", __name__)

# dh로 저장하는 함수
def save_user(kakao_id, region):
    # TODO: 친구가 DB에 저장하도록 구현할 부분
    print(f"[DEBUG] 저장: {kakao_id} - {region}")
    pass

@webhook.route("/webhook", methods=["POST"])
def kakao_webhook():
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
                        "text": f"✅ {region} 지역으로 설정했어요!\n내일부터 날씨 알려드릴게요 ☀️"
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
                        "text": "⚠️ 지역 설정에 실패했어요. 다시 입력해 주세요!"
                    }
                }]
            }
        }

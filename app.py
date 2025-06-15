from flask import Flask
from webhook import webhook  # blueprint import

app = Flask(__name__)
app.register_blueprint(webhook)

@app.route("/")
def home():
    return "✅ 카카오 챗봇 Webhook 서버 작동 중!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

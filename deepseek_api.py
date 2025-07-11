from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY")

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    message = data.get("message")
    history = data.get("history", [])

    # 过滤掉没有content的消息
    filtered_history = [m for m in history if m.get("content")]

    payload = {
        "model": "deepseek-chat",
        "messages": filtered_history + [{"role": "user", "content": message}]
    }

    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        resp = requests.post(DEEPSEEK_API_URL, json=payload, headers=headers, timeout=60)
        resp.raise_for_status()
        ai_reply = resp.json()["choices"][0]["message"]["content"]
        return jsonify({"reply": ai_reply})
    except Exception as e:
        return jsonify({"reply": "AI服务超时或异常，请稍后再试。"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
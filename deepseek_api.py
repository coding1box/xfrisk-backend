from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os

app = Flask(__name__)
CORS(app)

# 初始化 Sophnet 客户端
client = OpenAI(
    base_url="https://www.sophnet.com/api/open-apis/v1",
    api_key=os.environ.get("SOPHNET_API_KEY")
)

# 支持的模型
MODELS = {
    "fast": "DeepSeek-V3-Fast",
    "chat": "DeepSeek-V3-Chat",
    "r1": "DeepSeek-V3-R1",
    "r2": "DeepSeek-V3-R2"
}

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    message = data.get("message")
    history = data.get("history", [])
    model = data.get("model", "fast")  # 默认使用 fast 模型
    
    # 验证模型是否有效
    if model not in MODELS:
        return jsonify({"error": f"Invalid model: {model}. Available models: {list(MODELS.keys())"}), 400
    
    # 过滤掉没有content的消息
    filtered_history = [m for m in history if m.get("content")]

    try:
        # 创建完成
        completion = client.chat.completions.create(
            model=MODELS[model],
            messages=filtered_history + [{"role": "user", "content": message}]
        )
        
        # 返回 AI 的回复
        ai_reply = completion.choices[0].message.content
        return jsonify({"reply": ai_reply})
        
    except Exception as e:
        return jsonify({"reply": f"API服务异常: {str(e)}"}), 500

if __name__ == '__main__':
    pass  # 不需要启动代码，因为由 main.py 统一管理

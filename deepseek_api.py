from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import requests
import os
import json

app = Flask(__name__)
CORS(app)

DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"
# 直接写入 DeepSeek API Key
DEEPSEEK_API_KEY = "sk-771840d51c2d4b72b0eb29fc8deb9422"

# 添加环境变量检查
print(f"DeepSeek API Key: {DEEPSEEK_API_KEY[:10]}..." if DEEPSEEK_API_KEY else "未设置API密钥")

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
        print(f"非流式请求异常：{e}")
        return jsonify({"reply": "AI服务超时或异常，请稍后再试。"}), 500

@app.route('/api/chat/stream', methods=['POST'])
def chat_stream():
    data = request.get_json()
    print("收到前端流式请求：", data)
    message = data.get("message")
    history = data.get("history", [])

    if not message:
        return jsonify({"error": "消息不能为空"}), 400

    # 过滤掉没有content的消息
    filtered_history = [m for m in history if m.get("content")]

    payload = {
        "model": "deepseek-chat",
        "messages": filtered_history + [{"role": "user", "content": message}],
        "stream": True  # 启用流式输出
    }
    print("请求DeepSeek流式payload：", payload)

    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }

    def generate():
        try:
            # 发送流式请求到DeepSeek
            resp = requests.post(DEEPSEEK_API_URL, json=payload, headers=headers, stream=True, timeout=60)
            resp.raise_for_status()
            
            for line in resp.iter_lines():
                if line:
                    line = line.decode('utf-8')
                    if line.startswith('data: '):
                        data_str = line[6:]  # 移除 'data: ' 前缀
                        if data_str.strip() == '[DONE]':
                            yield f"data: [DONE]\n\n"
                            break
                        try:
                            data_json = json.loads(data_str)
                            if 'choices' in data_json and len(data_json['choices']) > 0:
                                choice = data_json['choices'][0]
                                if 'delta' in choice and 'content' in choice['delta']:
                                    content = choice['delta']['content']
                                    if content:
                                        yield f"data: {json.dumps({'content': content})}\n\n"
                        except json.JSONDecodeError:
                            continue
                            
        except requests.exceptions.Timeout:
            print("DeepSeek流式请求超时")
            error_msg = "AI服务响应超时，请稍后再试。"
            yield f"data: {json.dumps({'error': error_msg})}\n\n"
        except requests.exceptions.RequestException as e:
            print(f"DeepSeek流式请求网络异常：{e}")
            error_msg = "AI服务网络异常，请稍后再试。"
            yield f"data: {json.dumps({'error': error_msg})}\n\n"
        except Exception as e:
            print(f"DeepSeek流式请求异常：{e}")
            error_msg = "AI服务暂时不可用，请稍后再试。"
            yield f"data: {json.dumps({'error': error_msg})}\n\n"

    return Response(generate(), mimetype='text/plain')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

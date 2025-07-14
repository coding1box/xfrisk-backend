#!/usr/bin/env python3
"""
简单的API连接测试
"""
import requests
import os

def test_api_connection():
    """测试API连接"""
    api_key = os.environ.get("DEEPSEEK_API_KEY")
    print(f"API密钥: {api_key[:10]}..." if api_key else "未设置API密钥")
    
    url = "https://api.deepseek.com/v1/chat/completions"
    
    payload = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": "你好"}],
        "max_tokens": 50
    }
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        print("正在测试DeepSeek API连接...")
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        
        print(f"状态码: {response.status_code}")
        print(f"响应头: {dict(response.headers)}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ API连接成功")
            print(f"回复: {data['choices'][0]['message']['content']}")
        else:
            print(f"❌ API连接失败")
            print(f"错误信息: {response.text}")
            
    except requests.exceptions.Timeout:
        print("❌ 请求超时")
    except requests.exceptions.RequestException as e:
        print(f"❌ 网络错误: {e}")
    except Exception as e:
        print(f"❌ 其他错误: {e}")

if __name__ == "__main__":
    test_api_connection() 
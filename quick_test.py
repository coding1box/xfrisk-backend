#!/usr/bin/env python3
import requests
import json

def test_stream():
    url = "http://localhost:8080/api/chat/stream"
    payload = {"message": "你好", "history": []}
    headers = {"Content-Type": "application/json"}
    
    try:
        print("测试流式API...")
        response = requests.post(url, json=payload, headers=headers, stream=True, timeout=30)
        
        if response.status_code == 200:
            print("✅ 连接成功，开始接收流式数据...")
            content = ""
            for line in response.iter_lines():
                if line:
                    line = line.decode('utf-8')
                    if line.startswith('data: '):
                        data_str = line[6:]
                        if data_str.strip() == '[DONE]':
                            print(f"\n✅ 完成！完整回复：{content}")
                            break
                        try:
                            data = json.loads(data_str)
                            if 'content' in data:
                                content += data['content']
                                print(data['content'], end='', flush=True)
                        except:
                            continue
        else:
            print(f"❌ 失败，状态码：{response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"❌ 错误：{e}")

if __name__ == "__main__":
    test_stream() 
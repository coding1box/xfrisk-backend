#!/usr/bin/env python3
import requests
import json
import time

def test_stream():
    url = "http://localhost:8080/api/chat/stream"
    payload = {"message": "你好", "history": []}
    headers = {"Content-Type": "application/json"}
    
    try:
        print("测试流式API...")
        response = requests.post(url, json=payload, headers=headers, stream=True, timeout=30)
        
        print(f"状态码: {response.status_code}")
        print(f"响应头: {dict(response.headers)}")
        
        if response.status_code == 200:
            print("✅ 连接成功，开始接收流式数据...")
            content = ""
            line_count = 0
            
            for line in response.iter_lines():
                line_count += 1
                print(f"收到第{line_count}行: {line}")
                
                if line:
                    line = line.decode('utf-8')
                    print(f"解码后: {line}")
                    
                    if line.startswith('data: '):
                        data_str = line[6:]
                        print(f"数据部分: {data_str}")
                        
                        if data_str.strip() == '[DONE]':
                            print(f"\n✅ 完成！完整回复：{content}")
                            break
                        
                        try:
                            data = json.loads(data_str)
                            print(f"解析的JSON: {data}")
                            if 'content' in data:
                                content += data['content']
                                print(f"当前内容: {content}")
                            elif 'error' in data:
                                print(f"❌ 错误：{data['error']}")
                                break
                        except Exception as e:
                            print(f"JSON解析错误: {e}")
                            continue
                else:
                    print("收到空行")
                    
                if line_count > 50:  # 防止无限循环
                    print("达到最大行数限制")
                    break
                    
        else:
            print(f"❌ 失败，状态码：{response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"❌ 错误：{e}")

if __name__ == "__main__":
    test_stream() 
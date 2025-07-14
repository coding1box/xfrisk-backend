#!/usr/bin/env python3
"""
测试流式输出功能的脚本
"""
import requests
import json
import sys

def test_stream_api():
    """测试流式API"""
    url = "http://localhost:8080/api/chat/stream"
    
    payload = {
        "message": "你好，请简单介绍一下自己",
        "history": []
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        print("正在测试流式API...")
        response = requests.post(url, json=payload, headers=headers, stream=True, timeout=30)
        
        if response.status_code == 200:
            print("✅ 流式API连接成功")
            print("正在接收流式数据...")
            
            accumulated_content = ""
            for line in response.iter_lines():
                if line:
                    line = line.decode('utf-8')
                    if line.startswith('data: '):
                        data_str = line[6:]
                        if data_str.strip() == '[DONE]':
                            print("\n✅ 流式传输完成")
                            print(f"完整回复：{accumulated_content}")
                            break
                        
                        try:
                            data = json.loads(data_str)
                            if 'content' in data:
                                content = data['content']
                                accumulated_content += content
                                print(content, end='', flush=True)
                            elif 'error' in data:
                                print(f"\n❌ 错误：{data['error']}")
                                break
                        except json.JSONDecodeError:
                            continue
        else:
            print(f"❌ 请求失败，状态码：{response.status_code}")
            print(f"响应内容：{response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到服务器，请确保后端服务已启动")
    except requests.exceptions.Timeout:
        print("❌ 请求超时")
    except Exception as e:
        print(f"❌ 测试失败：{e}")

def test_normal_api():
    """测试普通API"""
    url = "http://localhost:8080/api/chat"
    
    payload = {
        "message": "你好",
        "history": []
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        print("正在测试普通API...")
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ 普通API连接成功")
            print(f"回复：{data.get('reply', '无回复')}")
        else:
            print(f"❌ 请求失败，状态码：{response.status_code}")
            print(f"响应内容：{response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到服务器，请确保后端服务已启动")
    except requests.exceptions.Timeout:
        print("❌ 请求超时")
    except Exception as e:
        print(f"❌ 测试失败：{e}")

if __name__ == "__main__":
    print("=== AI流式输出测试 ===\n")
    
    # 测试普通API
    test_normal_api()
    print("\n" + "="*50 + "\n")
    
    # 测试流式API
    test_stream_api() 
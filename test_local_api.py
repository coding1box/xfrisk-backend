#!/usr/bin/env python3
"""
测试本地API
"""
import requests
import json

def test_local_api():
    """测试本地API"""
    url = "http://localhost:8080/api/chat"
    
    payload = {
        "message": "你好，请简单介绍一下自己",
        "history": []
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        print("正在测试本地API...")
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ 本地API连接成功")
            print(f"回复: {data.get('reply', '无回复')}")
        else:
            print(f"❌ 本地API连接失败")
            print(f"错误信息: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到本地服务器，请确保后端服务已启动")
    except requests.exceptions.Timeout:
        print("❌ 请求超时")
    except Exception as e:
        print(f"❌ 其他错误: {e}")

def test_local_stream_api():
    """测试本地流式API"""
    url = "http://localhost:8080/api/chat/stream"
    
    payload = {
        "message": "你好，请简单介绍一下自己",
        "history": []
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        print("\n正在测试本地流式API...")
        response = requests.post(url, json=payload, headers=headers, stream=True, timeout=30)
        
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ 本地流式API连接成功")
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
            print(f"❌ 本地流式API连接失败")
            print(f"错误信息: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到本地服务器，请确保后端服务已启动")
    except requests.exceptions.Timeout:
        print("❌ 请求超时")
    except Exception as e:
        print(f"❌ 其他错误: {e}")

if __name__ == "__main__":
    print("=== 本地API测试 ===\n")
    
    # 测试普通API
    test_local_api()
    
    # 测试流式API
    test_local_stream_api() 
"""
测试判题器API格式
"""
import requests
import json

BASE_URL = "http://localhost:8000"


def test_judge_format():
    """测试判题器格式的请求"""
    print("=" * 60)
    print("测试判题器API格式")
    print("=" * 60)
    
    url = f"{BASE_URL}/api/v1/chat"
    
    # 判题器格式的请求
    payload = {
        "model_ip": "127.0.0.1",
        "session_id": "abc123",
        "message": "查询海淀区的房源"
    }
    
    headers = {
        "Content-Type": "application/json",
        "Session-ID": "abc123"
    }
    
    print(f"\n请求URL: {url}")
    print(f"请求头: {json.dumps(headers, indent=2, ensure_ascii=False)}")
    print(f"请求体: {json.dumps(payload, indent=2, ensure_ascii=False)}")
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        print(f"\n响应状态码: {response.status_code}")
        print(f"响应头: {dict(response.headers)}")
        
        if response.status_code == 200:
            print(f"响应内容: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        else:
            print(f"错误响应: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")


def test_without_session_header():
    """测试不带Session-ID请求头的情况"""
    print("\n" + "=" * 60)
    print("测试不带Session-ID请求头")
    print("=" * 60)
    
    url = f"{BASE_URL}/api/v1/chat"
    
    payload = {
        "model_ip": "127.0.0.1",
        "session_id": "abc123",
        "message": "查询海淀区的房源"
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        print(f"响应状态码: {response.status_code}")
        if response.status_code != 200:
            print(f"错误响应: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")


if __name__ == "__main__":
    test_judge_format()
    test_without_session_header()
"""
测试Web API服务
"""
import requests
import json

BASE_URL = "http://localhost:8000"


def test_health():
    """测试健康检查"""
    print("=== 测试健康检查 ===")
    response = requests.get(f"{BASE_URL}/health")
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.json()}\n")


def test_chat(message: str):
    """测试聊天接口"""
    print(f"=== 测试聊天: {message} ===")
    response = requests.post(
        f"{BASE_URL}/api/v1/chat",
        json={"message": message}
    )
    print(f"状态码: {response.status_code}")
    print(f"响应: {json.dumps(response.json(), ensure_ascii=False, indent=2)}\n")
    return response.json()


def test_reset():
    """测试重置接口"""
    print("=== 测试重置 ===")
    response = requests.post(f"{BASE_URL}/api/v1/reset")
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.json()}\n")


if __name__ == "__main__":
    print("开始测试API服务...\n")
    
    # 健康检查
    try:
        test_health()
    except Exception as e:
        print(f"健康检查失败: {e}")
        print("请确保服务已启动: python run_server.py\n")
        exit(1)
    
    # 测试简单查询
    test_chat("我想在朝阳区租房")
    
    # 测试复杂查询
    test_chat("查询海淀+两居+近地铁+电梯+民水民电+预算5000+60平以上的房源")
    
    # 测试多轮对话
    test_chat("现在的房子太吵了，想换个安静的地方")
    test_chat("朝阳区，预算6000左右")
    test_chat("两居室，最好近地铁")
    test_chat("帮我找找看")
    
    # 重置
    test_reset()
    
    print("测试完成！")
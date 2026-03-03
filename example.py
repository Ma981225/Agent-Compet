"""
使用示例
"""
from agent import RentalHouseAgent
from utils.logger import log_info


def example_simple_query():
    """示例1：简单查询"""
    agent = RentalHouseAgent()
    
    print("=== 示例1：简单查询 ===")
    reply = agent.process_user_input("我想在朝阳区租房")
    print(f"助手：{reply}\n")


def example_complex_query():
    """示例2：复杂条件查询"""
    agent = RentalHouseAgent()
    
    print("=== 示例2：复杂条件查询 ===")
    reply = agent.process_user_input("查询海淀+两居+近地铁+电梯+民水民电+预算5000+60平以上的房源")
    print(f"助手：{reply}\n")


def example_multi_turn():
    """示例3：多轮对话"""
    agent = RentalHouseAgent()
    
    print("=== 示例3：多轮对话 ===")
    
    # 第1轮：吐槽
    reply1 = agent.process_user_input("现在的房子太吵了，想换个安静的地方")
    print(f"用户：现在的房子太吵了，想换个安静的地方")
    print(f"助手：{reply1}\n")
    
    # 第2轮：明确区域
    reply2 = agent.process_user_input("朝阳区")
    print(f"用户：朝阳区")
    print(f"助手：{reply2}\n")
    
    # 第3轮：明确预算
    reply3 = agent.process_user_input("预算6000左右")
    print(f"用户：预算6000左右")
    print(f"助手：{reply3}\n")
    
    # 第4轮：明确户型
    reply4 = agent.process_user_input("两居室，最好近地铁")
    print(f"用户：两居室，最好近地铁")
    print(f"助手：{reply4}\n")
    
    # 第5轮：搜索房源
    reply5 = agent.process_user_input("帮我找找看")
    print(f"用户：帮我找找看")
    print(f"助手：{reply5}\n")


def example_cross_platform():
    """示例4：多平台交叉筛选"""
    agent = RentalHouseAgent()
    
    print("=== 示例4：多平台交叉筛选 ===")
    
    # 第1轮：初始需求
    reply1 = agent.process_user_input("我想在海淀区租一套两居室，预算5000")
    print(f"用户：我想在海淀区租一套两居室，预算5000")
    print(f"助手：{reply1}\n")
    
    # 第2轮：搜索链家
    reply2 = agent.process_user_input("先看看链家的房源")
    print(f"用户：先看看链家的房源")
    print(f"助手：{reply2}\n")
    
    # 第3轮：搜索安居客
    reply3 = agent.process_user_input("再看看安居客的")
    print(f"用户：再看看安居客的")
    print(f"助手：{reply3}\n")
    
    # 第4轮：搜索58同城
    reply4 = agent.process_user_input("58同城的也看看")
    print(f"用户：58同城的也看看")
    print(f"助手：{reply4}\n")
    
    # 第5轮：比价
    reply5 = agent.process_user_input("帮我比价一下")
    print(f"用户：帮我比价一下")
    print(f"助手：{reply5}\n")
    
    # 第6轮：决策
    reply6 = agent.process_user_input("推荐最合适的5套")
    print(f"用户：推荐最合适的5套")
    print(f"助手：{reply6}\n")


if __name__ == "__main__":
    example_simple_query()
    example_complex_query()
    example_multi_turn()
    example_cross_platform()
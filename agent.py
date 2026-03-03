"""
租房需求匹配智能体主程序
"""
from typing import Optional, List
from models.requirement import Requirement
from models.house import HouseInfo
from services.requirement_extractor import RequirementExtractor
from services.house_fetcher import HouseFetcher
from services.house_filter import HouseFilter
from services.house_evaluator import HouseEvaluator
from config import MAX_CANDIDATES, PLATFORMS
from utils.logger import log_info, log_error, log_warning


class RentalHouseAgent:
    """租房需求匹配智能体"""
    
    def __init__(self):
        """初始化智能体"""
        self.requirement_extractor = RequirementExtractor()
        self.house_fetcher = HouseFetcher()
        self.house_filter = HouseFilter()
        self.house_evaluator = HouseEvaluator()
        self.current_requirement: Optional[Requirement] = None
        self.candidate_houses: List[HouseInfo] = []
    
    def process_user_input(self, user_input: str) -> str:
        """
        处理用户输入
        
        Args:
            user_input: 用户输入的自然语言
            
        Returns:
            回复消息
        """
        try:
            log_info("[Agent] 开始处理用户输入，长度: %d", len(user_input))
            
            requirement, reply = self.requirement_extractor.extract_requirement(
                user_input, self.current_requirement
            )
            
            log_info("[Agent] 需求提取完成，需求完整性: %s", requirement.is_complete())
            
            if requirement.is_complete():
                self.current_requirement = requirement
                log_info("[Agent] 当前需求: %s", str(requirement.model_dump(exclude_none=True)))
                
                if self._should_search_houses(user_input):
                    platforms = self._extract_platforms(user_input)
                    log_info("[Agent] 检测到搜索意图，平台: %s", platforms if platforms else "全部平台")
                    houses = self._search_and_evaluate_houses(requirement, platforms)
                    if houses:
                        log_info("[Agent] 找到 %d 套候选房源", len(houses))
                        reply = self._format_recommendation(houses)
                    else:
                        log_warning("[Agent] 未找到符合需求的房源")
                        reply = "抱歉，没有找到符合您需求的房源，请尝试调整搜索条件。"
                else:
                    log_info("[Agent] 无需搜索房源，仅进行需求提取")
            else:
                log_info("[Agent] 需求不完整，等待更多信息")
                if not self.current_requirement:
                    self.current_requirement = requirement
            
            return reply
            
        except Exception as e:
            log_error("[Agent] 处理用户输入失败: %s", str(e))
            return "抱歉，处理您的请求时遇到了问题，请重新描述您的需求。"
    
    def _should_search_houses(self, user_input: str) -> bool:
        """判断是否需要搜索房源"""
        search_keywords = ["找", "搜索", "查询", "推荐", "看看", "筛选", "比价", "决策", "房源", "房子"]
        platform_keywords = ["链家", "安居客", "58同城", "lianjia", "anjuke"]
        return any(keyword in user_input for keyword in search_keywords) or any(keyword in user_input for keyword in platform_keywords)
    
    def _search_and_evaluate_houses(self, requirement: Requirement, platforms: Optional[List[str]] = None) -> List[HouseInfo]:
        """
        搜索并评价房源
        
        Args:
            requirement: 租房需求
            platforms: 指定平台列表，如果为None则使用所有平台
            
        Returns:
            评价后的房源列表（最多5套）
        """
        log_info("[Search] ========== 开始搜索房源 ==========")
        log_info("[Search] 需求: %s", str(requirement.model_dump(exclude_none=True)))
        log_info("[Search] 平台: %s", platforms if platforms else "全部平台")
        
        houses = self.house_fetcher.fetch_houses(requirement, platforms)
        log_info("[Search] 获取到 %d 套原始房源", len(houses))
        
        original_count = len(houses)
        
        houses = self.house_filter.deduplicate_houses(houses)
        log_info("[Search] 去重后剩余 %d 套房源", len(houses))
        
        houses = self.house_filter.verify_houses(houses)
        log_info("[Search] 核验后剩余 %d 套房源", len(houses))
        
        houses = self.house_filter.filter_houses(houses, requirement)
        log_info("[Search] 筛选后剩余 %d 套房源", len(houses))
        
        if not houses:
            log_warning("[Search] 筛选后无房源，搜索结束")
            return []
        
        log_info("[Search] 开始评价 %d 套房源", len(houses))
        houses = self.house_evaluator.evaluate_houses(houses, requirement)
        
        top_houses = houses[:MAX_CANDIDATES]
        self.candidate_houses = top_houses
        
        log_info("[Search] 最终推荐 %d 套房源（原始: %d -> 最终: %d）", 
                 len(top_houses), original_count, len(top_houses))
        log_info("[Search] ========== 搜索完成 ==========")
        
        return top_houses
    
    def _format_recommendation(self, houses: List[HouseInfo]) -> str:
        """
        格式化推荐结果
        
        Args:
            houses: 房源列表
            
        Returns:
            格式化的推荐消息
        """
        if not houses:
            return "抱歉，没有找到符合您需求的房源。"
        
        message = f"为您找到 {len(houses)} 套高匹配房源：\n\n"
        
        for i, house in enumerate(houses, 1):
            message += f"【房源 {i}】\n"
            message += f"标题：{house.title}\n"
            message += f"位置：{house.district} {house.address}\n"
            message += f"租金：{house.price:.0f}元/月\n"
            message += f"面积：{house.area:.0f}平方米\n"
            message += f"户型：{house.room_type}\n"
            
            if house.floor:
                message += f"楼层：{house.floor}\n"
            if house.orientation:
                message += f"朝向：{house.orientation}\n"
            if house.decoration:
                message += f"装修：{house.decoration}\n"
            if house.has_elevator is not None:
                message += f"电梯：{'有' if house.has_elevator else '无'}\n"
            if house.near_subway:
                message += "近地铁：是\n"
            if house.water_electric:
                message += f"水电：{house.water_electric}\n"
            
            if house.total_score:
                message += f"综合评分：{house.total_score:.1f}分\n"
            
            if house.advantages:
                message += f"优点：{', '.join(house.advantages)}\n"
            if house.disadvantages:
                message += f"缺点：{', '.join(house.disadvantages)}\n"
            
            if house.url:
                message += f"链接：{house.url}\n"
            
            message += "\n"
        
        return message
    
    def _extract_platforms(self, user_input: str) -> Optional[List[str]]:
        """从用户输入中提取平台信息"""
        platform_map = {
            "链家": "lianjia",
            "lianjia": "lianjia",
            "安居客": "anjuke",
            "anjuke": "anjuke",
            "58同城": "58tongcheng",
            "58": "58tongcheng"
        }
        
        platforms = []
        for keyword, platform in platform_map.items():
            if keyword in user_input:
                platforms.append(platform)
        
        return platforms if platforms else None
    
    def reset(self):
        """重置对话状态"""
        self.current_requirement = None
        self.candidate_houses = []
        self.requirement_extractor.reset_conversation()
        self.house_fetcher.clear_cache()
        log_info("已重置对话状态")


def main():
    """主函数"""
    agent = RentalHouseAgent()
    
    print("欢迎使用租房需求匹配智能体！")
    print("请输入您的租房需求，输入'退出'或'quit'结束对话。\n")
    
    while True:
        try:
            user_input = input("您：").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ["退出", "quit", "exit"]:
                print("感谢使用，再见！")
                break
            
            if user_input.lower() in ["重置", "reset"]:
                agent.reset()
                print("已重置对话状态\n")
                continue
            
            reply = agent.process_user_input(user_input)
            print(f"\n助手：{reply}\n")
            
        except KeyboardInterrupt:
            print("\n\n感谢使用，再见！")
            break
        except Exception as e:
            log_error("主程序错误: %s", str(e))
            print(f"发生错误：{str(e)}\n")


if __name__ == "__main__":
    main()
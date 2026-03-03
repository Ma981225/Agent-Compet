"""
多维度分析评价模块
"""
from typing import List, Tuple
from models.house import HouseInfo
from models.requirement import Requirement
from config import WEIGHTS
from utils.logger import log_info, log_error


class HouseEvaluator:
    """房源评价器，从多个维度分析房源"""
    
    def __init__(self):
        """初始化评价器"""
        self.weights = WEIGHTS
    
    def evaluate_houses(self, houses: List[HouseInfo], requirement: Requirement) -> List[HouseInfo]:
        """
        对房源进行多维度评价
        
        Args:
            houses: 房源列表
            requirement: 租房需求
            
        Returns:
            评价后的房源列表（已排序）
        """
        log_info("[Evaluator] 开始评价 %d 套房源", len(houses))
        evaluated_houses = []
        
        for i, house in enumerate(houses, 1):
            commute_score = self._calculate_commute_score(house, requirement)
            price_score = self._calculate_price_score(house, houses)
            facilities_score = self._calculate_facilities_score(house, requirement)
            
            total_score = (
                commute_score * self.weights["commute"] +
                price_score * self.weights["price_ratio"] +
                facilities_score * self.weights["facilities"]
            )
            
            house.commute_score = commute_score
            house.price_ratio_score = price_score
            house.facilities_score = facilities_score
            house.total_score = total_score
            
            advantages, disadvantages = self._generate_evaluation(house, requirement)
            house.advantages = advantages
            house.disadvantages = disadvantages
            
            evaluated_houses.append(house)
            
            if i <= 3:  # 只记录前3套的详细评分
                log_info("[Evaluator] 房源 %d 评分 - 通勤: %.1f, 性价比: %.1f, 配套: %.1f, 总分: %.1f", 
                         i, commute_score, price_score, facilities_score, total_score)
        
        evaluated_houses.sort(key=lambda x: x.total_score or 0, reverse=True)
        log_info("[Evaluator] 评价完成，最高分: %.1f, 最低分: %.1f", 
                 evaluated_houses[0].total_score if evaluated_houses else 0,
                 evaluated_houses[-1].total_score if evaluated_houses else 0)
        
        return evaluated_houses
    
    def _calculate_commute_score(self, house: HouseInfo, requirement: Requirement) -> float:
        """
        计算通勤距离评分
        
        Args:
            house: 房源信息
            requirement: 租房需求
            
        Returns:
            通勤评分（0-100）
        """
        if not requirement.commute_location:
            if house.near_subway:
                return 80.0
            elif house.subway_distance:
                if house.subway_distance <= 500:
                    return 90.0
                elif house.subway_distance <= 1000:
                    return 75.0
                elif house.subway_distance <= 2000:
                    return 60.0
                else:
                    return 40.0
            return 50.0
        
        if house.near_subway:
            return 85.0
        
        if house.subway_distance:
            if house.subway_distance <= 500:
                return 95.0
            elif house.subway_distance <= 1000:
                return 80.0
            elif house.subway_distance <= 2000:
                return 65.0
            else:
                return 45.0
        
        return 50.0
    
    def _calculate_price_score(self, house: HouseInfo, all_houses: List[HouseInfo]) -> float:
        """
        计算租金性价比评分
        
        Args:
            house: 房源信息
            all_houses: 所有房源列表（用于计算均价）
            
        Returns:
            性价比评分（0-100）
        """
        if house.area <= 0:
            return 50.0
        
        price_per_sqm = house.price / house.area
        
        if not all_houses:
            return 50.0
        
        avg_price_per_sqm = sum(h.price / h.area for h in all_houses if h.area > 0) / len(all_houses)
        
        if avg_price_per_sqm <= 0:
            return 50.0
        
        ratio = price_per_sqm / avg_price_per_sqm
        
        if ratio <= 0.8:
            return 100.0
        elif ratio <= 0.9:
            return 90.0
        elif ratio <= 1.0:
            return 80.0
        elif ratio <= 1.1:
            return 70.0
        elif ratio <= 1.2:
            return 60.0
        else:
            return max(30.0, 100.0 - (ratio - 1.2) * 50)
    
    def _calculate_facilities_score(self, house: HouseInfo, requirement: Requirement) -> float:
        """
        计算生活配套评分
        
        Args:
            house: 房源信息
            requirement: 租房需求
            
        Returns:
            配套评分（0-100）
        """
        score = 50.0
        
        if house.has_elevator:
            score += 15.0
        
        if house.near_subway:
            score += 20.0
        
        if house.water_electric and "民" in house.water_electric:
            score += 10.0
        
        if house.decoration and "精" in house.decoration:
            score += 10.0
        
        if house.facilities:
            score += min(15.0, len(house.facilities) * 3.0)
        
        if house.orientation and ("南" in house.orientation or "南北" in house.orientation):
            score += 5.0
        
        return min(100.0, score)
    
    def _generate_evaluation(self, house: HouseInfo, requirement: Requirement) -> Tuple[List[str], List[str]]:
        """
        生成优缺点评价
        
        Args:
            house: 房源信息
            requirement: 租房需求
            
        Returns:
            (优点列表, 缺点列表)
        """
        advantages = []
        disadvantages = []
        
        if house.near_subway or (house.subway_distance and house.subway_distance <= 1000):
            advantages.append("交通便利，近地铁")
        elif house.subway_distance and house.subway_distance > 2000:
            disadvantages.append("距离地铁较远")
        
        price_per_sqm = house.price / house.area if house.area > 0 else 0
        if price_per_sqm > 0:
            if price_per_sqm < 50:
                advantages.append("租金性价比高")
            elif price_per_sqm > 100:
                disadvantages.append("租金相对较高")
        
        if house.has_elevator:
            advantages.append("有电梯，出行方便")
        else:
            if house.floor and "高" in house.floor:
                disadvantages.append("高楼层无电梯")
        
        if house.water_electric and "民" in house.water_electric:
            advantages.append("民水民电，费用较低")
        
        if house.decoration and "精" in house.decoration:
            advantages.append("精装修，可直接入住")
        elif house.decoration and "简" in house.decoration:
            disadvantages.append("装修较简单")
        
        if house.orientation and ("南" in house.orientation or "南北" in house.orientation):
            advantages.append("朝向好，采光充足")
        elif house.orientation and "北" in house.orientation:
            disadvantages.append("北向，采光一般")
        
        if house.facilities and len(house.facilities) >= 5:
            advantages.append("配套设施齐全")
        elif not house.facilities or len(house.facilities) < 3:
            disadvantages.append("配套设施较少")
        
        if not advantages:
            advantages.append("房源信息完整")
        
        return advantages, disadvantages
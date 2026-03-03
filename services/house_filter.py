"""
房源筛选和核验模块
"""
from typing import List
from models.house import HouseInfo
from models.requirement import Requirement
from utils.logger import log_info, log_error


class HouseFilter:
    """房源筛选器，用于根据需求筛选和核验房源"""
    
    def filter_houses(self, houses: List[HouseInfo], requirement: Requirement) -> List[HouseInfo]:
        """
        根据需求筛选房源
        
        Args:
            houses: 房源列表
            requirement: 租房需求
            
        Returns:
            筛选后的房源列表
        """
        log_info("[Filter] 开始筛选房源，原始数量: %d", len(houses))
        log_info("[Filter] 筛选条件: %s", str(requirement.model_dump(exclude_none=True)))
        
        filtered = []
        rejected_count = 0
        
        for house in houses:
            if self._match_requirement(house, requirement):
                filtered.append(house)
            else:
                rejected_count += 1
        
        log_info("[Filter] 筛选完成，通过: %d，拒绝: %d", len(filtered), rejected_count)
        return filtered
    
    def _match_requirement(self, house: HouseInfo, requirement: Requirement) -> bool:
        """判断房源是否匹配需求"""
        if requirement.district and requirement.district not in house.district:
            return False
        
        if requirement.price_min and house.price < requirement.price_min:
            return False
        
        if requirement.price_max and house.price > requirement.price_max:
            return False
        
        if requirement.room_type and requirement.room_type not in house.room_type:
            return False
        
        if requirement.area_min and house.area < requirement.area_min:
            return False
        
        if requirement.area_max and house.area > requirement.area_max:
            return False
        
        if requirement.near_subway is not None:
            if requirement.near_subway and not house.near_subway:
                return False
        
        if requirement.has_elevator is not None:
            if requirement.has_elevator and not house.has_elevator:
                return False
        
        if requirement.water_electric:
            if house.water_electric and requirement.water_electric not in house.water_electric:
                return False
        
        if requirement.decoration:
            if house.decoration and requirement.decoration not in house.decoration:
                return False
        
        if requirement.orientation:
            if house.orientation and requirement.orientation not in house.orientation:
                return False
        
        return True
    
    def deduplicate_houses(self, houses: List[HouseInfo]) -> List[HouseInfo]:
        """
        去重房源（基于地址和价格）
        
        Args:
            houses: 房源列表
            
        Returns:
            去重后的房源列表
        """
        seen = set()
        unique_houses = []
        
        for house in houses:
            key = (house.address, house.price, house.area)
            if key not in seen:
                seen.add(key)
                unique_houses.append(house)
        
        log_info("去重后剩余 %d 套房源", len(unique_houses))
        return unique_houses
    
    def verify_houses(self, houses: List[HouseInfo]) -> List[HouseInfo]:
        """
        核验房源信息完整性
        
        Args:
            houses: 房源列表
            
        Returns:
            核验通过的房源列表
        """
        verified = []
        
        for house in houses:
            if self._verify_house(house):
                verified.append(house)
            else:
                log_info("房源 %s 信息不完整，已过滤", house.id)
        
        return verified
    
    def _verify_house(self, house: HouseInfo) -> bool:
        """核验单个房源信息"""
        if not house.id or not house.title:
            return False
        
        if house.price <= 0 or house.area <= 0:
            return False
        
        if not house.district or not house.address:
            return False
        
        return True
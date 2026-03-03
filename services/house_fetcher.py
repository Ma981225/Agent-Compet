"""
房源数据获取模块
"""
import requests
from typing import List, Dict, Any, Optional
from models.house import HouseInfo
from models.requirement import Requirement
from config import API_BASE_URL, PLATFORMS
from utils.logger import log_info, log_error, log_warning


class HouseFetcher:
    """房源数据获取器，支持多平台数据获取"""
    
    def __init__(self):
        """初始化房源获取器"""
        self.base_url = API_BASE_URL
        self.platforms = PLATFORMS
        self.cache: Dict[str, List[HouseInfo]] = {}
    
    def fetch_houses(self, requirement: Requirement, platforms: Optional[List[str]] = None) -> List[HouseInfo]:
        """
        根据需求获取房源信息
        
        Args:
            requirement: 租房需求
            platforms: 指定平台列表，如果为None则使用所有平台
            
        Returns:
            房源信息列表
        """
        if platforms is None:
            platforms = self.platforms
        
        all_houses = []
        cache_key = self._generate_cache_key(requirement, platforms)
        
        if cache_key in self.cache:
            log_info("使用缓存的房源数据")
            return self.cache[cache_key]
        
        for platform in platforms:
            try:
                houses = self._fetch_from_platform(platform, requirement)
                all_houses.extend(houses)
                log_info("从平台 %s 获取到 %d 套房源", platform, len(houses))
            except Exception as e:
                log_error("从平台 %s 获取房源失败: %s", platform, str(e))
        
        self.cache[cache_key] = all_houses
        return all_houses
    
    def _fetch_from_platform(self, platform: str, requirement: Requirement) -> List[HouseInfo]:
        """
        从指定平台获取房源
        
        Args:
            platform: 平台名称
            requirement: 租房需求
            
        Returns:
            房源信息列表
        """
        url = f"{self.base_url}/api/houses/search"
        params = self._build_search_params(requirement, platform)
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            houses = []
            for item in data.get("houses", []):
                try:
                    house = self._parse_house_data(item, platform)
                    houses.append(house)
                except Exception as e:
                    log_warning("解析房源数据失败: %s", str(e))
                    continue
            
            return houses
            
        except requests.exceptions.RequestException as e:
            log_error("请求平台 %s 失败: %s", platform, str(e))
            return []
    
    def _build_search_params(self, requirement: Requirement, platform: str) -> Dict[str, Any]:
        """构建搜索参数"""
        params = {
            "platform": platform
        }
        
        if requirement.district:
            params["district"] = requirement.district
        if requirement.price_min:
            params["price_min"] = requirement.price_min
        if requirement.price_max:
            params["price_max"] = requirement.price_max
        if requirement.room_type:
            params["room_type"] = requirement.room_type
        if requirement.area_min:
            params["area_min"] = requirement.area_min
        if requirement.area_max:
            params["area_max"] = requirement.area_max
        if requirement.near_subway is not None:
            params["near_subway"] = requirement.near_subway
        if requirement.has_elevator is not None:
            params["has_elevator"] = requirement.has_elevator
        if requirement.water_electric:
            params["water_electric"] = requirement.water_electric
        if requirement.decoration:
            params["decoration"] = requirement.decoration
        if requirement.orientation:
            params["orientation"] = requirement.orientation
        
        return params
    
    def _parse_house_data(self, data: Dict[str, Any], platform: str) -> HouseInfo:
        """解析房源数据"""
        return HouseInfo(
            id=str(data.get("id", "")),
            platform=platform,
            title=data.get("title", ""),
            district=data.get("district", ""),
            address=data.get("address", ""),
            price=float(data.get("price", 0)),
            area=float(data.get("area", 0)),
            room_type=data.get("room_type", ""),
            floor=data.get("floor"),
            orientation=data.get("orientation"),
            decoration=data.get("decoration"),
            has_elevator=data.get("has_elevator"),
            near_subway=data.get("near_subway"),
            subway_distance=data.get("subway_distance"),
            water_electric=data.get("water_electric"),
            facilities=data.get("facilities", []),
            images=data.get("images", []),
            url=data.get("url")
        )
    
    def _generate_cache_key(self, requirement: Requirement, platforms: List[str]) -> str:
        """生成缓存键"""
        req_dict = requirement.model_dump(exclude_none=True)
        return f"{sorted(platforms)}:{sorted(req_dict.items())}"
    
    def clear_cache(self):
        """清空缓存"""
        self.cache.clear()
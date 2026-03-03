"""
房源信息数据模型
"""
from typing import Optional, List, Dict
from pydantic import BaseModel, Field


class HouseInfo(BaseModel):
    """房源信息模型"""
    id: str = Field(..., description="房源ID")
    platform: str = Field(..., description="平台名称")
    title: str = Field(..., description="房源标题")
    district: str = Field(..., description="区域")
    address: str = Field(..., description="详细地址")
    price: float = Field(..., description="租金（元/月）")
    area: float = Field(..., description="面积（平方米）")
    room_type: str = Field(..., description="户型")
    floor: Optional[str] = Field(None, description="楼层")
    orientation: Optional[str] = Field(None, description="朝向")
    decoration: Optional[str] = Field(None, description="装修情况")
    has_elevator: Optional[bool] = Field(None, description="是否有电梯")
    near_subway: Optional[bool] = Field(None, description="是否近地铁")
    subway_distance: Optional[float] = Field(None, description="距离地铁站距离（米）")
    water_electric: Optional[str] = Field(None, description="水电类型")
    facilities: Optional[List[str]] = Field(None, description="配套设施")
    images: Optional[List[str]] = Field(None, description="房源图片")
    url: Optional[str] = Field(None, description="房源链接")
    
    # 分析评价字段
    commute_score: Optional[float] = Field(None, description="通勤评分")
    price_ratio_score: Optional[float] = Field(None, description="租金性价比评分")
    facilities_score: Optional[float] = Field(None, description="生活配套评分")
    total_score: Optional[float] = Field(None, description="综合评分")
    advantages: Optional[List[str]] = Field(None, description="优点")
    disadvantages: Optional[List[str]] = Field(None, description="缺点")


class HouseList(BaseModel):
    """房源列表模型"""
    houses: List[HouseInfo] = Field(default_factory=list, description="房源列表")
    total: int = Field(0, description="总数量")
